from typing import List, Dict, Optional, Tuple, Literal
import random
from datetime import datetime

from ekiti.models.word import WordEntry, LanguageCode

QuizMode = Literal["spelling", "multiple_choice"]
QuizDirection = Literal["target_to_english", "english_to_target"]

class QuizQuestion:
    """Represents a quiz question."""
    
    def __init__(
        self, 
        word: WordEntry,
        question: str,
        correct_answer: str,
        options: List[str],
        question_type: str,
        direction: str
    ):
        self.word = word
        self.question = question
        self.correct_answer = correct_answer
        self.options = options
        self.question_type = question_type
        self.direction = direction
        self.user_answer: Optional[str] = None
        self.answered_correctly: Optional[bool] = None
    
    def submit_answer(self, answer: str) -> bool:
        """Submit an answer and return if it's correct."""
        self.user_answer = answer
        self.answered_correctly = (answer == self.correct_answer)
        return self.answered_correctly

class QuizSession:
    """Manages a quiz session with multiple questions."""
    
    def __init__(
        self, 
        words: List[WordEntry],
        mode: QuizMode = "multiple_choice",
        direction: QuizDirection = "target_to_english",
        num_questions: int = 10
    ):
        self.words = words
        self.mode = mode
        self.direction = direction
        self.num_questions = min(num_questions, len(words))
        self.questions: List[QuizQuestion] = []
        self.current_question_index = -1
        self.score = 0
        self.start_time = datetime.utcnow()
        self._generate_questions()
    
    def _generate_questions(self):
        """Generate quiz questions based on the selected mode and direction."""
        selected_words = random.sample(self.words, self.num_questions)
        
        for word in selected_words:
            if self.direction == "target_to_english":
                question = f"What does '{word.word}' mean in English?"
                correct_answer = word.translations.get("en", "")
            else:  # english_to_target
                question = f"How do you say '{word.translations.get('en', '')}' in {word.language.upper()}?"
                correct_answer = word.word
            
            if self.mode == "multiple_choice":
                # Get 3 other random words for options
                other_words = [w for w in self.words if w != word]
                options = random.sample(
                    [w.translations.get("en", "") if self.direction == "target_to_english" else w.word 
                     for w in other_words], 
                    k=min(3, len(other_words))
                )
                options.append(correct_answer)
                random.shuffle(options)
            else:  # spelling mode
                options = []
            
            self.questions.append(QuizQuestion(
                word=word,
                question=question,
                correct_answer=correct_answer,
                options=options,
                question_type=self.mode,
                direction=self.direction
            ))
    
    def get_next_question(self) -> Optional[QuizQuestion]:
        """Get the next question in the quiz."""
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            return self.questions[self.current_question_index]
        return None
    
    def submit_answer(self, answer: str) -> bool:
        """Submit an answer for the current question."""
        if 0 <= self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            is_correct = current_question.submit_answer(answer)
            if is_correct:
                self.score += 1
            return is_correct
        return False
    
    def get_progress(self) -> Tuple[int, int]:
        """Return current progress as (current_question, total_questions)."""
        return self.current_question_index + 1, len(self.questions)
    
    def is_complete(self) -> bool:
        """Check if the quiz is complete."""
        return self.current_question_index >= len(self.questions) - 1
    
    def get_results(self) -> Dict:
        """Get quiz results."""
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        
        return {
            "total_questions": len(self.questions),
            "correct_answers": self.score,
            "score_percentage": (self.score / len(self.questions)) * 100 if self.questions else 0,
            "time_taken_seconds": round(duration, 2),
            "start_time": self.start_time,
            "end_time": end_time
        }
