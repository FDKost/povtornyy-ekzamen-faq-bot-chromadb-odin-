import pytest
from bot import FAQBot

@pytest.fixture
def bot():
    return FAQBot()

def test_answer_non_empty(bot):
    response = bot.answer("What is your name?")
    assert isinstance(response, str)
    assert len(response) > 0
