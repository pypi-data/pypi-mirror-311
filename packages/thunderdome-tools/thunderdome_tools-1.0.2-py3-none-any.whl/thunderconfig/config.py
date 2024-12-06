from dataclasses import dataclass, field
import os
from typing import List, Optional, Dict, Any, Union
import json
from datetime import datetime
from langchain.chat_models import init_chat_model

@dataclass
class APIConfig:
    user_id: str
    user_key: str
    input_text: str  # Input text is now a required parameter
    api_key: Optional[str] = None
    handler: Optional[str] = None  # New field
    agent_auth_token: Optional[str] = None  # New field
    timestamp: Optional[str] = None  # New field, formatted as ISO 8601
    trace_id: Optional[str] = None  # New field
    app: Optional[str] = None
    integration_id: Optional[str] = None
    prompt: Optional[str] = None
    actions: Optional[List[str]] = None
    model: Optional[str] = None
    temperature: Union[int, float, None] = None
    max_tokens: Optional[int] = None
    model_provider: Optional[str] = None
    provider_kwargs: Optional[Dict[str, Any]] = None
    kwargs: Optional[Dict[str, Any]] = None  # Additional kwargs for the payload

    def __post_init__(self):
        if self.timestamp is None:  # Automatically add current timestamp if not provided
            self.timestamp = datetime.utcnow().isoformat()
        self.validate()

    def validate(self):
        # Validate required string fields
        required_string_fields = ['user_id', 'api_key', 'input_text']
        for field_name in required_string_fields:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"'{field_name}' must be a non-empty string.")

        # Validate handler and agent_auth_token
        if self.handler is not None and (not isinstance(self.handler, str) or not self.handler.strip()):
            raise ValueError("'handler' must be a non-empty string.")
        if self.agent_auth_token is not None and (not isinstance(self.agent_auth_token, str) or not self.agent_auth_token.strip()):
            raise ValueError("'agent_auth_token' must be a non-empty string.")

        # Validate trace_id
        if self.trace_id is not None and (not isinstance(self.trace_id, str) or not self.trace_id.strip()):
            raise ValueError("'trace_id' must be a non-empty string.")

        # Validate optional fields if they are provided
        if self.actions is not None:
            if not isinstance(self.actions, list) or not self.actions:
                raise ValueError("'actions' must be a non-empty list of strings.")
            if not all(isinstance(action, str) and action.strip() for action in self.actions):
                raise ValueError("Each action in 'actions' must be a non-empty string.")

        if self.temperature is not None:
            if not isinstance(self.temperature, (int, float)):
                raise ValueError("'temperature' must be a number.")
            if not (0.0 <= self.temperature <= 1.0):
                raise ValueError("'temperature' must be between 0.0 and 1.0.")

        if self.max_tokens is not None:
            if not isinstance(self.max_tokens, int) or self.max_tokens <= 0:
                raise ValueError("'max_tokens' must be a positive integer.")

        if self.provider_kwargs is not None:
            if not isinstance(self.provider_kwargs, dict):
                raise ValueError("'provider_kwargs' must be a dictionary.")

        if self.kwargs is not None:
            if not isinstance(self.kwargs, dict):
                raise ValueError("'kwargs' must be a dictionary.")

    def to_dict(self):
        payload = {
            "config": {
                "user_id": self.user_id,
                "user_key": self.user_key,
                "api_key": self.api_key,
                "app": self.app,
                "integration_id": self.integration_id,
                "prompt": self.prompt,
                "actions": self.actions,
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "model_provider": self.model_provider,
                "provider_kwargs": self.provider_kwargs,
                "handler": self.handler,  # Include new field
                "agent_auth_token": self.agent_auth_token,  # Include new field
                "timestamp": self.timestamp,  # Include new field
                "trace_id": self.trace_id,  # Include new field
            },
            "input": {
                "input_value": self.input_text
            },
            "kwargs": self.kwargs if self.kwargs is not None else {}
        }

        # Remove None values from config
        payload["config"] = {k: v for k, v in payload["config"].items() if v is not None}

        return payload

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def init_llm(self):
        llm_config = {
            "model": self.model,
            "api_key": self.api_key,
            "max_tokens": self.max_tokens,
            "model_provider":self.model_provider,
            "provider_kwargs":self.provider_kwargs,
            "temperature":self.temperature

        }
        filtered_config = {k: v for k, v in llm_config.items() if v is not None}
        try:
            llm = init_chat_model(**filtered_config)
            return llm
        except Exception as e:
            print(f"Error initializing chat model: {e}")
    


class APIConfigBuilder:
    def __init__(self):
        self._config = {}

    def set_user_id(self, user_id: str):
        self._config['user_id'] = user_id
        return self

    def set_user_key(self, user_key: str):
        self._config['user_key'] = user_key
        return self
    
    def set_api_key(self, api_key: str):
        self._config['api_key'] = api_key
        return self

    def set_input_text(self, input_text: str):
        self._config['input_text'] = input_text
        return self

    def set_handler(self, handler: str):  # New method
        self._config['handler'] = handler
        return self

    def set_agent_auth_token(self, agent_auth_token: str):  # New method
        self._config['agent_auth_token'] = agent_auth_token
        return self

    def set_trace_id(self, trace_id: str):  # New method
        self._config['trace_id'] = trace_id
        return self

    def set_timestamp(self, timestamp: str):  # New method
        self._config['timestamp'] = timestamp
        return self

    def set_app(self, app: str):
        self._config['app'] = app
        return self

    def set_integration_id(self, integration_id: str):
        self._config['integration_id'] = integration_id
        return self

    def set_prompt(self, prompt: str):
        self._config['prompt'] = prompt
        return self

    def set_actions(self, actions: List[str]):
        self._config['actions'] = actions
        return self

    def set_model(self, model: str):
        self._config['model'] = model
        return self

    def set_temperature(self, temperature: Union[int, float]):
        self._config['temperature'] = temperature
        return self

    def set_max_tokens(self, max_tokens: int):
        self._config['max_tokens'] = max_tokens
        return self

    def set_model_provider(self, model_provider: str):
        self._config['model_provider'] = model_provider
        return self

    def set_provider_kwargs(self, provider_kwargs: Dict[str, Any]):
        self._config['provider_kwargs'] = provider_kwargs
        return self

    def set_kwargs(self, kwargs: Dict[str, Any]):
        self._config['kwargs'] = kwargs
        return self

    def build(self):
        required_fields = ['user_id', 'api_key', 'input_text']
        for field in required_fields:
            if field not in self._config:
                raise ValueError(f"'{field}' is a required field and must be set.")
        # Automatically set timestamp if not provided
        if 'timestamp' not in self._config:
            self._config['timestamp'] = datetime.utcnow().isoformat()
        return APIConfig(**self._config)

