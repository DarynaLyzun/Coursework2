"""Unit tests for the AIService.

This module verifies that the AI service correctly integrates with the
transformers pipeline and formats the classification results, using mocks
to avoid loading the heavy neural network during testing.
"""

from unittest.mock import patch, MagicMock
from app.services.ai_service import AIService

def test_ai_service_initialization():
    """Verifies that the pipeline is loaded with the correct model parameters.
    
    Ensures that we are requesting the specific mDeBERTa model and using the
    CPU (device=-1) by default.
    """
    with patch("app.services.ai_service.pipeline") as mock_pipeline:
        AIService()
        
        mock_pipeline.assert_called_once_with(
            task="zero-shot-classification",
            model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
            device=-1
        )

def test_classify_description_formatting():
    """Verifies that classification scores are correctly converted to percentages.
    
    The transformers library returns scores as floats (e.g., 0.992). This test
    ensures our service converts them to integers (e.g., 99) and maps them
    correctly to their labels.
    """
    mock_hf_result = {
        "labels": ["Rain", "Cold", "Sunny"],
        "scores": [0.992, 0.455, 0.001]
    }
    
    with patch("app.services.ai_service.pipeline") as mock_pipeline:
        mock_instance = MagicMock()
        mock_instance.return_value = mock_hf_result
        mock_pipeline.return_value = mock_instance
        
        service = AIService()
        output = service.classify_description("heavy rain", ["Rain", "Cold", "Sunny"])
        
        assert output["Rain"] == 99   # 0.992 -> 99
        assert output["Cold"] == 45   # 0.455 -> 45
        assert output["Sunny"] == 0   # 0.001 -> 0