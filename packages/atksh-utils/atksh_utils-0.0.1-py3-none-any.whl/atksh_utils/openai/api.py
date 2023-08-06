import json
from pprint import pprint
from typing import Any, Dict, Generator, List, Optional

from .functional import FunctionWrapper, function_info


class OpenAI:
    """
    A class for interacting with the OpenAI API.

    Args:
        api_key (str): The API key for accessing the OpenAI API.
        model_name (str): The name of the OpenAI model to use.
        openai (Any): The OpenAI module to use. If None, the module will be imported.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        openai=None,
    ) -> None:
        """
        Initializes the OpenAI class.

        Args:
            api_key (str): The API key for accessing the OpenAI API.
            model_name (str): The name of the OpenAI model to use.
            temperature (float): The temperature to use for the OpenAI API. Defaults to 0.7.
            top_p (float): The top_p to use for the OpenAI API. Defaults to 0.9.
            openai (Any): The OpenAI module to use. If None, the module will be imported.
        """
        if openai is None:
            import openai
        self.openai = openai
        self.openai.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.functions: List[FunctionWrapper] = []

        self.system_prompt = "You are FunctionChatGPT."

    def set_function(self, func):
        """
        Adds a function to the list of functions that can be called by the OpenAI API.

        Args:
            func: The function to add.
        """
        self.functions.append(function_info(func))

    def get_functions(self):
        """
        Returns a list of information about the functions that can be called by the OpenAI API.

        Returns:
            List[Dict[str, Any]]: A list of information about the functions.
        """
        return [f.info for f in self.functions]

    def set_system_prompt(self, prompt: str):
        """
        Sets the system prompt for the OpenAI API.

        Args:
            prompt (str): The system prompt to set.
        """
        self.system_prompt = prompt

    def call(self, user_prompt: str, messages: Optional[List[Dict[str, str]]] = None):
        """
        Calls the OpenAI API with the given user prompt and messages.

        Args:
            user_prompt (str): The user prompt to use.
            messages (Optional[List[Dict[str, str]]]): The messages to use. Defaults to None.

        Returns:
            List[Dict[str, str]]: The messages returned by the OpenAI API.
        """
        if messages is None:
            messages = []
            messages.append({"role": "system", "content": self.system_prompt})
            messages.append({"role": "user", "content": user_prompt})
        if len(self.functions) > 0:
            functions = self.get_functions()
            response = self.openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                functions=functions,
                function_call="auto",
                temperature=self.temperature,
                top_p=self.top_p,
            )
        else:
            response = self.openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
            )
        message = response["choices"][0]["message"]
        messages.append(message)

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            func = next(f for f in self.functions if f.info["name"] == function_name)

            filtered_args = {}
            function_call_args = json.loads(message["function_call"]["arguments"])
            for arg, value in function_call_args.items():
                if arg in func.info["parameters"]["properties"]:
                    filtered_args[arg] = value
            ret = func(**filtered_args)
            messages.append({"role": "function", "name": function_name, "content": json.dumps(ret)})
            return self.call(user_prompt, messages)

        return messages

    def __call__(self, user_prompt: str) -> str:
        """
        Calls the OpenAI API with the given user prompt.

        Args:
            user_prompt (str): The user prompt to use.

        Returns:
            str: The response from the OpenAI API.
        """
        messages = self.call(user_prompt)
        return messages[-1]["content"]
