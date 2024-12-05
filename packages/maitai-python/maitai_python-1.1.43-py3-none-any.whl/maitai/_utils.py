import functools
import inspect
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

import openai
import openai.types.chat as openai_types
from betterproto import Casing
from openai.types import ChatModel
from pydantic.json_schema import GenerateJsonSchema

import maitai_gen.chat as chat_types
from maitai._types import ToolFunction
from maitai.tools import Tools
from maitai_common.version import version

__version__ = f"{version}_python_{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

CallableT = TypeVar("CallableT", bound=Callable[..., Any])


class OpenAISchemaGenerator(GenerateJsonSchema):
    def generate(self, schema, mode="validation") -> dict:
        json_schema = super().generate(schema, mode=mode)

        # Inline the referenced objects
        def resolve_refs(obj):
            if isinstance(obj, dict):
                if "$ref" in obj and obj["$ref"].startswith("#/$defs/"):
                    ref_name = obj["$ref"].split("/")[-1]
                    return resolve_refs(json_schema.get("$defs", {}).get(ref_name, {}))
                return {k: resolve_refs(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [resolve_refs(item) for item in obj]
            return obj

        properties = resolve_refs(json_schema["properties"])

        return {
            "name": schema.get("title", "").lower() + "_schema",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": properties,
                "required": json_schema.get("required", []),
                "additionalProperties": False,
            },
        }


def required_args(*variants: Sequence[str]) -> Callable[[CallableT], CallableT]:
    def inner(func: CallableT) -> CallableT:
        params = inspect.signature(func).parameters
        positional = [
            name
            for name, param in params.items()
            if param.kind
            in {
                param.POSITIONAL_ONLY,
                param.POSITIONAL_OR_KEYWORD,
            }
        ]

        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            given_params: set[str] = set()
            for i, _ in enumerate(args):
                try:
                    given_params.add(positional[i])
                except IndexError:
                    raise TypeError(
                        f"{func.__name__}() takes {len(positional)} argument(s) but {len(args)} were given"
                    ) from None

            for key in kwargs.keys():
                given_params.add(key)

            for variant in variants:
                matches = all((param in given_params for param in variant))
                if matches:
                    break
            else:  # no break
                if len(variants) > 1:
                    variations = human_join(
                        [
                            "("
                            + human_join([quote(arg) for arg in variant], final="and")
                            + ")"
                            for variant in variants
                        ]
                    )
                    msg = f"Missing required arguments; Expected either {variations} arguments to be given"
                else:
                    assert len(variants) > 0

                    # TODO: this error message is not deterministic
                    missing = list(set(variants[0]) - given_params)
                    if len(missing) > 1:
                        msg = f"Missing required arguments: {human_join([quote(arg) for arg in missing])}"
                    else:
                        msg = f"Missing required argument: {quote(missing[0])}"
                raise TypeError(msg)
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return inner


# copied from https://github.com/Rapptz/RoboDanny
def human_join(seq: Sequence[str], *, delim: str = ", ", final: str = "or") -> str:
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


def quote(string: str) -> str:
    """Add single quotation marks around the given string. Does *not* do any escaping."""
    return f"'{string}'"


def convert_openai_chat_completion(
    chat: openai_types.ChatCompletion,
) -> chat_types.ChatCompletionResponse:
    return chat_types.ChatCompletionResponse().from_dict(chat.to_dict())


def convert_open_ai_chat_completion_chunk(
    chunk: openai_types.ChatCompletionChunk,
) -> chat_types.ChatCompletionChunk:
    return chat_types.ChatCompletionChunk().from_dict(chunk.to_dict())


def get_chat_completion_params(
    *,
    messages: Iterable[openai_types.ChatCompletionMessageParam],
    model: Union[str, ChatModel],
    frequency_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    logit_bias: Union[Optional[Dict[str, int]], openai.NotGiven] = openai.NOT_GIVEN,
    logprobs: Union[Optional[bool], openai.NotGiven] = openai.NOT_GIVEN,
    max_tokens: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    n: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    presence_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    response_format: Union[
        openai_types.completion_create_params.ResponseFormat,
        chat_types.ResponseFormat,
        openai.NotGiven,
    ] = openai.NOT_GIVEN,
    seed: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    stop: Union[Union[Optional[str], List[str]], openai.NotGiven] = openai.NOT_GIVEN,
    stream: Optional[bool] = False,
    stream_options: Union[
        Optional[openai_types.ChatCompletionStreamOptionsParam], openai.NotGiven
    ] = openai.NOT_GIVEN,
    temperature: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    tool_choice: Union[
        openai_types.ChatCompletionToolChoiceOptionParam, openai.NotGiven
    ] = openai.NOT_GIVEN,
    tools: Union[
        Iterable[Union[openai_types.ChatCompletionToolParam, ToolFunction]],
        openai.NotGiven,
    ] = openai.NOT_GIVEN,
    top_logprobs: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
    top_p: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
    user: Union[str, openai.NotGiven] = openai.NOT_GIVEN,
    parallel_tool_calls: Union[bool, openai.NotGiven] = openai.NOT_GIVEN,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    params = {
        "messages": [msg for msg in messages],
        "model": model,
        "stream": stream,
    }

    if not extra_headers:
        extra_headers = {}

    # Define all optional parameters in a dictionary
    optional_params = {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stop": stop,
        "logprobs": logprobs,
        "top_logprobs": top_logprobs,
        "n": n,
        "seed": seed,
        "logit_bias": logit_bias,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "user": user,
        "tool_choice": tool_choice,
        "parallel_tool_calls": parallel_tool_calls,
        "extra_headers": extra_headers,
    }

    # Add non-NOT_GIVEN params to the dict
    for param_name, value in optional_params.items():
        if value != openai.NOT_GIVEN:
            params[param_name] = value

    if stream_options != openai.NOT_GIVEN and stream_options:
        params["stream_options"] = {
            "include_usage": stream_options.get("include_usage")
        }

    if response_format != openai.NOT_GIVEN:
        if hasattr(response_format, "model_json_schema"):
            response_format = {
                "type": "json_schema",
                "json_schema": response_format.model_json_schema(
                    schema_generator=OpenAISchemaGenerator, mode="serialization"
                ),
            }
        params["response_format"] = {"type": response_format["type"]}
        if response_format.get("json_schema"):
            params["response_format"]["json_schema"] = response_format["json_schema"]

    if tools != openai.NOT_GIVEN:
        params["tools"] = []
        if isinstance(tools, Tools):
            params["tools"] = [tool.to_dict() for tool in tools.get_tool_definitions()]
        elif tools:
            for tool in tools:
                if hasattr(tool, "__tool__"):
                    params["tools"].append(tool.__tool__.to_dict())
                    continue

                tool_dict = {"type": tool["type"]}
                function = tool.get("function", {})

                properties = {}
                for prop_name, prop_value in (
                    function.get("parameters", {}).get("properties", {}).items()
                ):
                    if isinstance(prop_value, dict):
                        prop_dict = {
                            "type": prop_value.get("type"),
                            "description": prop_value.get("description"),
                        }
                        if prop_value.get("items"):
                            prop_dict["items"] = prop_value["items"]
                        properties[prop_name] = prop_dict
                    else:
                        properties[prop_name] = prop_value

                parameters = {}
                if function.get("parameters"):
                    parameters = {
                        "type": function["parameters"].get("type", ""),
                        "properties": properties,
                        "required": function["parameters"].get("required", []),
                        "additional_properties": function["parameters"].get(
                            "additional_properties", False
                        ),
                        "enum": function["parameters"].get("enum", []),
                    }

                tool_dict["function"] = {
                    "name": function.get("name"),
                    "description": function.get("description"),
                    "parameters": parameters,
                    "strict": function.get("strict", False),
                }
                params["tools"].append(tool_dict)

    return params


def chat_completion_chunk_to_response(
    final_chunk: chat_types.ChatCompletionChunk,
    content: Union[str, List[chat_types.ChatMessage]],
):
    chat_completion_response = chat_types.ChatCompletionResponse().from_dict(
        final_chunk.to_dict(casing=Casing.SNAKE)
    )
    if isinstance(content, str):
        chat_completion_response.choices[0].message = chat_types.ChatMessage(
            role="assistant", content=content
        )
    if isinstance(content, List):
        chat_completion_response.choices[0].message = content[-1]
    if isinstance(chat_completion_response.choices[0].message, dict):
        chat_completion_response.choices[
            0
        ].message = chat_types.ChatMessage().from_dict(
            chat_completion_response.choices[0].message
        )
    return chat_completion_response
