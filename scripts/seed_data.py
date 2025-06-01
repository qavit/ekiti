#!/usr/bin/env python3
"""
Script to seed the database with example vocabulary data.
"""
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ekiti.models.word import WordEntry, WordDetails, Example, LanguageCode
from ekiti.core.storage import StorageManager

def create_german_words() -> list[WordEntry]:
    """Create sample German vocabulary."""
    return [
        WordEntry(
            word="Buch",
            language="de",
            translations={"en": "book"},
            details=WordDetails(
                gender="n",
                plural="Bücher",
                part_of_speech="noun"
            ),
            examples=[
                Example(
                    sentence="Ich lese ein Buch.",
                    translation="I'm reading a book."
                )
            ],
            tags=["noun", "A1"]
        ),
        WordEntry(
            word="Haus",
            language="de",
            translations={"en": "house"},
            details=WordDetails(
                gender="n",
                plural="Häuser",
                part_of_speech="noun"
            ),
            examples=[
                Example(
                    sentence="Das ist mein Haus.",
                    translation="This is my house."
                )
            ],
            tags=["noun", "A1"]
        ),
        WordEntry(
            word="gehen",
            language="de",
            translations={"en": "to go"},
            details=WordDetails(
                part_of_speech="verb"
            ),
            examples=[
                Example(
                    sentence="Ich gehe nach Hause.",
                    translation="I'm going home."
                )
            ],
            tags=["verb", "A1"]
        )
    ]

def create_spanish_words() -> list[WordEntry]:
    """Create sample Spanish vocabulary."""
    return [
        WordEntry(
            word="libro",
            language="es",
            translations={"en": "book"},
            details=WordDetails(
                gender="m",
                plural="libros",
                part_of_speech="noun"
            ),
            examples=[
                Example(
                    sentence="Estoy leyendo un libro.",
                    translation="I'm reading a book."
                )
            ],
            tags=["noun", "A1"]
        ),
        WordEntry(
            word="casa",
            language="es",
            translations={"en": "house"},
            details=WordDetails(
                gender="f",
                plural="casas",
                part_of_speech="noun"
            ),
            examples=[
                Example(
                    sentence="Esta es mi casa.",
                    translation="This is my house."
                )
            ],
            tags=["noun", "A1"]
        ),
        WordEntry(
            word="ir",
            language="es",
            translations={"en": "to go"},
            details=WordDetails(
                part_of_speech="verb"
            ),
            examples=[
                Example(
                    sentence="Voy a casa.",
                    translation="I'm going home."
                )
            ],
            tags=["verb", "A1"]
        )
    ]

