import json
from datetime import datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, Field, field_serializer
from pydantic.types import Json

from emp_agents.types.enums import Role


class Function(BaseModel):
    name: str
    arguments: Json[Any]

    @field_serializer("arguments")
    def serialize_dt(self, dt: datetime, _info):
        return json.dumps(self.arguments)


class ToolCall(BaseModel):
    id: str
    type: str
    function: Function

    def __repr__(self):
        return f"<ToolCall function={self.function}>"


class Message(BaseModel):
    role: Role
    content: str | None
    tool_call_id: str | None = Field(
        default=None, validation_alias=AliasChoices("tool_call_id")
    )  # given to user in response
    refusal: str | None = Field(default=None)
    tool_calls: list[ToolCall] | None = Field(default=None)  # only in response

    @classmethod
    def build(
        self,
        content: str,
        role: Role = Role.user,
        tool_call_id: str | None = None,
        tool_calls: list[Any] | None = None,
    ):
        return Message(
            content=content,
            role=role,
            tool_calls=tool_calls,
            tool_call_id=tool_call_id,
        )

    def serialize_anthropic(self) -> dict[str, Any]:
        data: dict[str, Any] = {"role": self.role}
        data["content"] = [{"type": "text", "text": self.content}]
        return data

    def __repr__(self):
        if self.content:
            return f"{self.role.value}: {self.content}"
        return f"{self.role.value}: {self.tool_calls}"

    __str__ = __repr__
