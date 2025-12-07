"""AI Classification Service.

This module provides the interface to the Hugging Face transformers library,
specifically loading the mDeBERTa model for zero-shot text classification
to categorize weather descriptions into clothing-relevant tags.
"""

from transformers import pipeline

class AIService:
    """Uses a pre-trained NLI model to classify text.

    Attributes:
        classifier (Pipeline): The Hugging Face pipeline instance optimized
            for zero-shot classification.
    """

    def __init__(self):
        """Initializes the AI pipeline with the specific mDeBERTa model.
        
        The model is loaded into memory upon instantiation.
        """
        self.classifier = pipeline(
            task="zero-shot-classification",
            model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
            device=-1
        )

    def classify_description(self, text: str, candidate_labels: list[str]) -> dict[str, int]:
        """Classifies text against a list of labels using the NLI model.

        Args:
            text (str): The weather description to analyze (e.g., "heavy intensity rain").
            candidate_labels (list[str]): Potential tags to apply (e.g., ["Rain", "Cold"]).

        Returns:
            dict[str, int]: A dictionary mapping labels to confidence percentages (0-100).
            Example: {'Rain': 99, 'Cold': 10}
        """
        # We tell Python explicitly that 'result' is a dictionary to satisfy type checkers
        result: dict = self.classifier(text, candidate_labels, multi_label=True) # type: ignore
        
        return {
            label: int(score * 100) 
            for label, score in zip(result["labels"], result["scores"])
        }