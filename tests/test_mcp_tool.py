import pytest
from mcp_tool import UppercaseTool

def test_uppercase_tool():
    tool = UppercaseTool()
    input_text = "hello world"
    output = tool.run(input_text)
    assert output == "HELLO WORLD"
