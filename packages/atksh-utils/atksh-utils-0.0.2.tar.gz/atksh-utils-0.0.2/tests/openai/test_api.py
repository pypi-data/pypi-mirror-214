import json
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock

import pytest

from atksh_utils.openai import FunctionWrapper, OpenAI, function_info


@pytest.fixture
def openai_mock():
    openai_mock = MagicMock()
    return openai_mock


@pytest.fixture
def openai_instance(openai_mock):
    return OpenAI(api_key="test_api_key", model_name="test_model", openai=openai_mock)


def example_function(a: int, b: int) -> int:
    """This is a addition function.

    :param a: An integer.
    :type a: integer
    :param b: An integer.
    :type b: integer
    :return: The sum of a and b.
    :rtype: integer
    """
    return a + b


def test_openai_init(openai_instance):
    assert openai_instance.model_name == "test_model"
    assert openai_instance.functions == []
    assert openai_instance.system_prompt == "You are FunctionChatGPT."


def test_set_function(openai_instance):
    openai_instance.set_function(example_function)
    assert len(openai_instance.functions) == 1
    assert isinstance(openai_instance.functions[0], FunctionWrapper)


def test_get_functions(openai_instance):
    openai_instance.set_function(example_function)
    functions = openai_instance.get_functions()
    assert len(functions) == 1
    assert functions[0]["name"] == "example_function"


def test_set_system_prompt(openai_instance):
    openai_instance.set_system_prompt("New system prompt.")
    assert openai_instance.system_prompt == "New system prompt."


def test_call_without_function_call(openai_instance, openai_mock):
    user_prompt = "What is the weather like today?"
    openai_mock.ChatCompletion.create.return_value = {
        "choices": [{"message": {"role": "assistant", "content": "It is sunny today."}}]
    }

    response = openai_instance.call(user_prompt)
    assert len(response) == 3
    assert response[-1]["content"] == "It is sunny today."


def test_call_with_function_call(openai_instance, openai_mock):
    openai_instance.set_function(example_function)

    user_prompt = "Calculate 3 + 4."
    openai_mock.ChatCompletion.create.side_effect = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "function_call": {
                            "name": "example_function",
                            "arguments": json.dumps({"a": 3, "b": 4}),
                        },
                    }
                }
            ]
        },
        {"choices": [{"message": {"role": "assistant", "content": "The result is 7."}}]},
    ]

    response = openai_instance.call(user_prompt)
    assert response[-1]["content"] == "The result is 7."
