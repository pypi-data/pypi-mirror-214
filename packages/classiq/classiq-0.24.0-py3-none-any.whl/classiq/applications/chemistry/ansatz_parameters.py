import dataclasses
from typing import List, Tuple, Union

from classiq.interface.generator.excitations import EXCITATIONS_TYPE_EXACT


@dataclasses.dataclass
class UCCParameters:
    excitations: EXCITATIONS_TYPE_EXACT


@dataclasses.dataclass
class HVAParameters:
    reps: int


@dataclasses.dataclass
class HEAParameters:
    reps: int
    num_qubits: int
    connectivity_map: List[Tuple[int, int]]
    one_qubit_gates: List[str]
    two_qubit_gates: List[str]


AnsatzParameters = Union[UCCParameters, HVAParameters, HEAParameters]
