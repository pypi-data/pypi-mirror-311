from asyncio import Future
from datetime import UTC, datetime

import pytest

from promptscan_sdk import PromptScanSDK
from promptscan_sdk.client import GenerationInput, GenerationMessageInput, UsageInput, KeyValuePairInput, \
    CompletionTokensDetailsInput, PromptTokensDetailsInput, GraphQLClient


def test_api_key(client):
    res = client.api_key()
    assert res.api_key.enabled is True
    assert res.api_key.scope == "project"


def test_collect(client):
    res = client.collect_generations([GenerationInput(
        session_id="session-id",
        id="generation-id",
        model="gpt-4o-mini",
        messages=[GenerationMessageInput(role="system", content="You are a hero!")],
        usage=UsageInput(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            prompt_tokens_details=PromptTokensDetailsInput(cached_tokens=0, audio_tokens=0),
            completion_tokens_details=CompletionTokensDetailsInput(reasoning_tokens=0, audio_tokens=0)
        ),
        tags=[KeyValuePairInput(key="hero", value="true")],
        created=datetime.now(tz=UTC),
        duration=0.5,
        time_to_first_token=0.15
    )])
    assert res.collect.success is True
    assert res.collect.error is None


@pytest.fixture
def client() -> GraphQLClient:
    sdk = PromptScanSDK(
        api_key="project-f47ac10b-58cc-4372-a567-0e02b2c3d479",
        base_url="http://localhost:8020/graphql/")
    try:
        yield sdk.client
    finally:
        sdk.close()