"""AI Classification Service."""
from transformers import pipeline

class AIService:
    def __init__(self):
        # Changed to Facebook's BART Large MNLI as requested
        self.classifier = pipeline(
            task="zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1
        )

    def classify_description(
        self, 
        text: str, 
        candidate_labels: list[str],
        hypothesis_template: str = "This example is {}."
    ) -> dict[str, int]:
        result: dict = self.classifier(
            text, 
            candidate_labels, 
            multi_label=True,
            hypothesis_template=hypothesis_template
        ) # type: ignore
        
        return {
            label: int(score * 100) 
            for label, score in zip(result["labels"], result["scores"])
        }