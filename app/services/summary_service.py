from typing import Optional


class SummaryService:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or "llama3"

    async def generate_summary(self, content: str) -> str:
        if not content:
            return "No content provided."
        return f"[{self.model_name}] Summary: {content[:180]}"

    async def generate_review_summary(self, reviews: list[dict]) -> str:
        if not reviews:
            return "No reviews available."
        return f"{len(reviews)} reviews analyzed. Overall sentiment is positive."
