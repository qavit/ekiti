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
        self.skipped: bool = False
        self.unfamiliar: bool = False
        self.hint_shown: bool = False
    
    def submit_answer(self, answer: str) -> bool:
        """Submit an answer and return if it's correct."""
        self.user_answer = answer
        self.answered_correctly = (answer == self.correct_answer)
        return self.answered_correctly
    
    def skip(self) -> None:
        """Mark this question as skipped."""
        self.skipped = True
        self.answered_correctly = False
    
    def mark_unfamiliar(self) -> None:
        """Mark this word as unfamiliar."""
        self.unfamiliar = True
    
    def show_hint(self) -> str:
        """Show a hint for this question."""
        self.hint_shown = True
        if self.question_type == "multiple_choice":
            # For multiple choice, show half of the options (rounded up)
            num_to_show = (len(self.options) + 1) // 2
            hint_options = random.sample(self.options, num_to_show)
            if self.correct_answer not in hint_options:
                hint_options[-1] = self.correct_answer
            return f"Hint: The answer is one of: {', '.join(hint_options)}"
        else:
            # For spelling, show the first half of the word
            hint_length = max(1, len(self.correct_answer) // 2)
            hint = self.correct_answer[:hint_length] + "_" * (len(self.correct_answer) - hint_length)
            return f"Hint: The word starts with: {hint}"

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
    
    def _generate_questions(self) -> None:
        """Generate quiz questions based on the selected mode and direction."""
        # Select random words for the quiz
        selected_words = random.sample(self.words, self.num_questions)
        
        for word in selected_words:
            if self.direction == "target_to_english":
                question = word.word
                correct_answer = word.translations.get("en", "No English translation")
            else:
                question = word.translations.get("en", "No English translation")
                correct_answer = word.word
            
            if self.mode == "multiple_choice":
                # Generate incorrect options
                other_words = [w for w in self.words if w != word]
                other_answers = [
                    w.translations.get("en", "") if self.direction == "target_to_english" else w.word 
                    for w in random.sample(other_words, min(3, len(other_words)))
                ]
                options = [correct_answer] + other_answers
                random.shuffle(options)
            else:
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
    
    def get_current_question(self) -> Optional[QuizQuestion]:
        """Get the current question."""
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def submit_answer(self, answer: str) -> bool:
        """Submit an answer for the current question."""
        question = self.questions[self.current_question_index]
        is_correct = question.submit_answer(answer)
        if is_correct:
            self.score += 1
        return is_correct
    
    def skip_question(self) -> None:
        """Skip the current question."""
        if 0 <= self.current_question_index < len(self.questions):
            self.questions[self.current_question_index].skip()
    
    def mark_current_as_unfamiliar(self) -> None:
        """Mark the current word as unfamiliar."""
        if 0 <= self.current_question_index < len(self.questions):
            self.questions[self.current_question_index].mark_unfamiliar()
    
    def get_hint(self) -> str:
        """Get a hint for the current question."""
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index].show_hint()
        return "No current question to get a hint for."
    
    def get_skipped_questions(self) -> List[QuizQuestion]:
        """Get all skipped questions."""
        return [q for q in self.questions if q.skipped]
    
    def get_unfamiliar_words(self) -> List[WordEntry]:
        """Get all words marked as unfamiliar."""
        return [q.word for q in self.questions if q.unfamiliar]
    
    def get_progress(self) -> Tuple[int, int]:
        """Return current progress as (current_question, total_questions)."""
        return (self.current_question_index + 1, len(self.questions))
    
    def is_complete(self) -> bool:
        """Check if the quiz is complete."""
        return all(q.answered_correctly is not None or q.skipped for q in self.questions)
    
    def get_results(self) -> Dict[str, float]:
        """Get quiz results."""
        answered_questions = [q for q in self.questions if not q.skipped]
        total_questions = len(answered_questions)
        correct_answers = sum(1 for q in answered_questions if q.answered_correctly)
        score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        time_taken = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            "total_questions": total_questions,
            "answered_questions": len([q for q in self.questions if q.answered_correctly is not None]),
            "skipped_questions": len(self.get_skipped_questions()),
            "unfamiliar_words": len(self.get_unfamiliar_words()),
            "correct_answers": correct_answers,
            "score_percentage": score_percentage,
            "time_taken_seconds": time_taken
        }
