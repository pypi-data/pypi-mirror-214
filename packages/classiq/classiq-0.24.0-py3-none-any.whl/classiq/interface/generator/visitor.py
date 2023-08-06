from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar, Union

from pydantic import BaseModel

NodeType = TypeVar("NodeType", bound=Union[dict, list, str, BaseModel])
ConcreteBaseModel = TypeVar("ConcreteBaseModel", bound=BaseModel)
Key = TypeVar("Key")


class Visitor:
    def visit(self, node: NodeType) -> Optional[NodeType]:
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: NodeType) -> Optional[NodeType]:
        if isinstance(node, BaseModel):
            return self.visit_BaseModel(node)  # type: ignore[return-value]

        return node

    def visit_list(self, node: List[NodeType]) -> Optional[List[NodeType]]:
        for elem in node:
            self.visit(elem)

        return None

    def visit_dict(self, node: Dict[Key, NodeType]) -> Optional[Dict[Key, NodeType]]:
        for value in node.values():
            self.visit(value)

        return None

    def visit_BaseModel(self, node: ConcreteBaseModel) -> Optional[ConcreteBaseModel]:
        for _, value in node:
            self.visit(value)

        return None


class Transformer(Visitor):
    if TYPE_CHECKING:

        def visit(self, node: NodeType) -> NodeType:
            pass

    def visit_list(self, node: List[NodeType]) -> List[NodeType]:
        return [self.visit(elem) for elem in node]

    def visit_dict(self, node: Dict[Key, NodeType]) -> Dict[Key, NodeType]:
        return {key: self.visit(value) for key, value in node.items()}

    def visit_BaseModel(self, node: ConcreteBaseModel) -> ConcreteBaseModel:
        result: Dict[str, Any] = dict()
        for name, value in node:
            result[name] = self.visit(value)
        return node.copy(update=result)
