# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: config.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

import betterproto


class InferenceLocations(betterproto.Enum):
    CLIENT = 0
    SERVER = 1


@dataclass(eq=False, repr=False)
class Config(betterproto.Message):
    inference_location: "InferenceLocations" = betterproto.enum_field(1)
    evaluation_enabled: bool = betterproto.bool_field(2)
    apply_corrections: bool = betterproto.bool_field(3)
    model: str = betterproto.string_field(4)
    temperature: float = betterproto.float_field(5)
    streaming: bool = betterproto.bool_field(6)
    response_format: str = betterproto.string_field(7)
    stop: Optional[str] = betterproto.string_field(8, optional=True)
    logprobs: bool = betterproto.bool_field(9)
    max_tokens: Optional[int] = betterproto.int64_field(10, optional=True)
    n: int = betterproto.int64_field(11)
    presence_penalty: float = betterproto.double_field(15)
    frequency_penalty: float = betterproto.double_field(16)
    timeout: float = betterproto.double_field(17)
    context_retrieval_enabled: bool = betterproto.bool_field(18)
    fallback_model: Optional[str] = betterproto.string_field(19, optional=True)
    intent_stability: Optional[str] = betterproto.string_field(20, optional=True)
    safe_mode: bool = betterproto.bool_field(21)
    feedback: List[str] = betterproto.string_field(22)


@dataclass(eq=False, repr=False)
class ModelConfig(betterproto.Message):
    all_models: List[str] = betterproto.string_field(1)
    client_models: List[str] = betterproto.string_field(2)
    server_models: List[str] = betterproto.string_field(3)
    default_client_model: str = betterproto.string_field(4)
    default_server_model: str = betterproto.string_field(5)
