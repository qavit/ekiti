import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, TypeVar, Generic, Type
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import os

from ekiti.models.word import WordEntry, LanguageCode

T = TypeVar('T', bound=BaseModel)

class StorageError(Exception):
    """Base exception for storage-related errors."""
    pass

class BaseStorage(Generic[T]):
    """Base storage interface."""
    def __init__(self, model: Type[T]):
        self.model = model
    
    def save(self, item: T) -> T:
        raise NotImplementedError
    
    def get(self, item_id: str) -> Optional[T]:
        raise NotImplementedError
    
    def list(self) -> List[T]:
        raise NotImplementedError
    
    def delete(self, item_id: str) -> bool:
        raise NotImplementedError

class YAMLStorage(BaseStorage[WordEntry]):
    """YAML-based storage implementation."""
    
    def __init__(self, file_path: str):
        super().__init__(WordEntry)
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, WordEntry] = {}
        self._load()
    
    def _load(self):
        """Load data from YAML file."""
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                raw_data = yaml.safe_load(f) or {}
                self._data = {
                    k: WordEntry(**v) 
                    for k, v in raw_data.items()
                }
    
    def _save_to_disk(self):
        """Save data to YAML file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                {k: v.dict() for k, v in self._data.items()},
                f,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False
            )
    
    def save(self, entry: WordEntry) -> WordEntry:
        """Save a word entry."""
        if not entry.id:
            entry.id = len(self._data) + 1
        
        entry.last_reviewed = datetime.utcnow()
        entry.review_count += 1
        
        self._data[str(entry.id)] = entry
        self._save_to_disk()
        return entry
    
    def get(self, word_id: str) -> Optional[WordEntry]:
        """Get a word entry by ID."""
        return self._data.get(str(word_id))
    
    def list(self) -> List[WordEntry]:
        """List all word entries."""
        return list(self._data.values())
    
    def delete(self, word_id: str) -> bool:
        """Delete a word entry by ID."""
        word_id_str = str(word_id)
        if word_id_str in self._data:
            del self._data[word_id_str]
            self._save_to_disk()
            return True
        return False

class StorageManager:
    """Manages different storage backends."""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.expanduser("~/.config/ekiti")
        self.storages: Dict[str, BaseStorage] = {}
    
    def get_storage(self, language: str) -> BaseStorage[WordEntry]:
        """Get or create a storage instance for a language."""
        if language not in self.storages:
            storage_path = Path(self.data_dir) / f"{language}.yaml"
            self.storages[language] = YAMLStorage(str(storage_path))
        return self.storages[language]
    
    def get_all_words(self) -> List[WordEntry]:
        """Get all words from all language storages."""
        all_words = []
        for lang in os.listdir(self.data_dir):
            if lang.endswith('.yaml'):
                lang_code = lang[:-5]  # Remove .yaml
                storage = self.get_storage(lang_code)
                all_words.extend(storage.list())
        return all_words
