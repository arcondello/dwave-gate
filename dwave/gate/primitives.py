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

__all__ = [
    "Qubit",
    "Bit",
    "Variable",
]

from typing import Hashable, Optional

from dwave.gate.tools.counters import IDCounter


class Qubit:
    """Qubit type.

    Args:
        label: Label used to represent the qubit.
    """

    def __init__(self, label: Hashable) -> None:
        self._label = label
        self._id: str = IDCounter.next()

    @property
    def label(self) -> Hashable:
        """The qubit's name."""
        return self._label

    @property
    def id(self) -> str:
        """The qubit's unique identification number."""
        return self._id

    def __eq__(self, object: object) -> bool:
        """Two qubits are equal if they share the same id."""
        if isinstance(object, Qubit):
            return self.id == object.id
        return False

    def __repr__(self) -> str:
        """The representation of the variable is its label."""
        return f"<qubit: {self.label}, id:{self.id}>"

    def __hash__(self) -> int:
        """The hash of the qubit is determined by its id."""
        return hash(self.__class__.__name__ + self.id)


class Bit:
    """Classical bit type.

    Args:
        label: Label used to represent the bit.
    """

    def __init__(self, label: Hashable) -> None:
        self._label = label
        self._id: str = IDCounter.next()

    @property
    def label(self) -> Hashable:
        """The bit's label."""
        return self._label

    @property
    def id(self) -> str:
        """The bit's unique identification number."""
        return self._id

    def __eq__(self, object: object) -> bool:
        """Two bits are equal if they share the same id."""
        if isinstance(object, Bit):
            return self.id == object.id
        return False

    def __repr__(self) -> str:
        """The representation of the variable is its label."""
        return f"<bit: {self.label}, id:{self.id}>"

    def __hash__(self) -> int:
        """The hash of the qubit is determined by its id."""
        return hash(self.__class__.__name__ + self.id)


class Variable:
    """Variable parameter type.

    Used as a placeholder for parameter values. Two variables with the same label are considered
    equal (``Variable('a') == Variable('a')``) and have the same hash value, but not identical
    (``Variable('a') is not Variable('a')``)

    Args:
        name: String used to represent the variable.
    """

    def __init__(self, name: str) -> None:
        self._name = str(name)

        self._value: Optional[complex] = None

    @property
    def name(self) -> str:
        """The variable name."""
        return self._name

    @property
    def value(self) -> Optional[complex]:
        """The variable value, if set."""
        return self._value

    def __eq__(self, object: object) -> bool:
        """Two variables are equal if they share the same label."""
        if isinstance(object, Variable):
            return self.name == object.name
        if self._value and self._value == object:
            return True
        return False

    def __repr__(self) -> str:
        """The representation of the variable is its label."""
        if self._value:
            return str(self.value)
        return f"{{{self.name}}}"

    def __hash__(self) -> int:
        """The hash of the variable is determined by its label."""
        return hash(self.name)

    def set(self, value: complex):
        """Set a value for the variable.

        Args:
            value: Value that the variable should have.
        """
        self._value = value

    def reset(self):
        """Reset the variable value to ``None``."""
        self._value = None
