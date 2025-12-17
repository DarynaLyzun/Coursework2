"""Service for AI-based text classification."""

from transformers import pipeline


class AIService:
    """Handles interaction with the Hugging Face transformers pipeline."""

    def __init__(self):
        """Initializes the Zero-Shot Classification pipeline."""
        self.classifier = pipeline(
            task="zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1,
        )

    def classify_description(
        self,
        text: str,
        candidate_labels: list[str],
        hypothesis_template: str = "This example is {}.",
    ) -> dict[str, int]:
        """Classifies text against a list of candidate labels.

        Args:
            text (str): The text to classify.
            candidate_labels (list[str]): The list of possible labels.
            hypothesis_template (str): The template for the hypothesis.

        Returns:
            dict[str, int]: A dictionary mapping labels to confidence percentages (0-100).
        """
        result: dict = self.classifier(
            text,
            candidate_labels,
            multi_label=True,
            hypothesis_template=hypothesis_template,
        ) # type: ignore

        return {
            label: int(score * 100)
            for label, score in zip(result["labels"], result["scores"])
        }