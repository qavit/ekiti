from datetime import datetime
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field

LanguageCode = Literal["en", "de", "es", "id", "taigi"]
DifficultyLevel = Literal[1, 2, 3, 4, 5]

class Translation(BaseModel):
    """Represents a translation of a word in a specific language."""
    language: LanguageCode
    text: str
    
class Example(BaseModel):
    """Example sentence with its translation."""
    sentence: str
    translation: str

class WordDetails(BaseModel):
    """Additional details about a word."""
    gender: Optional[str] = None  # For languages with grammatical gender
    plural: Optional[str] = None
    part_of_speech: Optional[str] = None
    notes: Optional[str] = None

class WordEntry(BaseModel):
    """Represents a vocabulary entry in the database."""
    id: Optional[int] = None
    word: str  # The word in the target language
    language: LanguageCode  # Language code (e.g., 'de' for German)
    translations: Dict[LanguageCode, str]  # Translations in different languages
    details: WordDetails = Field(default_factory=WordDetails)
    examples: List[Example] = []
    tags: List[str] = []
    difficulty: DifficultyLevel = 3
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_reviewed: Optional[datetime] = None
    review_count: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "word": "Buch",
                "language": "de",
                "translations": {"en": "book"},
                "details": {
                    "gender": "n",
                    "plural": "Bücher",
                    "part_of_speech": "noun"
                },
                "examples": [
                    {
                        "sentence": "Ich lese ein Buch.",
                        "translation": "I'm reading a book."
                    }
                ],
                "tags": ["noun", "A1"],
                "difficulty": 2
            }
        }
