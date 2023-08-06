import json
from collections import defaultdict
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

from .functional import FunctionWrapper, function_info
from .prompt import generate_prompt, generate_react_prompt


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
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = self.api_key
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.functions: List[FunctionWrapper] = []

        self.system_prompt = generate_prompt()

    def make_child(self) -> "OpenAI":
        return OpenAI(self.api_key, self.model_name, self.temperature, self.top_p, self.openai)

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

    def add_instructions(self, instructions: Union[str, List[str]]):
        """
        Adds instructions to the system prompt.

        Args:
            prompt (str): The system prompt to set.
        """
        if isinstance(instructions, str):
            instructions = [instructions]
        instructions = list(map(lambda x: x.strip(), instructions))
        more = "\n" + "\n- ".join(instructions) + "\n"
        more = "#### Additional Instructions\n" + more
        self.system_prompt = generate_prompt(more)

    def set_system_prompt(self, prompt: str):
        """
        Sets the system prompt.

        Args:
            prompt (str): The system prompt to set.
        """
        self.system_prompt = generate_prompt(prompt)

    def step(self, message, delta):
        for k, v in delta.items():
            if message[k] is None:
                message[k] = v
            elif isinstance(message[k], dict):
                self.step(message[k], v)
            elif isinstance(message[k], str):
                message[k] += v
            elif isinstance(message[k], list):
                message[k].append(v)

    def call(
        self,
        user_prompt: str,
        messages: Optional[List[Dict[str, str]]] = None,
        stream_callback=None,
    ):
        """
        Calls the OpenAI API with the given user prompt and messages.

        Args:
            user_prompt (str): The user prompt to use.
            messages (Optional[List[Dict[str, str]]]): The messages to use. Defaults to None.
            stream_callback (Optional[Callable[[Dict[str, str]], None]]): A callback function to call for each message returned by the OpenAI API. Defaults to None.

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
                stream=stream_callback is not None,
            )
        else:
            response = self.openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=stream_callback is not None,
            )

        if stream_callback is not None:
            message = defaultdict(lambda: None)
            for chunk in response:
                delta = chunk["choices"][0]["delta"]
                self.step(message, delta)
                stream_callback(chunk)
            message = dict(message)
        else:
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
            return self.call(user_prompt, messages, stream_callback=stream_callback)

        return messages

    def __call__(self, user_prompt: str, stream_callback=None) -> Tuple[List[Dict[str, str]], str]:
        """
        Calls the OpenAI API with the given user prompt.

        Args:
            user_prompt (str): The user prompt to use.

        Returns:
            Tuple[List[Dict[str, str]], str]: The messages returned by the OpenAI API and the final message.
            str: The final message returned by the OpenAI API.
        """
        messages = self.call(user_prompt, stream_callback=stream_callback)
        return messages, messages[-1]["content"]

    def __repr__(self) -> str:
        return f"OpenAI(model_name={self.model_name}, temperature={self.temperature}, top_p={self.top_p})"

    def _create_react_functions(self):
        """Creates three OpenAI agents"""
        analyzer = self.make_child()
        planner = self.make_child()
        actor = self.make_child()
        analyzer.set_system_prompt(generate_react_prompt(turn="analyze"))
        planner.set_system_prompt(generate_react_prompt(turn="plan"))
        actor.set_system_prompt(generate_react_prompt(turn="act"))

        def analyze(description):
            """Analyze the description. The output format is like `goal state: xxx, current state: xxx, summary: xxx`.

            :param description: The well described text of the current situation and the context.
            :type description: str
            :return: The goal state, the current state, and summary of the current situation and the context. This includes the available functions and their arguments.
            :rtype: str
            """
            return analyzer(f"{description}")[1]

        def plan(goal_state, current_state):
            """Plan the sequence of actions to achieve the goal state from the current state. This can also be called multiple times to replan the sequence of actions.

            :param goal_state: The goal state.
            :type goal_state: str
            :param current_state: The current state.
            :type current_state: str
            :return: The sequence of actions to achieve the goal state from the current state.
            :rtype: list[str]
            """
            return planner(f"Goal state: {goal_state}, Current state: {current_state}")[1]

        def act(current_state, action, summary):
            """Act the action in the current state and the summary.

            :param current_state: The current state.
            :type current_state: str
            :param action: The action to act.
            :type action: str
            :param summary: The summary of the current situation and the context.
            :type summary: str
            :return: The next state.
            :rtype: str
            """
            return actor(f"Current state: {current_state}, Action: {action}, Summary: {summary}")[1]

        return analyze, plan, act

    def set_react_functions(self):
        """Adds three OpenAI agents"""
        analyzer, planner, actor = self._create_react_functions()
        self.set_function(analyzer)
        self.set_function(planner)
        self.set_function(actor)
