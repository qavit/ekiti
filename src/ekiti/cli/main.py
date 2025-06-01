import csv
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import typer
from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt, PromptBase
from rich.table import Table

from ekiti.core.quiz import QuizDirection, QuizMode, QuizSession
from ekiti.core.storage import StorageManager
from ekiti.models.word import Example, LanguageCode, WordDetails, WordEntry

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
def _prompt_word_details(language: str) -> WordDetails:
    """Prompt for word details based on language."""
    details = WordDetails()
    
    # Only ask for gender and plural for languages that need it
    if language in ["de", "es"]:  # German and Spanish have grammatical gender
        details.gender = Prompt.ask(
            "Gender (m/f/n for masculine/feminine/neuter)", 
            choices=["m", "f", "n", ""], 
            default="",
            show_choices=False
        ) or None
        
        if Confirm.ask("Add plural form?"):
            details.plural = Prompt.ask("Plural form")
    
    # Ask for part of speech if needed
    if Confirm.ask("Add part of speech?"):
        details.part_of_speech = Prompt.ask("Part of speech (e.g., noun, verb, adj)")
    
    # Add any notes
    if Confirm.ask("Add any notes?"):
        details.notes = Prompt.ask("Notes")
    
    return details

def _add_word(word: str, translation: str, language: str, trans_lang: str = "en") -> WordEntry:
    """Helper function to add a word with translation."""
    word_entry = WordEntry(
        word=word.strip(),
        language=language,
        translations={trans_lang: translation.strip()},
        details=WordDetails()
    )
    return storage.get_storage(language).save(word_entry)

@app.command()
def import_csv():
    """Import words from a CSV file."""
    console.print("\n[bold]Import Words from CSV[/bold]")
    
    # Get CSV file path
    while True:
        csv_path = Prompt.ask("\nEnter the path to the CSV file")
        csv_path = Path(csv_path).expanduser()
        if csv_path.exists():
            break
        console.print(f"[red]File not found: {csv_path}[/red]")
    
    # Get language
    language = select_language()
    
    # Get translation language (default to English)
    trans_lang = Prompt.ask(
        "\nEnter language code for translation", 
        default="en"
    ).lower()
    
    # Process CSV file
    imported = 0
    skipped = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) < 2:
                    skipped += 1
                    continue
                    
                word = row[0].strip()
                translations = [t.strip() for t in row[1].split(';') if t.strip()]
                
                if not word or not translations:
                    skipped += 1
                    continue
                
                # Join multiple translations with comma
                translation = ", ".join(translations)
                
                try:
                    _add_word(word, translation, language, trans_lang)
                    imported += 1
                    console.print(f"[green]✓[/green] Added: {word} → {translation}")
                except Exception as e:
                    console.print(f"[red]✗ Error adding {word}: {str(e)}[/red]")
                    skipped += 1
    
    except Exception as e:
        console.print(f"[red]Error reading CSV file: {str(e)}[/red]")
        return
    
    console.print(f"\n[bold]Import complete![/bold]")
    console.print(f"Imported: {imported}")
    console.print(f"Skipped: {skipped}")

@app.command()
def add():
    """Add a new word to the dictionary."""
    console.print("\n[bold]Add a New Word[/bold]")
    
    # Get word and language
    language = select_language()
    word = Prompt.ask("\nEnter the word")
    
    # Get translation
    trans_lang = Prompt.ask(
        "\nEnter language code for translation (e.g., 'en' for English)", 
        default="en"
    ).lower()
    translation = Prompt.ask(f"Enter '{word}' in {trans_lang.upper()}")
    
    # Create word entry
    word_entry = _add_word(word, translation, language, trans_lang)
    
    # Add word details
    if Confirm.ask("\nAdd word details?"):
        word_entry.details = _prompt_word_details(language)
    
    # Add tags
    if Confirm.ask("\nAdd any tags? (e.g., noun, A1, food)"):
        tags_input = Prompt.ask("Enter tags (comma-separated)")
        word_entry.tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
    
    # Add examples
    while Confirm.ask("\nAdd an example sentence?"):
        sentence = Prompt.ask("Enter example sentence")
        translation = Prompt.ask("Enter translation")
        word_entry.examples.append(
            Example(sentence=sentence, translation=translation)
        )
    
    # Save the final entry
    storage.get_storage(language).save(word_entry)
    console.print(f"\n[green]✓ Added: {word_entry.word}[/green]")

@app.command()
def list_words(language: str = None):
    """List all words in the dictionary."""
    console.print("\n[bold]Word List[/bold]")
    
    # Get storage for the specified language or all languages
    if language:
        storages = {language: storage.get_storage(language)}
    else:
        storages = {
            lang: storage.get_storage(lang) 
            for lang in ["de", "es", "id", "taigi"]
        }
    
    # Create and display table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Language")
    table.add_column("Word")
    table.add_column("Translation")
    table.add_column("Familiarity")
    table.add_column("Last Practiced")
    
    for lang, store in storages.items():
        for word_entry in store.list():
            # Get primary translation (usually English)
            translation = word_entry.translations.get("en", "No translation")
            
            # Format familiarity
            familiarity = f"{word_entry.familiarity*100:.0f}%" if word_entry.familiarity else "-"
            
            # Format last practiced date
            last_practiced = (
                word_entry.last_practiced.strftime("%Y-%m-%d") 
                if word_entry.last_practiced 
                else "Never"
            )
            
            table.add_row(
                lang.upper(),
                word_entry.word,
                translation[:30] + ("..." if len(translation) > 30 else ""),
                familiarity,
                last_practiced
            )
    
    console.print(table)

