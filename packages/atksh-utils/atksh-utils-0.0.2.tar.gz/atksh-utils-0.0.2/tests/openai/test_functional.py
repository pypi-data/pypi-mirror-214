from atksh_utils.openai import function_info


def my_function(x: int, y: str, flag: bool = False) -> float:
    """
    This is a test function.

    :param x: An integer.
    :type x: int
    :param y: A string.
    :type y: str
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
    assert info["parameters"]["properties"]["x"]["type"] == "int"
    assert info["parameters"]["properties"]["x"]["description"] == "An integer."
    assert info["parameters"]["properties"]["y"]["type"] == "str"
    assert info["parameters"]["properties"]["y"]["description"] == "A string."
    assert info["parameters"]["properties"]["flag"]["type"] == "bool, optional"
    assert (
        info["parameters"]["properties"]["flag"]["description"] == "A boolean. Defaults to False."
    )
    assert info["parameters"]["required"] == ["x", "y"]
    assert info["return_type"] == "float"
