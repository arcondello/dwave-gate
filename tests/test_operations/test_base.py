# Copyright 2022 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import math

import numpy as np
import pytest

import dwave.gate.operations.operations as ops
from dwave.gate.circuit import Circuit, ParametricCircuit
from dwave.gate.operations.base import ABCLockedAttr, Operation, create_operation


class TestLockedMetaclass:
    """Unit tests for the ``ABCLockedAttr`` metaclass.

    The list of locked attributes is part of the ``ABCLockedAttr`` metaclass. If adding a locked
    attribute there, please update this test to also test that locked attribute.
    """

    def test_locked_attribute(self):
        """Test that a locked class attribute cannot be changed."""

        class DummyLocked(metaclass=ABCLockedAttr):
            """Dummy class used to test the ``ABCLockedAttr`` metaclass."""

            matrix = [[1, 0], [0, 1]]
            not_matrix = 42

        assert DummyLocked.not_matrix == 42
        DummyLocked.not_matrix = 24
        assert DummyLocked.not_matrix == 24

        with pytest.raises(ValueError, match="Cannot set class attribute"):
            DummyLocked.matrix = 5

    def test_locked_attribute_subclass(self):
        """Test that a locked class attribute cannot be changed in a subclass."""

        class DummyLocked(metaclass=ABCLockedAttr):
            """Dummy class used to test the ``ABCLockedAttr`` metaclass."""

            matrix = [[1, 0], [0, 1]]
            not_matrix = 42

        class DummySub(DummyLocked):
            pass

        assert DummySub.not_matrix == 42
        DummySub.not_matrix = 24
        assert DummySub.not_matrix == 24

        with pytest.raises(ValueError, match="Cannot set class attribute"):
            DummySub.matrix = 5


class TestMatrixRepr:
    """Unit tests for all matrix representations of operations."""

    @pytest.mark.parametrize(
        "op, matrix",
        [
            (ops.X, np.array([[0, 1], [1, 0]])),
            (ops.Y, np.array([[0.0, -1.0j], [1.0j, 0.0]])),
            (ops.Z, np.array([[1, 0], [0, -1]])),
            (ops.Hadamard, math.sqrt(2) / 2 * np.array([[1.0, 1.0], [1.0, -1.0]])),
            (ops.RX(np.pi / 2), math.sqrt(2) / 2 * np.array([[1, -1j], [-1j, 1]])),
            (ops.RY(np.pi / 2), math.sqrt(2) / 2 * np.array([[1, -1], [1, 1]])),
            (ops.RZ(np.pi / 2), math.sqrt(2) / 2 * np.array([[1 - 1j, 0], [0, 1 + 1j]])),
            (ops.Rotation([np.pi / 2] * 3), math.sqrt(2) / 2 * np.array([[-1j, -1], [1, 1j]])),
            (ops.CX, np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])),
            (ops.CNOT, np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])),
            # (ops.CX(1, 0), np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])),
            (ops.CZ, np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])),
            (
                ops.SWAP,
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            ),
            (
                ops.CSWAP,
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            ),
            (
                ops.CCNOT,
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                    ]
                ),
            ),
            (
                ops.CRX(np.pi / 2),
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, math.sqrt(2) / 2, math.sqrt(2) / 2 * -1j],
                        [0.0, 0.0, math.sqrt(2) / 2 * -1j, math.sqrt(2) / 2],
                    ]
                ),
            ),
            (
                ops.CRY(np.pi / 2),
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, math.sqrt(2) / 2 * 1.0, -math.sqrt(2) / 2],
                        [0.0, 0.0, math.sqrt(2) / 2 * 1.0, math.sqrt(2) / 2 * 1.0],
                    ]
                ),
            ),
            (
                ops.CRZ(np.pi / 2),
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, math.sqrt(2) / 2 * (1 - 1j), 0.0],
                        [0.0, 0.0, 0.0, math.sqrt(2) / 2 * (1 + 1j)],
                    ]
                ),
            ),
            (
                ops.CRotation([np.pi / 2] * 3),
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, math.sqrt(2) / 2 * -1j, math.sqrt(2) / 2 * -1.0],
                        [0.0, 0.0, math.sqrt(2) / 2 * 1.0, math.sqrt(2) / 2 * 1j],
                    ]
                ),
            ),
        ],
    )
    def test_matrix_repr(self, op, matrix):
        """Test that matrix representations are correct."""
        assert np.allclose(op.matrix, matrix)

        # if matrix is accessed as a classproperty, then test it on an instance as well
        if not isinstance(op, Operation):
            assert np.allclose(op().matrix, matrix)

    @pytest.mark.parametrize(
        "op, qubits, matrix",
        [
            (ops.CX, [0, 1], np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])),
            (ops.CNOT, [0, 1], np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])),
            (ops.CX, [1, 0], np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])),
            (ops.CZ, [0, 1], np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])),
        ],
    )
    def test_controlled_matrix_repr(self, op, qubits, matrix, two_qubit_circuit):
        """Test that controlled matrix representations are correct."""
        two_qubit_circuit.unlock()
        with two_qubit_circuit.context as q:
            assert np.allclose(op(*[q[i] for i in qubits]).matrix, matrix)


