from typing import Mapping, Optional

import pydantic

from classiq.interface.generator.classical_function_call import ClassicalFunctionCall
from classiq.interface.generator.functions import FunctionDeclaration
from classiq.interface.generator.functions.quantum_invoker_declaration import (
    QuantumInvokerDeclaration,
)
from classiq.interface.generator.quantum_function_call import QuantumLambdaFunction

from classiq.exceptions import ClassiqValueError


class QuantumInvokerCall(ClassicalFunctionCall):
    target_function: QuantumLambdaFunction = pydantic.Field(
        description="A lambda function of the invoked quantum entry point"
    )

    _func_decl: Optional[QuantumInvokerDeclaration] = pydantic.PrivateAttr(default=None)

    def resolve_function_decl(
        self,
        function_dict: Mapping[str, FunctionDeclaration],
    ):
        super().resolve_function_decl(function_dict)
        if len(self.target_function.body) != 1:
            raise ClassiqValueError(
                "The lambda function passed to a quantum-invoker must contain exactly one function call."
            )
