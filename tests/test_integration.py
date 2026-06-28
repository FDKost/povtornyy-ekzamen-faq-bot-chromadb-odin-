import pytest
from bot import FAQBot

def test_bot_integration():
    bot = FAQBot()
    response = bot.answer("What is the capital of France?")
    assert isinstance(response, str)
    assert len(response) > 0
