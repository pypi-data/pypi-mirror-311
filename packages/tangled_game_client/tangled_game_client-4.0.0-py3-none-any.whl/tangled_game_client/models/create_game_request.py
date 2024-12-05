# coding: utf-8

"""
    Simple Game Service API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 4.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class CreateGameRequest(BaseModel):
    """
    CreateGameRequest
    """ # noqa: E501
    request_id: Optional[StrictStr] = Field(default=None, description="The ID of the request")
    created_by: Optional[StrictStr] = Field(default=None, description="Sub of the user creating the game")
    player_id1: Optional[StrictStr] = Field(default=None, description="The Agent ID of player 1 (default is the player creating the game)")
    player_id2: Optional[StrictStr] = Field(default=None, description="The Agent ID of player 2 (default is the player creating the game)")
    graph_id: Optional[StrictStr] = Field(default=None, description="The ID of the graph")
    vertex_count: StrictInt = Field(description="The number of vertices in the game")
    edges: List[Annotated[List[StrictInt], Field(min_length=2, max_length=2)]] = Field(description="A list of edges (tuples) representing connections between vertices")
    __properties: ClassVar[List[str]] = ["request_id", "created_by", "player_id1", "player_id2", "graph_id", "vertex_count", "edges"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of CreateGameRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if created_by (nullable) is None
        # and model_fields_set contains the field
        if self.created_by is None and "created_by" in self.model_fields_set:
            _dict['created_by'] = None

        # set to None if player_id1 (nullable) is None
        # and model_fields_set contains the field
        if self.player_id1 is None and "player_id1" in self.model_fields_set:
            _dict['player_id1'] = None

        # set to None if player_id2 (nullable) is None
        # and model_fields_set contains the field
        if self.player_id2 is None and "player_id2" in self.model_fields_set:
            _dict['player_id2'] = None

        # set to None if graph_id (nullable) is None
        # and model_fields_set contains the field
        if self.graph_id is None and "graph_id" in self.model_fields_set:
            _dict['graph_id'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateGameRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "request_id": obj.get("request_id"),
            "created_by": obj.get("created_by"),
            "player_id1": obj.get("player_id1"),
            "player_id2": obj.get("player_id2"),
            "graph_id": obj.get("graph_id"),
            "vertex_count": obj.get("vertex_count"),
            "edges": obj.get("edges")
        })
        return _obj


