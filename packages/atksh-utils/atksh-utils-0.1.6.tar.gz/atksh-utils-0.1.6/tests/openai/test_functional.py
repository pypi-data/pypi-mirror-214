from atksh_utils.openai import function_info


def my_function(x: int, y: str, z: "list[str]", flag: bool = False) -> float:
    """
    This is a test function.

    :param x: An integer.
    :type x: int
    :param y: A string.
    :type y: str
    :param z: A list of strings.
    :type z: list[str]
    :param flag: A boolean. Defaults to False.
    :type flag: bool, optional
    :return: A float.
    :rtype: float
    """
    return 3.14


def test_extract_function_info():
    func = function_info(my_function)
    info = func.info

    assert info["name"] == "my_function"
    assert info["description"] == "This is a test function."
    assert info["parameters"]["type"] == "object"
    assert info["parameters"]["properties"]["x"]["type"] == "integer"
    assert info["parameters"]["properties"]["x"]["description"] == "An integer."
    assert info["parameters"]["properties"]["y"]["type"] == "string"
    assert info["parameters"]["properties"]["y"]["description"] == "A string."
    assert info["parameters"]["properties"]["z"]["type"] == "array"
    assert info["parameters"]["properties"]["z"]["items"]["type"] == "string"
    assert info["parameters"]["properties"]["flag"]["type"] == "boolean"
    assert (
        info["parameters"]["properties"]["flag"]["description"] == "A boolean. Defaults to False."
    )
    assert info["parameters"]["required"] == ["x", "y", "z"]
    assert info["return_type"] == "number"
