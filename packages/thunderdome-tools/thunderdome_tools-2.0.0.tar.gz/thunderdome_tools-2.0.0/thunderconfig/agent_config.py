import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

class InputModel(BaseModel):
    input_value: str = Field(..., description="The main input value for the agent, such as a command or query.")

class ConfigModel(BaseModel):
    user_id: str = Field(..., description="User ID for whom the agent is executed.")
    actions: Optional[List[str]] = Field(None, description="List of actions the agent can perform.")
    app: Optional[str] = Field(None, description="The app for which the agent is configured.")
    integration_id: Optional[str] = Field(None, description="Integration ID for the app.")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for the model.")
    model: Optional[str] = Field(None, description="Model name.")
    model_provider: Optional[str] = Field(None, description="Model provider, e.g., 'openai'.")
    prompt: Optional[str] = Field(None, description="Prompt for the agent.")
    provider_kwargs: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional provider-specific keyword arguments."
    )
    temperature: Optional[float] = Field(None, description="Temperature for the model.")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "user_id": "testing-langserve",
                    "actions": [
                        "GMAIL_SEND_EMAIL",
                        "GMAIL_FETCH_EMAILS"
                    ],
                    "app": "GMAIL",
                    "integration_id": "your_integration_id",
                    "max_tokens": 16384,
                    "model": "gpt-4",
                    "model_provider": "openai",
                    "prompt": "You are a helpful assistant that can perform tasks with the user's email account.",
                    "provider_kwargs": {
                        "openai_api_base": "https://your-custom-openai-endpoint.com/v1",
                        "openai_api_key": "your_override_openai_api_key"
                    },
                    "temperature": 0
                }
            ]
        }

class ThunderInput(BaseModel):
    input: InputModel = Field(..., description="The input message for the agent, containing 'input_value'.")
    config: ConfigModel = Field(..., description="Configuration parameters for the agent.")
    kwargs: Dict = Field({}, description="Additional keyword arguments for the agent.")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "config": {
                        "user_id": "testing-langserve",
                        "actions": [
                            "GMAIL_SEND_EMAIL",
                            "GMAIL_FETCH_EMAILS"
                        ],
                        "app": "GMAIL",
                        "integration_id": "your_integration_id",
                        "max_tokens": 16384,
                        "model": "gpt-4",
                        "model_provider": "openai",
                        "prompt": "You are a helpful assistant that can perform tasks with the user's email account.",
                        "provider_kwargs": {
                            "openai_api_base": "https://your-custom-openai-endpoint.com/v1",
                            "openai_api_key": "your_override_openai_api_key"
                        },
                        "temperature": 0
                    },
                    "input": {
                        "input_value": "Send an email to someone@example.com saying hi"
                    },
                    "kwargs": {}
                }
            ]
        }




