import time
from typing import Any, Dict, Literal, Optional, overload
import uuid

from google.ai.generativelanguage import (
    GenerateContentResponse,
    GenerativeServiceAsyncClient,
    GenerativeServiceClient,
)
from google.api_core.client_options import ClientOptions
import google.generativeai as genai
from google.generativeai.types.generation_types import AsyncGenerateContentResponse
from openai import NOT_GIVEN, NotGiven
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from adapters.abstract_adapters.sdk_chat_adapter import SDKChatAdapter
from adapters.general_utils import get_dynamic_cost
from adapters.types import (
    AdapterChatCompletion,
    AdapterStreamAsyncChatCompletion,
    AdapterStreamSyncChatCompletion,
    Conversation,
    ConversationRole,
    Cost,
    Model,
    ModelProperties,
    Provider,
    Turn,
    Vendor,
)


class GeminiModel(Model):
    provider_name: str = Provider.gemini.value
    vendor_name: str = Vendor.gemini.value

    properties: ModelProperties = ModelProperties(gdpr_compliant=True)


MODELS: list[Model] = [
    GeminiModel(
        name="gemini-1.0-pro",
        cost=Cost(prompt=0.5e-6, completion=1.5e-6),
        context_length=30720,
        completion_length=2048,
    ),
    GeminiModel(
        name="gemini-1.5-pro",
        cost=Cost(prompt=3.5e-6, completion=10.5e-6),
        context_length=128000,
        completion_length=8192,
    ),
    GeminiModel(
        name="gemini-1.5-flash",
        cost=Cost(prompt=0.35e-6, completion=0.70e-6),
        context_length=128000,
        completion_length=8192,
    ),
]