def show_help():
    """Show available commands during the quiz."""
    console.print("\n[bold]Available Commands:[/bold]")
    console.print("  [bold]h[/bold] - Show this help")
    console.print("  [bold]s[/bold] - Skip this word")
    console.print("  [bold]?[/bold] - Get a hint")
    console.print("  [bold]u[/bold] - Mark as unfamiliar")
    console.print("  [bold]q[/bold] - Quit the quiz")
    console.print("  [bold]your answer[/bold] - Submit your answer\n")

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
    console.print("\nType 'h' during the quiz to see available commands.")
    
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
                    user_input = Prompt.ask("\nEnter your answer (number) or command")
                    
                    # Handle commands
                    if user_input.lower() == 'h':
                        show_help()
                        continue
                    elif user_input.lower() == 's':  # Skip
                        session.skip_question()
                        console.print("[yellow]Question skipped.[/yellow]")
                        break
                    elif user_input == '?':  # Hint
                        hint = session.get_hint()
                        console.print(f"[blue]{hint}[/blue]")
                        continue
                    elif user_input.lower() == 'u':  # Mark as unfamiliar
                        session.mark_current_as_unfamiliar()
                        console.print("[yellow]Word marked as unfamiliar.[/yellow]")
                        continue
                    elif user_input.lower() == 'q':  # Quit
                        if Confirm.ask("\nAre you sure you want to quit the quiz?"):
                            console.print("\n[bold]Quiz aborted.[/bold]")
                            return
                        continue
                    
                    # Process answer
                    try:
                        answer_idx = int(user_input) - 1
                        if 0 <= answer_idx < len(question.options):
                            answer = question.options[answer_idx]
                            is_correct = session.submit_answer(answer)
                            
                            if is_correct:
                                console.print("[green]✓ Correct![/green]")
                            else:
                                console.print(f"[red]✗ Incorrect. The correct answer is: {question.correct_answer}[/red]")
                            break
                        console.print(f"[red]Please enter a number between 1 and {len(question.options)}[/red]")
                    except ValueError:
                        console.print("[red]Please enter a valid number or command.[/red]")
                        
                except KeyboardInterrupt:
                    if Confirm.ask("\nAre you sure you want to quit the quiz?"):
                        console.print("\n[bold]Quiz aborted.[/bold]")
                        return
                    continue
        
        else:  # spelling mode
            while True:
                user_input = Prompt.ask("\nType your answer or command")
                
                # Handle commands
                if user_input.lower() == 'h':
                    show_help()
                    continue
                elif user_input.lower() == 's':  # Skip
                    session.skip_question()
                    console.print("[yellow]Question skipped.[/yellow]")
                    break
                elif user_input == '?':  # Hint
                    hint = session.get_hint()
                    console.print(f"[blue]{hint}[/blue]")
                    continue
                elif user_input.lower() == 'u':  # Mark as unfamiliar
                    session.mark_current_as_unfamiliar()
                    console.print("[yellow]Word marked as unfamiliar.[/yellow]")
                    continue
                elif user_input.lower() == 'q':  # Quit
                    if Confirm.ask("\nAre you sure you want to quit the quiz?"):
                        console.print("\n[bold]Quiz aborted.[/bold]")
                        return
                    continue
                
                # Process answer
                is_correct = session.submit_answer(user_input)
                if is_correct:
                    console.print("[green]✓ Correct![/green]")
                else:
                    console.print(f"[red]✗ Incorrect. The correct answer is: {question.correct_answer}[/red]")
                break
    
    # Show results
    results = session.get_results()
    console.print("\n[bold]Quiz Complete![/bold]")
    console.print(f"Score: {results['correct_answers']}/{results['total_questions']} ({results['score_percentage']:.1f}%)")
    console.print(f"Time: {results['time_taken_seconds']:.1f} seconds")
    
    # Show skipped questions and unfamiliar words if any
    skipped = session.get_skipped_questions()
    if skipped:
        console.print("\n[yellow]Skipped words:[/yellow]")
        for q in skipped:
            console.print(f"- {q.word.word} ({q.word.translations.get('en', 'No translation')})")
    
    unfamiliar = session.get_unfamiliar_words()
    if unfamiliar:
        console.print("\n[yellow]Words marked as unfamiliar:[/yellow]")
        for word in unfamiliar:
            console.print(f"- {word.word} ({word.translations.get('en', 'No translation')})")
    
    # Save unfamiliar words to a list for review
    if unfamiliar:
        review_file = Path.home() / ".config" / "ekiti" / "unfamiliar_words.txt"
        review_file.parent.mkdir(parents=True, exist_ok=True)
        with open(review_file, "a", encoding="utf-8") as f:
            for word in unfamiliar:
                f.write(f"{word.word} - {word.translations.get('en', 'No translation')}\n")
        console.print(f"\n[green]Unfamiliar words have been saved to {review_file}[/green]")

@app.callback()
def main():
    """Ekiti - A flashcard app for language learning (會記得)."""
    pass

if __name__ == "__main__":
    app()
