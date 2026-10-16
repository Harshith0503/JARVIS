from datetime import datetime
from urllib.parse import quote_plus
import webbrowser


def handle_command(command: str) -> str:
    """Run a supported command and return JARVIS's reply."""
    text = command.strip().lower()

    if not text:
        return "I didn't catch a command. Try again."

    if any(greeting in text for greeting in ("hello", "hi jarvis", "hey jarvis")):
        return "Hello! I'm ready to help."

    if "time" in text:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}."

    if "date" in text or "what day" in text:
        today = datetime.now().strftime("%A, %B %d")
        return f"Today is {today}."

    if "open youtube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    
    if "open google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    if text.startswith("search for "):
        query = command.strip()[len("search for "):]
        webbrowser.open(
            "https://www.google.com/search?q=" + quote_plus(query)
        )
        return f"Searching the web for {query}."

    if text in {"help", "what can you do"}:
        return (
            "I can tell you the time and date, open Google or YouTube, "
            "and search the web. More skills are coming."
        )

    if text in {"stop", "quit", "exit", "goodbye"}:
        return "Goodbye!"

    return (
        "I don't know that command yet. Say help to hear what I can do."
    )