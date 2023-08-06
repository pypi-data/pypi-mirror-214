# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Propagate operator class and public API function definition."""


from typing import List
from temporian.core import operator_lib
from temporian.core.data.node import Node, create_node_new_features_new_sampling
from temporian.core.operators.base import Operator
from temporian.core.operators.resample import Resample
from temporian.proto import core_pb2 as pb


class Propagate(Operator):
    def __init__(
        self,
        input: Node,
        sampling: Node,
    ):
        super().__init__()

        self.add_input("input", input)
        self.add_input("sampling", sampling)

        self._index_mapping: List[int] = []

        sampling_index_name = sampling.schema.index_names()
        sampling_index_dtypes = sampling.schema.index_dtypes()

        for index in input.schema.indexes:
            try:
                sampling_idx = sampling_index_name.index(index.name)
                self._index_mapping.append(sampling_idx)
            except ValueError as exc:
                raise ValueError(
                    "The index of input should be contained in the index of"
                    f' sampling. Index "{index.name}" from input is not'
                    " available in sampling. input.index="
                    f" {input.schema.indexes},"
                    f" sampling.index={sampling.schema.indexes}."
                ) from exc
            if sampling_index_dtypes[sampling_idx] != index.dtype:
                raise ValueError(
                    f'The index "{index.name}" is found both in the input and'
                    " sampling argument. However, the dtype is different."
                    f" {index.dtype} != {sampling_index_dtypes[sampling_idx]}"
                )

        # Note: The propagate operator creates a new sampling.
        self.add_output(
            "output",
            create_node_new_features_new_sampling(
                features=input.schema.features,
                indexes=sampling.schema.indexes,
                is_unix_timestamp=sampling.schema.is_unix_timestamp,
                creator=self,
            ),
        )

        self.check()

    @property
    def index_mapping(self):
        return self._index_mapping

    @classmethod
    def build_op_definition(cls) -> pb.OperatorDef:
        return pb.OperatorDef(
            key="PROPAGATE",
            attributes=[],
            inputs=[
                pb.OperatorDef.Input(key="input"),
                pb.OperatorDef.Input(key="sampling"),
            ],
            outputs=[pb.OperatorDef.Output(key="output")],
        )


operator_lib.register_operator(Propagate)


# TODO: Do we want for "propagate" to take a list of feature names
# (like add_index) instead?
def propagate(input: Node, sampling: Node, resample: bool = False) -> Node:
    """Propagates feature values over a sub index.

    Given `input` and `sampling` where `input` has a super index of
    `sampling` (e.g., the index of `input` is `["x"]`, and the index of
    `sampling` is `["x","y"]`), duplicates the features of `input` over the
    index of `sampling`.

    Example:

        Inputs:
            input:
                feature_1: ...
                feature_2: ...
                index: ["x"]
            sampling:
                index: ["x", "y"]

        Output:
            feature_1: ...
            feature_2: ...
            index: ["x", "y"]

    Args:
        input: Node to propagate.
        sampling: Index to propagate over.
        resample: If true, apply a [`tp.resample()`][temporian.resample] before
            propagating, for the output to have the same sampling as `sampling`.

    Returns:
        Node propagated over `sampling`'s index.
    """

    result = Propagate(
        input=input,
        sampling=sampling,
    ).outputs["output"]

    if resample:
        result = Resample(input=result, sampling=sampling).outputs["output"]

    return result
