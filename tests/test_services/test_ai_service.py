"""Unit tests for AI service."""

from unittest.mock import MagicMock, patch

from app.services.ai_service import AIService


def test_ai_service_initialization():
    """Verifies that the service initializes the correct model."""
    with patch("app.services.ai_service.pipeline") as mock_pipeline:
        AIService()

        mock_pipeline.assert_called_once_with(
            task="zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1,
        )


def test_classify_description_formatting():
    """Verifies that classification scores are formatted correctly."""
    mock_hf_result = {
        "labels": ["Rain", "Cold", "Sunny"],
        "scores": [0.992, 0.455, 0.001],
    }

    with patch("app.services.ai_service.pipeline") as mock_pipeline:
        mock_instance = MagicMock()
        mock_instance.return_value = mock_hf_result
        mock_pipeline.return_value = mock_instance

        service = AIService()
        output = service.classify_description("heavy rain", ["Rain", "Cold", "Sunny"])

        assert output["Rain"] == 99
        assert output["Cold"] == 45
        assert output["Sunny"] == 0