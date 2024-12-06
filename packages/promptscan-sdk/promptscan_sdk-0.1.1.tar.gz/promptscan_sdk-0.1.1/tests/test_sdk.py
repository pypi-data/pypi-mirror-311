import logging
import logging.config
from functools import partial
from time import sleep
from unittest.mock import patch, Mock

import pytest

import promptscan_sdk
from promptscan_sdk import PromptScanSDK
from promptscan_sdk.client import GenerationInput, KeyValuePairInput, CollectGenerations, CollectGenerationsCollect, \
    CollectGenerationsCollectError

generation = partial(GenerationInput, model="gpt-4o-mini", messages=[])


@pytest.fixture(autouse=True)
def configure_logging():
    logging.config.fileConfig('logging.conf')


@pytest.fixture(autouse=True)
def client():
    with patch('promptscan_sdk.sdk.GraphQLClient', autospec=True) as mock:
        # mock.collect_generations = AsyncMock(
        #     return_value=CollectGenerations(collect=CollectGenerationsCollect(success=True, error=None)))
        # print("mock.collect_generations", mock.collect_generations)
        yield mock


@pytest.mark.xfail(raises=ValueError)
def test_missing_key():
    PromptScanSDK()


def test_collect_generations_with_multiple_api_keys():
    sdk = PromptScanSDK(api_key="key-default", auto_flush=False, debug=True)

    sdk.collect(generation(id="a"),"key-a")
    sdk.collect(generation(id="b"),"key-b")
    sdk.collect(generation(id="c"),"key-a")
    sdk.collect(generation(id="d"))

    assert sdk.queued_generations_count() == 4

    sdk.flush()
    assert sdk.queued_generations_count() == 0

    assert (collect := sdk.client.collect_generations).call_count == 3
    auth_headers = {call.kwargs.get("headers", {}).get("Authorization", None) for call in collect.call_args_list}
    assert {None, "Bearer key-a", "Bearer key-b"} == auth_headers


def test_retry_on_failed_flush():
    responses = [
        ValueError("Failed to flush"),
        CollectGenerations(collect=CollectGenerationsCollect(
            success=False, error=CollectGenerationsCollectError(message="Failed"))),
        CollectGenerations(collect=CollectGenerationsCollect(success=True, error=None)),
    ]

    def side_effect(*args, **kwargs):
        if isinstance(res := responses.pop(0), Exception):
            raise res
        return res

    sdk = PromptScanSDK(api_key="key-default", auto_flush=False, debug=True)
    sdk.client.collect_generations = Mock(side_effect=side_effect)

    sdk.collect(generation(id="a"))
    assert sdk.queued_generations_count() == 1

    sdk.flush()
    assert sdk.queued_generations_count() == 1

    sdk.flush()
    assert sdk.queued_generations_count() == 1

    sdk.flush()
    assert sdk.queued_generations_count() == 0


def test_auto_flush():
    sdk = PromptScanSDK(api_key="key-default", auto_flush=True, flush_interval_millis=50, debug=True)
    with patch.object(PromptScanSDK, 'flush', new_callable=Mock) as mock_flush:
        sleep(0.1)
        assert 1 <= mock_flush.call_count <= 3
    sdk.close()


def test_flush_on_close():
    sdk = PromptScanSDK(api_key="key-default", auto_flush=False, debug=True)
    with patch.object(PromptScanSDK, 'flush', new_callable=Mock) as mock_flush:
        sdk.close()
        mock_flush.assert_called_once()


async def test_enabled(client):
    sdk = PromptScanSDK(api_key="key-default", auto_flush=False, enabled=False, debug=True)

    sdk.collect(generation(id="a"))
    sdk.flush()
    assert (collect := sdk.client.collect_generations).call_count == 0

    sdk.enabled = True
    sdk.collect(generation(id="a"))
    sdk.flush()
    assert collect.call_count == 1

    sdk.enabled = False
    sdk.collect(generation(id="a"))
    sdk.flush()
    assert collect.call_count == 1


def test_default_meta():
    sdk = PromptScanSDK(api_key="key-default", auto_flush=False, default_tags={"env": "test", "version": "1.0"})

    sdk.collect(generation(
        id="a",
        tags=[
            KeyValuePairInput(key="version", value="2.0"),
            KeyValuePairInput(key="app", value="demo")
        ]
    ))

    generations = sdk.flush()
    assert len(generations) == 1
    assert {t.key: t.value for t in generations[0].tags} == {
        "env": "test",
        "version": "2.0",
        "app": "demo"
    }


def test_static_usage():
    promptscan_sdk.configure(api_key="key-default", debug=True)
    promptscan_sdk.collect(generation(id="a"))

    client = promptscan_sdk.client()
    promptscan_sdk.close()
    client.collect_generations.assert_called_once()

    with pytest.raises(AssertionError):
        promptscan_sdk.collect(generation(id="a"))

