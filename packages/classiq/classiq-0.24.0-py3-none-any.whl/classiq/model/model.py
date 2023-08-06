"""Model module, implementing facilities for designing models and generating circuits using Classiq platform."""
from __future__ import annotations

import logging
import tempfile
from contextlib import nullcontext
from typing import IO, ContextManager, Dict, List, Mapping, Optional, Union

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.functions import NativeFunctionDefinition
from classiq.interface.generator.functions.assignment_statement import (
    AssignmentStatement,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
)
from classiq.interface.generator.functions.classical_type import Real
from classiq.interface.generator.functions.save_statement import SaveStatement
from classiq.interface.generator.functions.variable_declaration_statement import (
    VariableDeclaration,
)
from classiq.interface.generator.generated_circuit import GeneratedCircuit
from classiq.interface.generator.model import (
    Constraints,
    Model as APIModel,
    Preferences,
)
from classiq.interface.generator.model.model import (
    CLASSICAL_ENTRY_FUNCTION_NAME,
    MAIN_FUNCTION_NAME,
)
from classiq.interface.generator.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.generator.types.builtin_struct_declarations.pauli_struct_declarations import (
    Hamiltonian,
)

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import AsyncifyABC
from classiq.exceptions import ClassiqError
from classiq.model import function_handler
from classiq.quantum_functions.function_library import FunctionLibrary
from classiq.quantum_register import QReg, QRegGenericAlias
from classiq.synthesis import SerializedModel

_logger = logging.getLogger(__name__)

_SupportedIO = Union[IO, str]

# TODO: Add docstrings for auto generated methods.


def _file_handler(fp: Optional[_SupportedIO], mode: str = "r") -> ContextManager[IO]:
    if fp is None:
        temp_file = tempfile.NamedTemporaryFile(mode, suffix=".qmod", delete=False)
        print(f"Using temporary file: {temp_file.name!r}")
        return temp_file

    if isinstance(fp, str):
        return open(fp, mode)

    return nullcontext(fp)


class Model(function_handler.FunctionHandler, metaclass=AsyncifyABC):
    """Facility to generate circuits, based on the model."""

    def __init__(self, **kwargs) -> None:
        """Init self."""
        super().__init__()
        self._model = APIModel(**kwargs)

    @classmethod
    def from_model(cls, model: APIModel) -> Model:
        return cls(**dict(model))

    @property
    def _body(
        self,
    ) -> List[QuantumFunctionCall]:
        return self._model.body

    @property
    def constraints(self) -> Constraints:
        """Get the constraints aggregated in self.

        Returns:
            The constraints data.
        """
        return self._model.constraints

    @property
    def preferences(self) -> Preferences:
        """Get the preferences aggregated in self.

        Returns:
            The preferences data.
        """
        return self._model.preferences

    def create_inputs(
        self, inputs: Mapping[IOName, QRegGenericAlias]
    ) -> Dict[IOName, QReg]:
        qregs = super().create_inputs(inputs=inputs)
        self._model.set_inputs(self.input_wires)
        return qregs

    def set_outputs(self, outputs: Mapping[IOName, QReg]) -> None:
        super().set_outputs(outputs=outputs)
        self._model.set_outputs(self.output_wires)

    async def synthesize_async(
        self,
        constraints: Optional[Constraints] = None,
        preferences: Optional[Preferences] = None,
    ) -> GeneratedCircuit:
        """Async version of `generate`
        Generates a circuit, based on the aggregation of requirements in self.

        Returns:
            The results of the generation procedure.
        """
        self._model.preferences = preferences or self._model.preferences
        self._model.constraints = constraints or self._model.constraints
        return await ApiWrapper.call_generation_task(self._model)

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a user-defined custom function library.

        Args:
            library (FunctionLibrary): The custom function library.
        """
        super().include_library(library=library)
        # It is important that the .functions list is shared between the library and
        # the model, as it is modified in-place
        self._model.functions = library._data
        library.remove_function_definition(MAIN_FUNCTION_NAME)
        self._model.functions.append(NativeFunctionDefinition(name=MAIN_FUNCTION_NAME))

    def get_model(self) -> SerializedModel:
        return self._model.get_model()

    def create_library(self) -> None:
        self._function_library = FunctionLibrary(*self._model.functions)
        self._model.functions = self._function_library._data

    def sample(
        self, num_shots: int, execution_params: Optional[Dict[str, float]] = None
    ) -> None:
        execution_params = execution_params or dict()

        if CLASSICAL_ENTRY_FUNCTION_NAME in self._model.classical_functions:
            raise ClassiqError("A classical entry function already exists in the model")

        sample_entry_point = ClassicalFunctionDefinition(
            name=CLASSICAL_ENTRY_FUNCTION_NAME,
            body=[
                VariableDeclaration(name="result", var_type=Hamiltonian()),
                AssignmentStatement(
                    assigned_variable="result",
                    invoked_expression=QuantumInvokerCall(
                        function="sample",
                        params={"num_shots": Expression(expr=f"{num_shots}")},
                        target_function=QuantumLambdaFunction(
                            body=[
                                QuantumFunctionCall(
                                    function=MAIN_FUNCTION_NAME,
                                    params={
                                        name: Expression(expr=str(value))
                                        for name, value in execution_params.items()
                                    },
                                ),
                            ],
                        ),
                    ),
                ),
                SaveStatement(saved_variable="result"),
            ],
        )

        self._model.classical_functions.append(sample_entry_point)
        self._model.function_dict[MAIN_FUNCTION_NAME].param_decls = {
            name: Real() for name in execution_params.keys()
        }
