from abc import abstractmethod
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Generator,
    Generic,
    Literal,
    Optional,
    TypeVar,
    overload,
)

from openai import NOT_GIVEN, NotGiven

from adapters.abstract_adapters.api_key_adapter_mixin import ApiKeyAdapterMixin
from adapters.abstract_adapters.base_adapter import BaseAdapter
from adapters.abstract_adapters.provider_adapter_mixin import ProviderAdapterMixin
from adapters.client_cache import client_cache
from adapters.constants import OVERRIDE_ALL_BASE_URLS
from adapters.general_utils import (
    EMPTY_CONTENT,
    delete_none_values,
    stream_generator_auto_close,
)
from adapters.types import (
    AdapterChatCompletion,
    AdapterChatCompletionChunk,
    AdapterException,
    AdapterStreamAsyncChatCompletion,
    AdapterStreamSyncChatCompletion,
    ContentTurn,
    ContentType,
    Conversation,
    ConversationRole,
    Model,
    ModelProperties,
)

CLIENT_SYNC = TypeVar("CLIENT_SYNC")
CLIENT_ASYNC = TypeVar("CLIENT_ASYNC")


class SDKChatAdapter(
    BaseAdapter,
    ApiKeyAdapterMixin,
    ProviderAdapterMixin,
    Generic[CLIENT_SYNC, CLIENT_ASYNC],
):
    _client_sync: CLIENT_SYNC
    _client_async: CLIENT_ASYNC

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._setup_clients(self.get_api_key())

    def _get_or_create_client(
        self, api_key: str, client_type: Literal["sync", "async"]
    ) -> Any:
        base_url = OVERRIDE_ALL_BASE_URLS or self.get_base_sdk_url()
        client = client_cache.get_client(base_url, api_key, client_type)
        if not client:
            client = getattr(self, f"_create_client_{client_type}")(
                api_key=api_key, base_url=base_url
            )
            client_cache.set_client(base_url, api_key, client_type, client)
        return client

    def _setup_clients(self, api_key: str) -> None:
        self._client_sync = self._get_or_create_client(api_key, "sync")
        self._client_async = self._get_or_create_client(api_key, "async")

    @abstractmethod
    def _call_sync(self) -> Callable[..., Any]:
        pass

    @abstractmethod
    def _call_async(self) -> Callable[..., Any]:
        pass

    @abstractmethod
    def _create_client_sync(self, base_url: str, api_key: str) -> CLIENT_SYNC:
        pass

    @abstractmethod
    def _create_client_async(self, base_url: str, api_key: str) -> CLIENT_ASYNC:
        pass

    @abstractmethod
    def get_base_sdk_url(self) -> str:
        pass

    @abstractmethod
    def _extract_response(self, request: Any, response: Any) -> AdapterChatCompletion:
        pass

    @abstractmethod
    def _extract_stream_response(
        self, request: Any, response: Any, state: dict[str, Any]
    ) -> AdapterChatCompletionChunk:
        pass

    def _adjust_temperature(self, temperature: float) -> float:
        return temperature

    # pylint: disable=too-many-statements
    def _get_params(self, llm_input: Conversation, **kwargs: Any) -> Dict[str, Any]:
        if kwargs.get("stream") == NOT_GIVEN:
            kwargs["stream"] = False

        if (
            kwargs.get("tool_choices") is not None
            and self.get_model().supports_tool_choice is False
        ):
            raise AdapterException(
                f"Tool choice is not supported on {self.get_model().name}"
            )

        if (
            kwargs.get("temperature") is not None
            and self.get_model().supports_temperature is False
        ):
            del kwargs["temperature"]

        completion_length = self.get_model().completion_length
        if (
            kwargs.get("max_tokens")
            and completion_length
            and kwargs.get("max_tokens", 0) > completion_length
        ):
            raise AdapterException(
                f"max_tokens {kwargs.get('max_tokens')} should be less than max completion length {completion_length} for {self.get_model().name}"
            )

        if (
            self.get_model().supports_streaming is False
            and kwargs.get("stream") is True
        ):
            raise AdapterException(
                f"Streaming is not supported on {self.get_model().name}"
            )

        if self.get_model().supports_user is False and "user" in kwargs:
            del kwargs["user"]

        if self.get_model().supports_functions is False and "functions" in kwargs:
            raise AdapterException(
                f"Function calling is not supported on {self.get_model().name}"
            )

        if self.get_model().supports_tools is False and "tools" in kwargs:
            raise AdapterException(f"Tools is not supported on {self.get_model().name}")

        if self.get_model().supports_n is False and "n" in kwargs and kwargs["n"] >= 1:
            if kwargs["n"] == 1:
                del kwargs["n"]
            else:
                raise AdapterException(f"n is not supported on {self.get_model().name}")

        if self.get_model().supports_vision is False:
            for turn in llm_input.turns:
                if isinstance(turn, ContentTurn):
                    for content in turn.content:
                        if content.type == ContentType.image_url:
                            raise AdapterException(
                                f"Image input is not supported on {self.get_model().name}"
                            )

        if (
            self.get_model().supports_json_output is False
            and "response_format" in kwargs
            and kwargs["response_format"]["type"] == "json_object"
        ):
            raise AdapterException(
                f"JSON response format is not supported on {self.get_model().name}"
            )

        messages = [turn.model_dump() for turn in llm_input.turns]

        # ====

        if (
            not self.get_model().supports_only_assistant
            and len(messages)
            and messages[0]["role"] == ConversationRole.assistant.value
        ):
            messages.append(
                {"role": ConversationRole.user.value, "content": EMPTY_CONTENT}
            )

        if (
            not self.get_model().supports_only_system
            and len(messages)
            and messages[0]["role"] == ConversationRole.system.value
        ):
            messages.append(
                {"role": ConversationRole.user.value, "content": EMPTY_CONTENT}
            )

        # Convert json content to string if not supported
        if not self.get_model().supports_json_content:
            for message in messages:
                if "content" in message and isinstance(message["content"], list):
                    message["content"] = "\n".join(
                        [
                            content["text"]
                            for content in message["content"]
                            if "text" in content
                        ]
                    )

        # Convert empty string to EMPTY_CONTENT if not supported
        if not self.get_model().supports_empty_content:
            for message in messages:
                if (
                    isinstance(message["content"], str)
                    and message["content"].strip() == ""
                ):
                    message["content"] = EMPTY_CONTENT
                elif isinstance(message["content"], list):
                    for content in message["content"]:
                        if (
                            isinstance(content, dict)
                            and "text" in content
                            and content["text"].strip() == ""
                        ):
                            content["text"] = EMPTY_CONTENT

        # Change system prompt roles to assistant
        if not self.get_model().supports_multiple_system:
            for message in messages[1:]:
                if message["role"] == ConversationRole.system.value:
                    message["role"] = ConversationRole.assistant.value

        # Change system prompt roles to user
        if not self.get_model().supports_system:
            for message in messages:
                if message["role"] == ConversationRole.system.value:
                    message["role"] = ConversationRole.user.value

        # Join messages from the same role
        if not self.get_model().supports_repeating_roles:
            result: list[Any] = []
            current_role = None
            current_content: list[Any] = []

            for message in messages:
                role = message["role"]

                # If the role changes, save the concatenated content and start a new group
                if role != current_role:
                    if current_role is not None:
                        result.append(
                            {"role": current_role, "content": " ".join(current_content)}
                        )

                        # Check if a "system" message is between two "user" messages
                        if (
                            current_role == "system"
                            and len(result) > 1
                            and result[-2]["role"] == "user"
                            and role == "user"
                        ):
                            result.append(
                                {"role": "assistant", "content": EMPTY_CONTENT}
                            )

                    current_role = role
                    current_content = []

                # Append content to the current group
                current_content.append(message["content"])

            # Add the last group to the result
            if current_content:
                result.append(
                    {"role": current_role, "content": " ".join(current_content)}
                )

            messages = result

        # If the last message is assistant, add an empty user message
        if (
            self.get_model().supports_first_assistant is False
            and messages[0]["role"] == ConversationRole.assistant.value
        ):
            messages.insert(
                0, {"role": ConversationRole.user.value, "content": EMPTY_CONTENT}
            )

            # If the first message is assistant, add an empty user message
        if (
            self.get_model().supports_last_assistant is False
            and messages[-1]["role"] == ConversationRole.assistant.value
        ):
            messages.append(
                {"role": ConversationRole.user.value, "content": EMPTY_CONTENT}
            )

        # ====

        return {
            "messages": messages,
            **(
                {"temperature": self._adjust_temperature(kwargs.get("temperature", 1))}
                if kwargs.get("temperature") is not None
                else {}
            ),
            **kwargs,
        }

    def get_model(self) -> Model:
        if self._current_model is None:
            raise ValueError("Model is not set")
        return self._current_model

    def get_model_properteis(self, model_name: str) -> ModelProperties:
        for model in self.get_supported_models():
            if model.name == model_name:
                return model.properties
        raise ValueError(f"Model {model_name} not found")

    def set_api_key(self, api_key: str) -> None:
        super().set_api_key(api_key)
        self._setup_clients(api_key)

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
        params = self._get_params(llm_input, stream=stream, **kwargs)

        response = await self._call_async()(
            model=self.get_model()._get_api_path(),
            **delete_none_values(params),
        )

        if not stream:
            return self._extract_response(request=llm_input, response=response)

        async def stream_response() -> AsyncGenerator[AdapterChatCompletionChunk, None]:
            state: dict[str, Any] = {}
            async with stream_generator_auto_close(response):
                try:
                    async for chunk in response:
                        yield self._extract_stream_response(
                            request=llm_input, response=chunk, state=state
                        )
                except Exception as e:
                    raise AdapterException(f"Error in streaming response: {e}") from e
                finally:
                    if hasattr(response, "close"):
                        await response.close()
                    # elif hasattr(response, "aclose"):  # For Cohere SDK
                    # await response.aclose()

        return AdapterStreamAsyncChatCompletion(response=stream_response())

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
        params = self._get_params(llm_input, stream=stream, **kwargs)

        response = self._call_sync()(
            model=self.get_model()._get_api_path(),
            **delete_none_values(params),
        )

        if not stream:
            return self._extract_response(request=llm_input, response=response)

        def stream_response() -> Generator[AdapterChatCompletionChunk, Any, None]:
            state: dict[str, Any] = {}
            try:
                for chunk in response:
                    yield self._extract_stream_response(
                        request=llm_input, response=chunk, state=state
                    )
            except Exception as e:
                raise AdapterException(f"Error in streaming response: {e}") from e
            finally:
                response.close()

        return AdapterStreamSyncChatCompletion(response=stream_response())