@pytest.mark.xfail(reason="Measurements are not implemented yet.")
class TestMeasurement:
    """Unit tests for the ``Measurement`` class."""


@pytest.mark.xfail(reason="Barriers are not implemented yet.")
class TestBarrier:
    """Unit tests for the ``Barrier`` class."""


class TestCreateOperation:
    """Unit tests for the ``create_operation`` function."""

    def test_parametric(self):
        """Test creating an operation out of a parametric circuit."""
        circuit = ParametricCircuit(1)

        with circuit.context as (p, q):
            ops.RZ(p[0], q[0])
            ops.RY(p[1], q[0])
            ops.RZ(p[2], q[0])

        RotOp = create_operation(circuit, name="Rot")
        params = [0.23, 0.34, 0.45]
        rot_op = RotOp(params)

        assert RotOp.matrix is None
        assert RotOp.label == "Rot"

        assert np.allclose(rot_op.matrix, ops.Rotation(params).matrix)
        assert rot_op.label == f"Rot({params})"

    def test_non_parametric(self):
        """Test creating an operation out of a non-parametric circuit."""
        circuit = Circuit(1)

        with circuit.context as q:
            ops.Hadamard(q[0])
            ops.X(q[0])
            ops.Hadamard(q[0])

        ZOp = create_operation(circuit, name="Z")

        assert np.allclose(ZOp.matrix, ops.Z.matrix)
        assert ZOp.label == "Z"

    def test_no_label(self):
        """Test creating an operation without a label."""
        circuit = Circuit(1)

        with circuit.context as q:
            ops.Hadamard(q[0])
            ops.X(q[0])
            ops.Hadamard(q[0])

        ZOp = create_operation(circuit)

        assert ZOp.label == "CustomOperation"

    def test_parametric_mix(self):
        """Test creating an operation out of a parametric circuit with some hard-coded
        parameters."""
        circuit = ParametricCircuit(1)

        with circuit.context as (p, q):
            ops.RZ(0.1, q[0])
            ops.RY(p[0], q[0])
            ops.RZ(0.3, q[0])
            ops.X(q[0])  # cover testing non-parametric ops in parametric circuits
            ops.X(q[0])  # negate the previous X-gate to compare with Rotation-gate

        RotOp = create_operation(circuit, name="Rot")
        params = [0.2]
        rot_op = RotOp(params)

        assert RotOp.matrix is None
        assert RotOp.label == "Rot"

        assert np.allclose(rot_op.matrix, ops.Rotation([0.1, 0.2, 0.3]).matrix)
        assert rot_op.label == "Rot([0.2])"
