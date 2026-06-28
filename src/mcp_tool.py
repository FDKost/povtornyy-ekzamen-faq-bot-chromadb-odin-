from langchain.tools import BaseTool

class UppercaseTool(BaseTool):
    name = "uppercase_tool"
    description = "Converts the input text to uppercase."

    def _run(self, text: str) -> str:
        return text.upper()

    async def _arun(self, text: str) -> str:
        return self._run(text)