def create_indonesian_words() -> list[WordEntry]:
    """Create Indonesian vocabulary."""
    words = [
        # Basic pronouns
        WordEntry(
            word="saya",
            language="id",
            translations={"en": "I"},
            details=WordDetails(part_of_speech="pronoun"),
            examples=[
                Example(
                    sentence="Saya senang bertemu dengan Anda.",
                    translation="I'm happy to meet you."
                )
            ],
            tags=["pronoun", "A1"]
        ),
        WordEntry(
            word="kamu",
            language="id",
            translations={"en": "you"},
            details=WordDetails(part_of_speech="pronoun"),
            examples=[
                Example(
                    sentence="Kamu dari mana?",
                    translation="Where are you from?"
                )
            ],
            tags=["pronoun", "A1"]
        ),
        
        # Common verbs
        WordEntry(
            word="makan",
            language="id",
            translations={"en": "to eat"},
            details=WordDetails(part_of_speech="verb"),
            examples=[
                Example(
                    sentence="Saya makan nasi.",
                    translation="I eat rice."
                )
            ],
            tags=["verb", "A1"]
        ),
        WordEntry(
            word="minum",
            language="id",
            translations={"en": "to drink"},
            details=WordDetails(part_of_speech="verb"),
            examples=[
                Example(
                    sentence="Dia minum air.",
                    translation="He/She drinks water."
                )
            ],
            tags=["verb", "A1"]
        ),
        WordEntry(
            word="tidur",
            language="id",
            translations={"en": "to sleep"},
            details=WordDetails(part_of_speech="verb"),
            examples=[
                Example(
                    sentence="Saya tidur pukul sepuluh malam.",
                    translation="I sleep at ten o'clock at night."
                )
            ],
            tags=["verb", "A1"]
        ),
        
        # Common nouns
        WordEntry(
            word="rumah",
            language="id",
            translations={"en": "house"},
            details=WordDetails(part_of_speech="noun"),
            examples=[
                Example(
                    sentence="Ini rumah saya.",
                    translation="This is my house."
                )
            ],
            tags=["noun", "A1"]
        ),
        WordEntry(
            word="restoran",
            language="id",
            translations={"en": "restaurant"},
            details=WordDetails(part_of_speech="noun"),
            examples=[
                Example(
                    sentence="Kami makan di restoran itu semalam.",
                    translation="We ate at that restaurant last night."
                )
            ],
            tags=["noun", "A1"]
        ),
        WordEntry(
            word="pasar",
            language="id",
            translations={"en": "market"},
            details=WordDetails(part_of_speech="noun"),
            examples=[
                Example(
                    sentence="Ibu pergi ke pasar setiap pagi.",
                    translation="Mother goes to the market every morning."
                )
            ],
            tags=["noun", "A1"]
        ),
        
        # Time-related
        WordEntry(
            word="hari",
            language="id",
            translations={"en": "day"},
            details=WordDetails(part_of_speech="noun"),
            examples=[
                Example(
                    sentence="Satu hari ada 24 jam.",
                    translation="There are 24 hours in a day."
                )
            ],
            tags=["time", "A1"]
        ),
        WordEntry(
            word="malam",
            language="id",
            translations={"en": "night"},
            details=WordDetails(part_of_speech="noun"),
            examples=[
                Example(
                    sentence="Saya suka berjalan-jalan di malam hari.",
                    translation="I like to take a walk at night."
                )
            ],
            tags=["time", "A1"]
        ),
        
        # Body parts
        WordEntry(
            word="kepala",
            language="id",
            translations={"en": "head"},
            details=WordDetails(part_of_speech="noun"),
            tags=["body", "A1"]
        ),
        WordEntry(
            word="tangan",
            language="id",
            translations={"en": "hand"},
            details=WordDetails(part_of_speech="noun"),
            tags=["body", "A1"]
        ),
        WordEntry(
            word="kaki",
            language="id",
            translations={"en": "foot, leg"},
            details=WordDetails(part_of_speech="noun"),
            tags=["body", "A1"]
        ),
        
        # Numbers
        WordEntry(
            word="satu",
            language="id",
            translations={"en": "one"},
            details=WordDetails(part_of_speech="number"),
            tags=["number", "A1"]
        ),
        WordEntry(
            word="dua",
            language="id",
            translations={"en": "two"},
            details=WordDetails(part_of_speech="number"),
            tags=["number", "A1"]
        ),
        WordEntry(
            word="tiga",
            language="id",
            translations={"en": "three"},
            details=WordDetails(part_of_speech="number"),
            tags=["number", "A1"]
        ),
        
        # Common phrases
        WordEntry(
            word="Apa kabar?",
            language="id",
            translations={"en": "How are you?"},
            details=WordDetails(part_of_speech="phrase"),
            tags=["phrase", "A1"]
        ),
        WordEntry(
            word="Selamat tinggal.",
            language="id",
            translations={"en": "Goodbye."},
            details=WordDetails(part_of_speech="phrase"),
            tags=["phrase", "A1"]
        )
    ]
    
    return words

def seed_database():
    """Seed the database with example data."""
    storage = StorageManager()
    
    # Add words for each language
    languages = {
        "de": create_german_words(),
        "es": create_spanish_words(),
        "id": create_indonesian_words()
    }
    
    # Save all words
    for lang_code, words in languages.items():
        lang_storage = storage.get_storage(lang_code)
        for word in words:
            lang_storage.save(word)
    
    print(f"Successfully added words for: {', '.join(languages.keys())}")

if __name__ == "__main__":
    seed_database()
