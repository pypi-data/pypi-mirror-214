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

from temporian.implementation.numpy.data.event_set import EventSet
from temporian.implementation.numpy.operators.base import OperatorImplementation
from temporian.core.operators.base import Operator
from temporian.core.serialization import serialize


def assertEqualEventSet(self, real: EventSet, expected: EventSet):
    """Asserts the equality between real and expected.

    Prints a nice message in case of error.
    """

    self.assertEqual(
        real,
        expected,
        f"\nREAL:\n{real}\nEXPECTED:\n{expected}",
    )


def testOperatorAndImp(self, op: Operator, imp: OperatorImplementation):
    """Tests an operator and its implementation.

    Currently test:
      - Serialization / unserialization of the operator.
    """

    # TODO: Add tests related to the implementation.
    del imp

    serialized_op = serialize._serialize_operator(op)

    nodes = {}
    for node in op.inputs.values():
        nodes[serialize._identifier(node)] = node
    for node in op.outputs.values():
        nodes[serialize._identifier(node)] = node

    _ = serialize._unserialize_operator(serialized_op, nodes)