def parse_to_config(agent_input) -> APIConfig:
    required_config_fields = ["user_id", "user_key"]
    required_input_fields = ["input_value"]

    # Check for missing required fields in the input dictionary
    for field in required_input_fields:
        if field not in agent_input['input'] or not agent_input['input']['input_value'].strip():
            raise ValueError(f"Missing required field in 'input': '{field}'")

    # Check for missing required fields in the config dictionary
    for field in required_config_fields:
        if field not in agent_input['config'] or not str(agent_input['config'].get(field, "")).strip():
            raise ValueError(f"Missing required field in 'config': '{field}'")

    # Extract input_value from the AgentInput
    input_value = agent_input['input']['input_value']

    # Extract config from AgentInput
    config = agent_input['config']

    # Dynamically build APIConfig using extracted values
    api_config = APIConfig(
        user_id=config["user_id"],  # Required
        user_key=config.get("user_key", ""),  # Optional
        api_key=config["api_key"],  # Required
        input_text=input_value,  # Required
        handler=config.get("handler"),  # Optional
        agent_auth_token=config.get("agent_auth_token"),  # Optional
        timestamp=config.get("timestamp"),  # Optional
        trace_id=config.get("trace_id"),  # Optional
        app=config.get("app"),  # Optional
        integration_id=config.get("integration_id"),  # Optional
        prompt=config.get("prompt"),  # Optional
        actions=config.get("actions"),  # Optional
        model=config.get("model"),  # Optional
        temperature=config.get("temperature"),  # Optional
        max_tokens=config.get("max_tokens"),  # Optional
        model_provider=config.get("model_provider"),  # Optional
        provider_kwargs=config.get("provider_kwargs"),  # Optional
        kwargs=agent_input['kwargs'] if agent_input['kwargs'] else {},  # Optional
    )
    return api_config

def load_env_variables_to_config(config: APIConfig) -> APIConfig:
    """
    Load environment variables and update the APIConfig object if necessary.

    Args:
        config (APIConfig): The existing configuration object.

    Returns:
        APIConfig: The updated configuration object with values from environment variables.
    """
    # Environment variables to override or set default values
    env_defaults = {
        "api_key": os.getenv("LANGCHAIN_API_KEY"),
        "handler": os.getenv("LANGCHAIN_TRACING_V2", "true"),
        "app": os.getenv("DEFAULT_APP", "GMAIL"),
        "integration_id": os.getenv("DEFAULT_INTEGRATION", "1867d112-4e54-4c25-a589-f418f56b72b7"),
        "prompt": os.getenv("DEFAULT_PROMPT", "You are a helpful assistant."),
        "actions": os.getenv("DEFAULT_ACTIONS", "GMAIL_SEND_EMAIL/GMAIL_FETCH_EMAILS").split("/"),
        "model_provider": os.getenv("DEFAULT_MODEL_PROVIDER", "openai"),
        "model": os.getenv("DEFAULT_MODEL", "gpt-4"),
        "temperature": float(os.getenv("DEFAULT_TEMPERATURE", "0.0")),
        "max_tokens": int(os.getenv("DEFAULT_MAX_TOKENS", "16384")),
        "provider_kwargs": {}
    }

    # OpenAI-specific environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    if openai_api_key:
        env_defaults["provider_kwargs"]["openai_api_key"] = openai_api_key
    if openai_api_base:
        env_defaults["provider_kwargs"]["openai_api_base"] = openai_api_base

    # Azure OpenAI-specific environment variables
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_api_base = os.getenv("AZURE_OPENAI_API_BASE")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    azure_deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
    if azure_api_key:
        env_defaults["provider_kwargs"]["azure_openai_api_key"] = azure_api_key
    if azure_api_base:
        env_defaults["provider_kwargs"]["azure_openai_api_base"] = azure_api_base
    if azure_api_version:
        env_defaults["provider_kwargs"]["azure_openai_api_version"] = azure_api_version
    if azure_deployment_name:
        env_defaults["provider_kwargs"]["azure_deployment_name"] = azure_deployment_name

    # LiteLLM-specific environment variables
    litellm_api_key = os.getenv("LITELLM_API_KEY")
    litellm_server_url = os.getenv("LITELLM_SERVER_URL")
    if litellm_api_key:
        env_defaults["provider_kwargs"]["litellm_api_key"] = litellm_api_key
    if litellm_server_url:
        env_defaults["provider_kwargs"]["litellm_server_url"] = litellm_server_url

    # Update the config object with environment variables if they are not already set
    for key, value in env_defaults.items():
        if getattr(config, key) is None and value is not None:
            setattr(config, key, value)

    return config