# TODO: max_tokens doesnt work
class GeminiSDKChatProviderAdapter(
    SDKChatAdapter[GenerativeServiceClient, GenerativeServiceAsyncClient]
):
    @staticmethod
    def get_supported_models() -> list[Model]:
        return MODELS

    @staticmethod
    def get_api_key_name() -> str:
        return "GEMINI_API_KEY"

    def get_base_sdk_url(self) -> str:
        return ""

    def __init__(self) -> None:
        self.model: genai.GenerativeModel | None = None
        super().__init__()

    def get_model_name(self) -> str:
        if self._current_model is None:
            raise ValueError("Model not set")
        return self._current_model.name

    def _call_sync(self) -> Any:
        return self._client_sync

    def _call_async(self) -> Any:
        return self._client_async

    def _create_client_sync(
        self, base_url: str, api_key: str
    ) -> GenerativeServiceClient:
        return GenerativeServiceClient(
            client_options=ClientOptions(api_key=api_key), transport="rest"
        )

    def _create_client_async(
        self, base_url: str, api_key: str
    ) -> GenerativeServiceAsyncClient:
        return GenerativeServiceAsyncClient(
            client_options=ClientOptions(api_key=api_key), transport="rest"
        )

    def _adjust_temperature(self, temperature: float) -> float:
        return temperature / 2

    def _extract_response(
        self,
        request: Any,
        response: GenerateContentResponse,
    ) -> AdapterChatCompletion:
        choices: list[Choice] = []

        for candidate in response.candidates:
            choices.append(
                Choice(
                    message=ChatCompletionMessage(
                        role=ConversationRole.assistant.value,
                        content=response.text,
                    ),
                    finish_reason="stop",
                    index=candidate.index,
                )
            )

        usage = CompletionUsage(
            prompt_tokens=response.usage_metadata.prompt_token_count,
            completion_tokens=response.usage_metadata.candidates_token_count,
            total_tokens=response.usage_metadata.prompt_token_count
            + response.usage_metadata.candidates_token_count,
        )

        dynamic_cost = get_dynamic_cost(self.get_model_name(), usage.prompt_tokens)
        cost = (
            dynamic_cost.prompt * usage.prompt_tokens
            + dynamic_cost.completion * usage.completion_tokens
            + self.get_model().cost.request
        )

        return AdapterChatCompletion(
            id=str(uuid.uuid4()),
            created=int(time.time()),
            model=self.get_model().name,
            object="chat.completion",
            cost=cost,
            usage=usage,
            choices=choices,
            # Deprecated
            response=Turn(
                role=ConversationRole.assistant,
                content=choices[0].message.content or "",
            ),
            token_counts=Cost(
                prompt=usage.prompt_tokens,
                completion=usage.completion_tokens,
                request=self.get_model().cost.request,
            ),
        )

    async def _extract_response_async(
        self,
        request: Any,  # pylint: disable=unused-argument
        response: AsyncGenerateContentResponse,
    ) -> AdapterChatCompletion:
        choices: list[Choice] = []

        for candidate in response.candidates:
            choices.append(
                Choice(
                    message=ChatCompletionMessage(
                        role=ConversationRole.assistant.value,
                        content=response.text,
                    ),
                    finish_reason="stop",
                    index=candidate.index,
                )
            )

        usage = CompletionUsage(
            prompt_tokens=response.usage_metadata.prompt_token_count,
            completion_tokens=response.usage_metadata.candidates_token_count,
            total_tokens=response.usage_metadata.prompt_token_count
            + response.usage_metadata.candidates_token_count,
        )

        dynamic_cost = get_dynamic_cost(self.get_model_name(), usage.prompt_tokens)
        cost = (
            dynamic_cost.prompt * usage.prompt_tokens
            + dynamic_cost.completion * usage.completion_tokens
            + self.get_model().cost.request
        )

        return AdapterChatCompletion(
            id=str(uuid.uuid4()),
            created=int(time.time()),
            model=self.get_model().name,
            object="chat.completion",
            cost=cost,
            usage=usage,
            choices=choices,
            # Deprecated
            response=Turn(
                role=ConversationRole.assistant,
                content=choices[0].message.content or "",
            ),
            token_counts=Cost(
                prompt=usage.prompt_tokens,
                completion=usage.completion_tokens,
                request=self.get_model().cost.request,
            ),
        )

    def _extract_stream_response(
        self, request: Any, response: Any, state: dict[str, Any]
    ) -> Any:
        return response

    def _get_params(
        self,
        llm_input: Conversation,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        params = super()._get_params(llm_input, **kwargs)

        last_message = params["messages"].pop()
        last_content = last_message["content"] or " "

        transformed_messages = []
        for message in params["messages"]:
            transformed_message = {
                "parts": [_map_content_to_str(message["content"], message["role"])],
                "role": _map_role(message["role"]),
            }
            transformed_messages.append(transformed_message)

        if "max_tokens" in params:
            params["max_output_tokens"] = params["max_tokens"]
            del params["max_tokens"]

        del params["messages"]

        return {
            "config": params,
            "history": transformed_messages,
            "prompt": _map_content_to_str(last_content, last_message["role"]),
        }

    @overload
    async def execute_async(
        self,
        llm_input: Conversation,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        **kwargs: Any,
    ) -> AdapterChatCompletion: ...

    @overload
    async def execute_async(
        self,
        llm_input: Conversation,
        stream: Literal[True],
        **kwargs: Any,
    ) -> AdapterStreamAsyncChatCompletion: ...

    async def execute_async(
        self,
        llm_input: Conversation,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        **kwargs: Any,
    ) -> AdapterChatCompletion | AdapterStreamAsyncChatCompletion:
        params = self._get_params(llm_input, **kwargs)

        model = genai.GenerativeModel(
            model_name=self.get_model_name(),
            generation_config=params["config"],
        )
        model._async_client = self._call_async()

        convo = model.start_chat(history=params["history"])

        result = await convo.send_message_async(params["prompt"])

        return await self._extract_response_async(request=llm_input, response=result)

    @overload
    def execute_sync(
        self,
        llm_input: Conversation,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        **kwargs: Any,
    ) -> AdapterChatCompletion: ...

    @overload
    def execute_sync(
        self,
        llm_input: Conversation,
        stream: Literal[True],
        **kwargs: Any,
    ) -> AdapterStreamSyncChatCompletion: ...

    def execute_sync(
        self,
        llm_input: Conversation,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        **kwargs: Any,
    ) -> AdapterChatCompletion | AdapterStreamSyncChatCompletion:
        params = self._get_params(llm_input, **kwargs)

        self.model = genai.GenerativeModel(
            model_name=self.get_model_name(),
            generation_config=params.get("config") or None,
        )
        self.model._client = self._call_sync()

        chat = self.model.start_chat(history=params["history"])
        result = chat.send_message(params["prompt"])
        return self._extract_response(request=llm_input, response=result)


def _map_content_to_str(
    content: str | list[dict[str, Any]], role: str | ConversationRole
) -> str:
    if not content or content in [" ", "\n", "\t"]:
        return "."

    if isinstance(content, list):
        return " ".join(content.get("text", "") for content in content)

    if role != "system":
        return content

    return f"*{content}*"


def _map_role(role: str | ConversationRole) -> str:
    match role:
        case ConversationRole.user | ConversationRole.system | "user" | "system":
            return "user"
        case ConversationRole.assistant | "assistant":
            return "model"
        case _:
            return "user"