# Define Config class
class ThunderConfigHandler:
    def __init__(self, config):
        self.load_defaults()
        self.set_langchain_env_variables()
        self.config = self.process_config(config)

    def load_defaults(self):
        # LangChain configuration
        self.LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY', 'your_default_langchain_api_key')
        self.LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'true')
        self.LANGCHAIN_ENDPOINT = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
        self.LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT', 'default_project')

        # Default model configuration
        self.DEFAULT_MODEL_PROVIDER = os.getenv('DEFAULT_MODEL_PROVIDER', 'openai')
        self.DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gpt-4')
        self.DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', '0.0'))
        self.DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', '16384'))
        self.DEFAULT_APP = os.getenv('DEFAULT_APP', 'GMAIL')
        self.DEFAULT_PROMPT = os.getenv('DEFAULT_PROMPT', 'You are a helpful assistant.')
        self.DEFAULT_ACTIONS = os.getenv('DEFAULT_ACTIONS', 'GMAIL_SEND_EMAIL/GMAIL_FETCH_EMAILS').split('/')
        self.DEFAULT_INTEGRATION = os.getenv('DEFAULT_INTEGRATION', '1867d112-4e54-4c25-a589-f418f56b72b7')

        # OpenAI Environment Variables
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

        # Azure OpenAI Environment Variables
        self.AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
        self.AZURE_OPENAI_API_BASE = os.getenv('AZURE_OPENAI_API_BASE')
        self.AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15')
        self.AZURE_DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME')

        # LiteLLM Environment Variables
        self.LITELLM_API_KEY = os.getenv('LITELLM_API_KEY')
        self.LITELLM_SERVER_URL = os.getenv('LITELLM_SERVER_URL')

    def set_langchain_env_variables(self):
        # Set environment variables for LangChain
        os.environ['LANGCHAIN_API_KEY'] = self.LANGCHAIN_API_KEY
        os.environ['LANGCHAIN_TRACING_V2'] = self.LANGCHAIN_TRACING_V2
        os.environ['LANGCHAIN_ENDPOINT'] = self.LANGCHAIN_ENDPOINT
        os.environ['LANGCHAIN_PROJECT'] = self.LANGCHAIN_PROJECT

    def process_config(self, input_config: ThunderInput) -> Dict[str, Any]:
        self.config = {}

        # User ID
        self.config['user_id'] = input_config.user_id
        if not self.config['user_id']:
            raise ValueError("user_id is required in config or .env")

        # App name
        self.config['app'] = input_config.app or self.DEFAULT_APP

        # Integration ID
        self.config['integration_id'] = input_config.integration_id or self.DEFAULT_INTEGRATION

        # Prompt
        self.config['prompt'] = input_config.prompt or self.DEFAULT_PROMPT

        # Actions
        self.config['actions'] = input_config.actions or self.DEFAULT_ACTIONS

        # Model configuration
        self.config['model'] = input_config.model or self.DEFAULT_MODEL
        self.config['temperature'] = input_config.temperature if input_config.temperature is not None else self.DEFAULT_TEMPERATURE
        self.config['max_tokens'] = input_config.max_tokens or self.DEFAULT_MAX_TOKENS
        self.config['model_provider'] = input_config.model_provider or self.DEFAULT_MODEL_PROVIDER

        # Provider-specific kwargs
        self.config['provider_kwargs'] = input_config.provider_kwargs or {}

        # Merge provider-specific settings
        if self.config['model_provider'].lower() == 'openai':
            self.config['provider_kwargs']['openai_api_key'] = self.config['provider_kwargs'].get('openai_api_key', self.OPENAI_API_KEY)
            self.config['provider_kwargs']['openai_api_base'] = self.config['provider_kwargs'].get('openai_api_base', self.OPENAI_API_BASE)
        elif self.config['model_provider'].lower() == 'azure':
            self.config['provider_kwargs']['azure_api_key'] = self.config['provider_kwargs'].get('azure_api_key', self.AZURE_OPENAI_API_KEY)
            self.config['provider_kwargs']['azure_api_base'] = self.config['provider_kwargs'].get('azure_api_base', self.AZURE_OPENAI_API_BASE)
            self.config['provider_kwargs']['azure_api_version'] = self.config['provider_kwargs'].get('azure_api_version', self.AZURE_OPENAI_API_VERSION)
            self.config['provider_kwargs']['azure_deployment_name'] = self.config['provider_kwargs'].get('azure_deployment_name', self.AZURE_DEPLOYMENT_NAME or self.config['model'])
        elif self.config['model_provider'].lower() == 'litellm':
            self.config['provider_kwargs']['litellm_api_key'] = self.config['provider_kwargs'].get('litellm_api_key', self.LITELLM_API_KEY)
            self.config['provider_kwargs']['litellm_server_url'] = self.config['provider_kwargs'].get('litellm_server_url', self.LITELLM_SERVER_URL)
        else:
            raise ValueError(f"Model provider {self.config['model_provider']} is not supported.")

        return self.config

    def init_llm(self):
        # Build the initial llm_config dictionary
        llm_config = {
            "model": self.config['model'],
            "max_tokens": self.config['max_tokens'],
            "model_provider": self.config['model_provider'],
            "temperature": self.config['temperature']
        }

        # Extract provider_kwargs and remove it from llm_config
        provider_kwargs = self.config.get('provider_kwargs', {})

        # Filter out None values from llm_config
        filtered_config = {k: v for k, v in llm_config.items() if v is not None}

        # Unpack provider_kwargs into filtered_config
        if provider_kwargs:
            if isinstance(provider_kwargs, dict):
                filtered_config.update(provider_kwargs)
            else:
                raise ValueError("provider_kwargs must be a dictionary")

        print("Final LLM Configuration:", filtered_config)

        # Initialize the chat model
        try:
            llm = init_chat_model(**filtered_config)
            return llm
        except Exception as e:
            print(f"Error initializing chat model: {e}")
            raise

