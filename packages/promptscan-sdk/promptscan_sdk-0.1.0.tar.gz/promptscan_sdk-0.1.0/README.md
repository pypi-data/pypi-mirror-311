# PromptScan Python SDK

The PromptScan Python SDK provides a simple way to integrate PromptScan's monitoring and analytics capabilities into your LLM application.

## Installation

```bash
pip install promptscan-sdk
```

## Quick Start

```python
import promptscan_sdk
from promptscan_sdk.client import GenerationInput, GenerationMessageInput, UsageInput
from datetime import datetime, UTC

# Initialize the SDK
promptscan_sdk.configure(api_key="your-project-api-key")

# Collect generation data
promptscan_sdk.collect(
    GenerationInput(
        session_id="unique-session-id",
        id="generation-id",
        model="gpt-4",
        messages=[
            GenerationMessageInput(role="system", content="You are a helpful assistant.")
        ],
        usage=UsageInput(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150
        ),
        created=datetime.now(tz=UTC),
        duration=0.5,
        time_to_first_token=0.15
    )
)

# Close the SDK on application exit, since it uses background threads for non-blocking flushing of the generations that should be stopped and generation buffer flushed.
promptscan_sdk.close()
```

## Multiple api-key support

You can log generations for different projects by using multiple project api-keys.

```python
collect(generation_a_input, api_key="your-project-A-api-key")
collect(generation_b_input, api_key="your-project-B-api-key")
```


[//]: # (## OpenAI API)

[//]: # ()
[//]: # (```python)

[//]: # (from promptscan_sdk.utils import from_openai_completion)

[//]: # ()
[//]: # (generation = from_openai_completion&#40;completion&#41;)

[//]: # (collect&#40;generation&#41;)

[//]: # (```)

[//]: # ()
[//]: # (```python)

[//]: # (from promptscan_sdk.utils import from_openai_completion)

[//]: # ()
[//]: # (generation, chunks = from_openai_completion_stream&#40;completion&#41;)

[//]: # ()
[//]: # (for chunk in chunks:)

[//]: # (    pass)

[//]: # ()
[//]: # (collect&#40;generation&#41;)

[//]: # (```)