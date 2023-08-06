from typing import NewType

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model import Model as APIModel
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.model import SerializedModel
from classiq.interface.generator.model.preferences.preferences import Preferences

from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper

SerializedQuantumProgram = NewType("SerializedQuantumProgram", str)


def synthesize(model: SerializedModel) -> SerializedQuantumProgram:
    api_model = APIModel.parse_raw(model)
    quantum_program = async_utils.run(ApiWrapper.call_generation_task(api_model))
    return SerializedQuantumProgram(quantum_program.json(indent=2))


def set_preferences(
    model: SerializedModel, preferences: Preferences
) -> SerializedModel:
    api_model = APIModel.parse_raw(model)
    api_model.preferences = preferences
    return api_model.get_model()


def set_constraints(
    model: SerializedModel, constraints: Constraints
) -> SerializedModel:
    api_model = APIModel.parse_raw(model)
    api_model.constraints = constraints
    return api_model.get_model()


def set_execution_preferences(
    model: SerializedModel, execution_preferences: ExecutionPreferences
) -> SerializedModel:
    api_model = APIModel.parse_raw(model)
    api_model.execution_preferences = execution_preferences
    return api_model.get_model()


__all__ = [
    "SerializedModel",
    "synthesize",
    "set_preferences",
    "set_constraints",
    "set_execution_preferences",
]
