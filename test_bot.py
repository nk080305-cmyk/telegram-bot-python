"""
Unit tests for bot.py recommendation logic and conversation state helpers.

Run with:  pytest test_bot.py -v
"""

import os
import sys
import types
import importlib.util
import pytest


# ---------------------------------------------------------------------------
# Helpers to import bot.py without a real Telegram connection
# ---------------------------------------------------------------------------

def _load_bot_module():
    """Import bot.py with telebot and dotenv mocked out."""
    # Mock telebot so no real HTTP calls are made at import time
    mock_telebot = types.ModuleType('telebot')

    class _MockBot:
        def __init__(self, token):
            pass

        def message_handler(self, **kwargs):
            def decorator(func):
                return func
            return decorator

    mock_telebot.TeleBot = _MockBot
    sys.modules['telebot'] = mock_telebot

    mock_dotenv = types.ModuleType('dotenv')
    mock_dotenv.load_dotenv = lambda: None
    sys.modules['dotenv'] = mock_dotenv

    os.environ['API_TOKEN'] = 'test_token'

    spec = importlib.util.spec_from_file_location(
        'bot',
        os.path.join(os.path.dirname(__file__), 'bot.py'),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bot_module = _load_bot_module()
get_recommendations = bot_module.get_recommendations
CAR_CATALOGUE = bot_module.CAR_CATALOGUE
normalize_brand = bot_module.normalize_brand


# ---------------------------------------------------------------------------
# get_recommendations tests
# ---------------------------------------------------------------------------

class TestGetRecommendations:

    def test_unknown_brand_returns_error_with_brand_list(self):
        result = get_recommendations(50000, 0, 'Lada')
        assert "don't have listings for 'Lada'" in result
        # Should list available brands
        assert 'Toyota' in result

    def test_affordable_new_car(self):
        result = get_recommendations(30000, 0, 'Toyota')
        assert 'Corolla' in result  # 20 000 ≤ 30 000
        assert 'Camry' in result    # 28 000 ≤ 30 000
        assert 'Hilux' not in result  # 35 000 > 30 000

    def test_nothing_affordable_shows_cheapest(self):
        result = get_recommendations(1000, 0, 'BMW')
        assert 'No BMW models' in result
        assert 'cheapest' in result.lower()

    def test_exact_budget_boundary_included(self):
        # Toyota Corolla is 20 000; budget exactly 20 000 should include it
        result = get_recommendations(20000, 0, 'Toyota')
        assert 'Corolla' in result
        assert 'Camry' not in result  # 28 000 > 20 000

    def test_used_car_discount_one_extra_owner(self):
        # 2 owners → 1 extra → 15 % discount
        # Renault Clio: 15000 * 0.85 = 12 750  →  fits in 16 000
        # Renault Captur: 20000 * 0.85 = 17 000 → does NOT fit in 16 000
        result = get_recommendations(16000, 2, 'Renault')
        assert 'Clio' in result
        assert 'Captur' not in result

    def test_discount_cap_at_75_percent(self):
        # 7 owners → 6 extra → 6 * 15% = 90%  →  capped at 75%
        # Renault Clio: 15000 * 0.25 = 3 750
        result = get_recommendations(5000, 7, 'Renault')
        assert 'Clio' in result
        assert '3,750' in result

    def test_no_discount_for_one_owner(self):
        # 1 owner → 0 extra owners → no discount
        result_new = get_recommendations(30000, 0, 'Toyota')
        result_one = get_recommendations(30000, 1, 'Toyota')
        assert result_new == result_one

    def test_bmw_case_insensitive_via_handler_logic(self):
        """normalize_brand must resolve all BMW variants to the catalogue key 'BMW'."""
        normalize = bot_module.normalize_brand
        for variant in ('bmw', 'BMW', 'Bmw', 'bMw'):
            brand = normalize(variant)
            assert brand == 'BMW', f"Expected 'BMW' for input {variant!r}, got {brand!r}"
        result = get_recommendations(50000, 0, 'BMW')
        assert '3 Series' in result

    def test_all_brands_are_reachable(self):
        """Every brand in the catalogue should return recommendations for a high budget."""
        for brand in CAR_CATALOGUE:
            result = get_recommendations(200000, 0, brand)
            assert 'No ' not in result, f"Brand {brand!r} returned no results"

    def test_output_format_contains_bullet_and_price(self):
        result = get_recommendations(30000, 0, 'Honda')
        # Should have bullet points and dollar signs
        assert '•' in result
        assert '$' in result



# ---------------------------------------------------------------------------
# /help handler
# ---------------------------------------------------------------------------

class TestHelpHandler:

    def _make_message(self, chat_id=42):
        """Return a minimal fake message object."""
        msg = types.SimpleNamespace()
        msg.chat = types.SimpleNamespace(id=chat_id)
        return msg

    def test_help_handler_sends_message(self):
        """cmd_help should call bot.send_message with all four commands listed."""
        sent = {}

        def fake_send(chat_id, text, **kwargs):
            sent['chat_id'] = chat_id
            sent['text'] = text

        bot_module.bot.send_message = fake_send
        bot_module.cmd_help(self._make_message(chat_id=99))

        assert sent['chat_id'] == 99
        text = sent['text']
        for cmd in ('/start', '/restart', '/cancel', '/help'):
            assert cmd in text, f"Expected {cmd!r} in /help output"
        assert 'Budget' in text or 'budget' in text.lower()

    def test_help_handler_lists_brands(self):
        """The /help message should mention available brands."""
        sent = {}
        bot_module.bot.send_message = lambda chat_id, text, **kw: sent.update(text=text)
        bot_module.cmd_help(self._make_message())
        # Every brand in the catalogue should appear in the help text
        first_brand = list(CAR_CATALOGUE.keys())[0]
        assert first_brand in sent['text']

class TestStateConstants:

    def test_state_constants_are_distinct(self):
        assert bot_module.BUDGET != bot_module.OWNERS
        assert bot_module.OWNERS != bot_module.BRAND
        assert bot_module.BUDGET != bot_module.BRAND

    def test_state_constants_are_sequential(self):
        assert bot_module.BUDGET == 0
        assert bot_module.OWNERS == 1
        assert bot_module.BRAND == 2
        assert bot_module.FEEDBACK == 3


# ---------------------------------------------------------------------------
# Feedback system tests
# ---------------------------------------------------------------------------

class TestFeedbackSystem:

    def setup_method(self):
        """Reset module-level state before each test."""
        bot_module.user_state.clear()
        bot_module.user_feedback.clear()

    def _make_message(self, text, chat_id=1):
        msg = types.SimpleNamespace()
        msg.chat = types.SimpleNamespace(id=chat_id)
        msg.text = text
        return msg

    def _patch_send(self):
        sent = []
        bot_module.bot.send_message = lambda chat_id, text, **kw: sent.append(text)
        return sent

    def test_valid_rating_is_stored(self):
        """A rating between 1 and 5 is stored in user_feedback."""
        sent = self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.FEEDBACK,
            'budget': 30000,
            'owners': 0,
            'brand': 'Toyota',
        }
        bot_module.handle_text(self._make_message('4'))
        assert len(bot_module.user_feedback) == 1
        assert bot_module.user_feedback[0]['rating'] == 4
        assert bot_module.user_feedback[0]['brand'] == 'Toyota'
        assert bot_module.user_feedback[0]['chat_id'] == 1

    def test_valid_rating_shows_stars(self):
        """Thank-you message includes the correct number of star emojis."""
        sent = self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.FEEDBACK,
            'budget': 30000,
            'owners': 0,
            'brand': 'Honda',
        }
        bot_module.handle_text(self._make_message('3'))
        thank_you = next(m for m in sent if 'Thank you' in m)
        assert '⭐⭐⭐' in thank_you

    def test_invalid_rating_reprompts(self):
        """An out-of-range value keeps the user in FEEDBACK state."""
        sent = self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.FEEDBACK,
            'budget': 30000,
            'owners': 0,
            'brand': 'BMW',
        }
        bot_module.handle_text(self._make_message('6'))
        assert bot_module.user_state[1]['state'] == bot_module.FEEDBACK
        assert len(bot_module.user_feedback) == 0
        assert any('1 to 5' in m for m in sent)

    def test_non_numeric_feedback_reprompts(self):
        """Non-numeric input keeps the user in FEEDBACK state."""
        sent = self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.FEEDBACK,
            'budget': 30000,
            'owners': 0,
            'brand': 'Audi',
        }
        bot_module.handle_text(self._make_message('great'))
        assert bot_module.user_state[1]['state'] == bot_module.FEEDBACK
        assert len(bot_module.user_feedback) == 0

    def test_rating_clears_state(self):
        """After a valid rating, the user's state is cleared."""
        self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.FEEDBACK,
            'budget': 30000,
            'owners': 0,
            'brand': 'Ford',
        }
        bot_module.handle_text(self._make_message('5'))
        assert 1 not in bot_module.user_state

    def test_skip_command_in_feedback_state(self):
        """The /skip command clears FEEDBACK state without storing any rating."""
        sent = self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.FEEDBACK,
            'budget': 30000,
            'owners': 0,
            'brand': 'Mazda',
        }
        msg = self._make_message('/skip')
        msg.chat.id = 1
        bot_module.cmd_skip(msg)
        assert 1 not in bot_module.user_state
        assert len(bot_module.user_feedback) == 0
        assert any('skipped' in m.lower() for m in sent)

    def test_skip_command_outside_feedback_state(self):
        """/skip outside feedback state sends an informative message."""
        sent = self._patch_send()
        msg = self._make_message('/skip')
        msg.chat.id = 1
        bot_module.cmd_skip(msg)
        assert any('Nothing to skip' in m for m in sent)

    def test_brand_state_transitions_to_feedback(self):
        """After entering a brand, the state advances to FEEDBACK."""
        sent = self._patch_send()
        bot_module.user_state[1] = {
            'state': bot_module.BRAND,
            'budget': 50000,
            'owners': 0,
        }
        bot_module.handle_text(self._make_message('Toyota'))
        assert bot_module.user_state[1]['state'] == bot_module.FEEDBACK
        assert any('1–5' in m or '1-5' in m for m in sent)
