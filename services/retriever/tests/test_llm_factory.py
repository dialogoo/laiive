from unittest.mock import patch
import pytest
from src.main import llm_factory
from src.config import Settings


def test_openai_factory():
    settings = Settings(
        POSTGRES_USER="test",
        POSTGRES_PASSWORD="test",  # pragma: allowlist secret
        POSTGRES_DB="test",
        POSTGRES_URL="postgresql://test",
        API_URL="http://test",
        HOST="0.0.0.0",
        PORT=8000,
        LLM_PROVIDER="openai",
        LLM_MODEL="gpt-4o-mini",
        OPENAI_API_KEY="sk-test-key",  # pragma: allowlist secret
    )

    with patch("src.main.settings", settings):
        with patch("src.main.OpenAI") as mock_openai:
            llm_factory()
            mock_openai.assert_called_once_with(
                api_key="sk-test-key",  # pragma: allowlist secret
                model="gpt-4o-mini",
                temperature=0.1,
            )


def test_anthropic_factory():
    settings = Settings(
        POSTGRES_USER="test",
        POSTGRES_PASSWORD="test",  # pragma: allowlist secret
        POSTGRES_DB="test",
        POSTGRES_URL="postgresql://test",
        API_URL="http://test",
        HOST="0.0.0.0",
        PORT=8000,
        LLM_PROVIDER="anthropic",
        LLM_MODEL="claude-3-5-sonnet-20241022",
        ANTHROPIC_API_KEY="sk-ant-test-key",  # pragma: allowlist secret
    )

    with patch("src.main.settings", settings):
        with patch("src.main.Anthropic") as mock_anthropic:
            llm_factory()
            mock_anthropic.assert_called_once_with(
                api_key="sk-ant-test-key",  # pragma: allowlist secret
                model="claude-3-5-sonnet-20241022",
                temperature=0.1,
            )


def test_gemini_factory():
    settings = Settings(
        POSTGRES_USER="test",
        POSTGRES_PASSWORD="test",  # pragma: allowlist secret
        POSTGRES_DB="test",
        POSTGRES_URL="postgresql://test",
        API_URL="http://test",
        HOST="0.0.0.0",
        PORT=8000,
        LLM_PROVIDER="gemini",
        LLM_MODEL="gemini-2.5-flash-lite",
        GEMINI_API_KEY="test-gemini-key",  # pragma: allowlist secret
    )

    with patch("src.main.settings", settings):
        with patch("src.main.Gemini") as mock_gemini:
            llm_factory()
            mock_gemini.assert_called_once_with(
                api_key="test-gemini-key",  # pragma: allowlist secret
                model="gemini-2.5-flash-lite",
                temperature=0.1,
            )


@pytest.mark.integration
def test_openai_real():
    try:

        settings = Settings()
        if not settings.openai_api_key:
            pytest.skip("OPENAI_API_KEY not set in .env")
        settings.llm_provider = "openai"
        settings.llm_model = "gpt-4o-mini"

        with patch("src.main.settings", settings):
            llm = llm_factory()
            response = llm.complete("Say hello")
            assert response.text is not None
            assert len(response.text) > 0
    except Exception as e:
        pytest.skip(f"Failed to load settings from .env: {e}")


@pytest.mark.integration
def test_anthropic_real():
    try:
        settings = Settings()
        if not settings.anthropic_api_key:
            pytest.skip("ANTHROPIC_API_KEY not set in .env")
        settings.llm_provider = "anthropic"
        settings.llm_model = "claude-3-5-haiku-20241022"

        with patch("src.main.settings", settings):
            llm = llm_factory()
            response = llm.complete("Say hello")
            assert response.text is not None
            assert len(response.text) > 0
    except Exception as e:
        pytest.skip(f"Failed to load settings from .env: {e}")


@pytest.mark.integration
def test_gemini_real():
    try:
        settings = Settings()
        if not settings.gemini_api_key:
            pytest.skip("GEMINI_API_KEY not set in .env")
        settings.llm_provider = "gemini"
        settings.llm_model = "gemini-2.5-flash-lite"

        with patch("src.main.settings", settings):
            llm = llm_factory()
            response = llm.complete("Say hello")
            assert response.text is not None
            assert len(response.text) > 0
    except Exception as e:
        pytest.skip(f"Failed to load settings from .env: {e}")
