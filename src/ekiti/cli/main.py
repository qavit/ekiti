import typer
from typing import Optional, List
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt

from ekiti.core.storage import StorageManager
from ekiti.core.quiz import QuizSession, QuizMode, QuizDirection
from ekiti.models.word import WordEntry, LanguageCode

app = typer.Typer()
console = Console()
storage = StorageManager()

# Helper functions
def display_word(word: WordEntry):
    """Display a word entry in a formatted way."""
    console.print(f"\n[bold blue]{word.word}[/bold blue]")
    
    # Display translations
    if word.translations:
        console.print("\n[bold]Translations:[/bold]")
        for lang, text in word.translations.items():
            console.print(f"  {lang.upper()}: {text}")
    
    # Display details
    if word.details:
        details = []
        if word.details.gender:
            details.append(f"Gender: {word.details.gender}")
        if word.details.plural:
            details.append(f"Plural: {word.details.plural}")
        if details:
            console.print("\n" + " | ".join(details))
    
    # Display examples
    if word.examples:
        console.print("\n[bold]Examples:[/bold]")
        for i, example in enumerate(word.examples, 1):
            console.print(f"  {i}. {example.sentence}")
            console.print(f"     → {example.translation}")
    
    if word.tags:
        console.print("\n" + " ".join(f"[dim]#{tag}[/dim]" for tag in word.tags))

def select_language() -> str:
    """Prompt user to select a language."""
    languages = ["German (de)", "Spanish (es)", "Indonesian (id)", "Taigi (taigi)"]
    console.print("\n[bold]Select a language:[/bold]")
    for i, lang in enumerate(languages, 1):
        console.print(f"  {i}. {lang}")
    
    while True:
        try:
            choice = IntPrompt.ask("\nEnter your choice", default=1, show_default=True)
            if 1 <= choice <= len(languages):
                return languages[choice - 1].split("(")[1].strip(" )")
            console.print("[red]Invalid choice. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")

def select_quiz_mode() -> str:
    """Prompt user to select quiz mode."""
    console.print("\n[bold]Select quiz mode:[/bold]")
    console.print("  1. Multiple Choice")
    console.print("  2. Spelling")
    
    while True:
        choice = Prompt.ask("\nEnter your choice", default="1")
        if choice == "1":
            return "multiple_choice"
        elif choice == "2":
            return "spelling"
        console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")

def select_quiz_direction() -> str:
    """Prompt user to select quiz direction."""
    console.print("\n[bold]Select quiz direction:[/bold]")
    console.print("  1. Word → Translation")
    console.print("  2. Translation → Word")
    
    while True:
        choice = Prompt.ask("\nEnter your choice", default="1")
        if choice == "1":
            return "target_to_english"
        elif choice == "2":
            return "english_to_target"
        console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")

# CLI Commands
@app.command()
def add():
    """Add a new word to the dictionary."""
    console.print("\n[bold]Add a new word[/bold]")
    
    # Get word details
    language = select_language()
    word = Prompt.ask("\nEnter the word")
    
    # Get translations
    translations = {}
    while True:
        trans_lang = Prompt.ask("\nEnter language code for translation (e.g., 'en' for English)", default="en").lower()
        trans_text = Prompt.ask(f"Enter '{word}' in {trans_lang.upper()}")
        translations[trans_lang] = trans_text
        
        if not Confirm.ask("Add another translation?"):
            break
    
    # Create word entry
    word_entry = WordEntry(
        word=word,
        language=language,
        translations=translations,
    )
    
    # Add examples
    while Confirm.ask("\nAdd an example sentence?"):
        sentence = Prompt.ask("Enter example sentence")
        translation = Prompt.ask("Enter translation")
        word_entry.examples.append(
            {"sentence": sentence, "translation": translation}
        )
    
    # Save word
    storage.get_storage(language).save(word_entry)
    console.print(f"\n[green]✓ Word '{word}' added successfully![/green]")

@app.command()
def list_words(language: str = None):
    """List all words in the dictionary."""
    if not language:
        language = select_language()
    
    words = storage.get_storage(language).list()
    
    if not words:
        console.print("[yellow]No words found in the dictionary.[/yellow]")
        return
    
    table = Table(title=f"Words in {language.upper()}")
    table.add_column("Word", style="cyan")
    table.add_column("Translation")
    table.add_column("Tags")
    
    for word in words:
        translation = word.translations.get("en", "")
        tags = ", ".join(word.tags) if word.tags else ""
        table.add_row(word.word, translation, tags)
    
    console.print(table)

@app.command()
def quiz(
    language: str = None,
    mode: str = None,
    direction: str = None,
    num_questions: int = 10
):
    """Start a vocabulary quiz."""
    console.print("\n[bold]Vocabulary Quiz[/bold]")
    
    # Get quiz parameters
    if not language:
        language = select_language()
    if not mode:
        mode = select_quiz_mode()
    if not direction:
        direction = select_quiz_direction()
    
    # Get words for the quiz
    words = storage.get_storage(language).list()
    if not words:
        console.print("[red]No words found in the dictionary.[/red]")
        return
    
    # Start quiz session
    session = QuizSession(
        words=words,
        mode=mode,
        direction=direction,
        num_questions=min(num_questions, len(words))
    )
    
    console.print(f"\nStarting {mode.replace('_', ' ').title()} Quiz ({direction})")
    console.print(f"Language: {language.upper()} | Questions: {len(session.questions)}")
    
    # Ask questions
    while not session.is_complete():
        question = session.get_next_question()
        if not question:
            break
        
        current, total = session.get_progress()
        console.print(f"\n[dim]Question {current} of {total}[/dim]")
        console.print(f"\n[bold]{question.question}[/bold]")
        
        if question.question_type == "multiple_choice":
            for i, option in enumerate(question.options, 1):
                console.print(f"  {i}. {option}")
            
            while True:
                try:
                    answer_idx = IntPrompt.ask("\nEnter your answer (number)", default=1) - 1
                    if 0 <= answer_idx < len(question.options):
                        session.submit_answer(question.options[answer_idx])
                        break
                    console.print(f"[red]Please enter a number between 1 and {len(question.options)}[/red]")
                except ValueError:
                    console.print("[red]Please enter a valid number.[/red]")
        else:  # spelling mode
            answer = Prompt.ask("\nType your answer")
            session.submit_answer(answer)
        
        # Show feedback
        if question.answered_correctly:
            console.print("[green]✓ Correct![/green]")
        else:
            console.print(f"[red]✗ Incorrect. The correct answer is: {question.correct_answer}[/red]")
    
    # Show results
    results = session.get_results()
    console.print("\n[bold]Quiz Complete![/bold]")
    console.print(f"Score: {results['correct_answers']}/{results['total_questions']} ({results['score_percentage']:.1f}%)")
    console.print(f"Time: {results['time_taken_seconds']:.1f} seconds")

@app.callback()
def main():
    """Ekiti - A flashcard app for language learning (會記得)."""
    pass

if __name__ == "__main__":
    app()
