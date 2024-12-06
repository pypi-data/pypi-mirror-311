### Updated Documentation for ThunderTools

# ThunderTools

**ThunderTools** is a Python package designed to streamline development and provide consistent, reusable tools for projects like Thunderdome. It includes utilities for API configuration, validation, and interaction with external systems, promoting efficient and standardized workflows.

---

## Tools in ThunderTools

1. **API Config Maker or ThunderConfig**
   - A comprehensive utility for creating, validating, and serializing API configurations.
   - Supports environment variable integration for dynamic and flexible configuration management.
   - Enables seamless integration with machine learning models, external APIs, and custom workflows.

---

## Installation

Install ThunderTools using pip:

```bash
pip install thunderdome-tools
```

---

## Tool: API Config Maker or ThunderConfig

The **API Config Maker** in ThunderTools provides a robust and extensible framework for creating API configurations. It includes advanced features like validation, environment variable support, and integration with machine learning models.

### Key Features

- **Validation**: Enforces data integrity with checks for required fields and value constraints.
- **Serialization**: Converts configurations to dictionary or JSON formats for compatibility with various systems.
- **Builder Pattern**: Facilitates easy configuration creation through a chainable interface.
- **Environment Variable Integration**: Dynamically populates configuration fields from environment variables.
- **Machine Learning Support**: Simplifies initialization and interaction with chat models using pre-built configurations.
- **Expanded Optional Fields**: Includes additional fields like `handler`, `agent_auth_token`, `timestamp`, and `trace_id` for enhanced flexibility.

---

### Usage

#### Importing the API Config Maker

To use the API Config Maker, import it from ThunderTools:

```python
from thundertools.config import APIConfig, APIConfigBuilder
```

#### Using `APIConfig`

Directly create an `APIConfig` object by providing the required parameters and any additional optional parameters:

```python
from thundertools.config import APIConfig

config = APIConfig(
    user_id="12345",
    user_key="my_user_key",
    api_key="my_api_key",
    input_text="Hello, world!",
    handler="MyHandler",
    agent_auth_token="secure_token",
    trace_id="trace_12345"
)

print(config.to_json())
```

#### Using `APIConfigBuilder`

The builder pattern allows for a more flexible and readable way to construct configuration objects:

```python
from thundertools.config import APIConfigBuilder

config = (
    APIConfigBuilder()
    .set_user_id("12345")
    .set_user_key("my_user_key")
    .set_api_key("my_api_key")
    .set_input_text("Hello, world!")
    .set_handler("MyHandler")
    .set_agent_auth_token("secure_token")
    .set_trace_id("trace_12345")
    .build()
)

print(config.to_dict())
```

---

### Environment Variable Integration

Leverage environment variables to populate configuration fields dynamically. The `load_env_variables_to_config` function enriches the `APIConfig` object with values from the environment.

#### Example Usage:

```python
from thundertools.config import APIConfig, load_env_variables_to_config

config = APIConfig(
    user_id="12345",
    user_key="my_user_key",
    input_text="Hello, world!",
    api_key=None  # Intentionally left empty to load from environment
)

config = load_env_variables_to_config(config)

print(config.to_dict())
```

Environment variables used:

- `LANGCHAIN_API_KEY`
- `LANGCHAIN_TRACING_V2`
- `DEFAULT_APP`
- `DEFAULT_INTEGRATION`
- `DEFAULT_PROMPT`
- `DEFAULT_ACTIONS`
- `DEFAULT_MODEL_PROVIDER`
- `DEFAULT_MODEL`
- `DEFAULT_TEMPERATURE`
- `DEFAULT_MAX_TOKENS`
- Provider-specific keys for OpenAI, Azure OpenAI, and LiteLLM.

---

### APIConfig Class Reference

| Parameter          | Type                   | Description                                                  |
| ------------------ | ---------------------- | ------------------------------------------------------------ |
| `user_id`          | `str` (required)       | Unique identifier for the user.                              |
| `user_key`         | `str` (required)       | Key specific to the user for authentication.                 |
| `api_key`          | `str` (required)       | API key for authentication.                                  |
| `input_text`       | `str` (required)       | The primary input or payload text for the API.               |
| `handler`          | `str` (optional)       | The handler associated with the configuration.               |
| `agent_auth_token` | `str` (optional)       | Authentication token for the agent.                          |
| `timestamp`        | `str` (optional)       | ISO 8601 timestamp. Automatically set if not provided.       |
| `trace_id`         | `str` (optional)       | Trace identifier for tracking requests.                      |
| `app`              | `str` (optional)       | The application initiating the request.                      |
| `integration_id`   | `str` (optional)       | Integration ID for external services.                        |
| `prompt`           | `str` (optional)       | A prompt string for the API.                                 |
| `actions`          | `list[str]` (optional) | List of actions to perform.                                  |
| `model`            | `str` (optional)       | Model identifier for machine learning requests.              |
| `temperature`      | `float` (optional)     | A value between 0.0 and 1.0 controlling response randomness. |
| `max_tokens`       | `int` (optional)       | Maximum tokens allowed in the response.                      |
| `model_provider`   | `str` (optional)       | The provider of the ML model (e.g., OpenAI, Hugging Face).   |
| `provider_kwargs`  | `dict` (optional)      | Additional arguments for the model provider.                 |
| `kwargs`           | `dict` (optional)      | Additional key-value pairs for customization.                |

---

### Methods

#### `to_dict()`

Converts the `APIConfig` object into a dictionary. Fields with `None` values are excluded.

#### `to_json()`

Converts the `APIConfig` object into a JSON string.

#### `init_llm()`

Initializes a chat model using the configuration and returns the model object.

---

### Builder Class Reference

| Method                         | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| `set_user_id(user_id)`         | Sets the `user_id` field.                          |
| `set_user_key(user_key)`       | Sets the `user_key` field.                         |
| `set_api_key(api_key)`         | Sets the `api_key` field.                          |
| `set_input_text(text)`         | Sets the `input_text` field.                       |
| `set_handler(handler)`         | Sets the `handler` field.                          |
| `set_agent_auth_token(token)`  | Sets the `agent_auth_token` field.                 |
| `set_trace_id(trace_id)`       | Sets the `trace_id` field.                         |
| `set_timestamp(timestamp)`     | Sets the `timestamp` field.                        |
| `set_app(app)`                 | Sets the `app` field.                              |
| `set_integration_id(id)`       | Sets the `integration_id` field.                   |
| `set_prompt(prompt)`           | Sets the `prompt` field.                           |
| `set_actions(actions)`         | Sets the `actions` field.                          |
| `set_model(model)`             | Sets the `model` field.                            |
| `set_temperature(temp)`        | Sets the `temperature` field.                      |
| `set_max_tokens(tokens)`       | Sets the `max_tokens` field.                       |
| `set_model_provider(provider)` | Sets the `model_provider` field.                   |
| `set_provider_kwargs(kwargs)`  | Sets the `provider_kwargs` field.                  |
| `set_kwargs(kwargs)`           | Sets additional key-value pairs in `kwargs`.       |
| `build()`                      | Creates an `APIConfig` object with the set fields. |

---
