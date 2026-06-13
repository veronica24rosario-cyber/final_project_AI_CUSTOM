"""
BDD scenarios for Context Augmented Generation.

Feature: Context Augmented Generation

Scenario: Remember user name
  Given a user starts a conversation
  When the user says "My name is Julio"
  And later asks "What is my name?"
  Then the system should remember "Julio"

Scenario: Remember preferred technology
  Given a user says "I work with Python"
  When the user later asks "What technology do I use?"
  Then the system should remember "Python"
"""
import tempfile
from pathlib import Path

import pytest

from backend.context_store import ContextStore
from backend.cag.context_manager import ContextManager


@pytest.fixture
def manager(tmp_path):
    store = ContextStore(path=tmp_path / "bdd.json")
    return ContextManager(store=store)


class TestRememberUserName:
    """Scenario: Remember user name."""

    def test_user_name_is_persisted(self, manager):
        # When the user says "My name is Julio"
        manager.save_context("julio_user", "My name is Julio")
        # Then the system should remember "Julio"
        context = manager.retrieve_context("julio_user")
        values = " ".join(str(item["value"]) for item in context)
        assert "Julio" in values

    def test_context_prompt_contains_name(self, manager):
        manager.save_context("julio_user", "My name is Julio")
        prompt = manager.build_context_prompt("julio_user")
        assert "Julio" in prompt


class TestRememberPreferredTechnology:
    """Scenario: Remember preferred technology."""

    def test_technology_is_persisted(self, manager):
        # Given a user says "I work with Python"
        manager.save_context("dev_user", "I work with Python")
        # Then the system should remember "Python"
        context = manager.retrieve_context("dev_user")
        values = " ".join(str(item["value"]) for item in context)
        assert "Python" in values

    def test_context_prompt_contains_technology(self, manager):
        manager.save_context("dev_user", "I work with Python")
        prompt = manager.build_context_prompt("dev_user")
        assert "Python" in prompt
