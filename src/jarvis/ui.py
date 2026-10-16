import queue
import threading

from datetime import datetime

import customtkinter as ctk
import speech_recognition as sr

from .assistant import Assistant
from .speech import SpeechService


BG = "#080D13"
PANEL = "#101922"
PANEL_LIGHT = "#15232D"
BORDER = "#223440"
ACCENT = "#62E5E0"
TEXT = "#E7F0F3"
MUTED = "#8CA0AA"


class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=BG)
        self.title("JARVIS | Personal Assistant")
        self.geometry("1180x760")
        self.minsize(940, 640)
        self.assistant = Assistant()
        self.speech = SpeechService()
        self.events = queue.Queue()
        self.speech_jobs = queue.Queue()
        self.listening = False
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()
        self._add_message(
            "JARVIS",
            "Good evening. I'm online and ready. Try asking for the time,"
            "opening a website, or searching the web."
        )
        threading.Thread(
            target=self._speech_worker,
            daemon=True
        ).start()
        self._poll_events()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#0B1219"
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        ctk.CTkLabel(
            sidebar,
            text="◉  J A R V I S",
            text_color=ACCENT,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=24, pady=(28, 8))
        ctk.CTkLabel(
            sidebar,
            text="PERSONAL INTELLIGENCE",
            text_color=MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=26, pady=(0, 34))
        ctk.CTkLabel(
            sidebar,
            text="WORKSPACE",
            text_color="#627680",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=25, pady=(0, 10))
        ctk.CTkLabel(
            sidebar,
            text="◈   Assistant",
            height=40,
            corner_radius=8,
            fg_color="#14272E",
            text_color=ACCENT,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).pack(fill="x", padx=14)
        ctk.CTkFrame(
            sidebar,
            height=1,
            fg_color=BORDER,
        ).pack(fill="x", padx=20, pady=22)
        ctk.CTkLabel(
            sidebar,
            text="SYSTEM",
            text_color="#627680",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=25, pady=(0, 12))
        ctk.CTkLabel(
            sidebar,
            text="●  Core online",
            text_color="#8EDDB2",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=25, pady=5)
        ctk.CTkLabel(
            sidebar,
            text="●  Voice ready",
            text_color="#8EDDB2",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=25, pady=5)
        ctk.CTkLabel(
            sidebar,
            text="LOCAL PROTOTYPE  ·  V1",
            text_color="#536671",
            font=("Segoe UI", 9),
        ).pack(side="bottom", anchor="w", padx=22, pady=20)

    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=28, pady=24)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        today = datetime.now().strftime("%A  ·  %d %B %Y").upper()
        ctk.CTkLabel(
            header,
            text=today,
            text_color=MUTED,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text="Good evening, Harsh.",
            text_color=TEXT,
            font=("Segoe UI", 29, "bold"),
        ).pack(anchor="w", pady=(6, 2))
        ctk.CTkLabel(
            header,
            text="Your personal assistant is ready when you are.",
            text_color=MUTED,
            font=("Segoe UI", 12),
        ).pack(anchor="w")
        body = ctk.CTkFrame(main, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, minsize=235)
        body.grid_rowconfigure(0, weight=1)
        self._build_chat(body)
        self._build_info(body)

    def _build_chat(self, parent):
        chat_card = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=14,
        )
        chat_card.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        chat_card.grid_columnconfigure(0, weight=1)
        chat_card.grid_rowconfigure(1, weight=1)
        top = ctk.CTkFrame(chat_card, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=16)
        ctk.CTkLabel(
            top,
            text="CONVERSATION",
            text_color=TEXT,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        self.status = ctk.CTkLabel(
            top,
            text="●  READY",
            text_color="#8EDDB2",
            font=("Segoe UI", 9, "bold"),
        )
        self.status.pack(side="right")
        self.history = ctk.CTkScrollableFrame(
            chat_card,
            fg_color="#0B1219",
            corner_radius=10,
        )
        self.history.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 12),
        )
        chips = ctk.CTkFrame(chat_card, fg_color="transparent")
        chips.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 8))
        for label, command in [
            ("What's the time?", "what time is it"),
            ("Open YouTube", "open youtube"),
            ("Help", "help"),
        ]:
            ctk.CTkButton(
                chips,
                text=label,
                width=112,
                height=30,
                fg_color=PANEL_LIGHT,
                hover_color="#203640",
                text_color="#B8C9CF",
                font=("Segoe UI", 10),
                command=lambda value=command: self._submit_text(value),
            ).pack(side="left", padx=(0, 7))
        entry_row = ctk.CTkFrame(chat_card, fg_color="transparent")
        entry_row.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))
        entry_row.grid_columnconfigure(0, weight=1)
        self.entry = ctk.CTkEntry(
            entry_row,
            height=44,
            placeholder_text="Message JARVIS or try “search for space news”…",
            fg_color="#0B1219",
            border_color=BORDER,
            text_color=TEXT,
            corner_radius=9,
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.entry.bind("<Return>", self._submit_entry)
        self.mic_button = ctk.CTkButton(
            entry_row,
            text="🎙",
            width=44,
            height=44,
            fg_color=PANEL_LIGHT,
            hover_color="#203640",
            command=self._start_listening,
        )
        self.mic_button.grid(row=0, column=1, padx=(0, 8))
        ctk.CTkButton(
            entry_row,
            text="Send  ↗",
            width=90,
            height=44,
            fg_color="#49CFCB",
            hover_color="#69E7E1",
            text_color="#071417",
            font=("Segoe UI", 11, "bold"),
            command=lambda: self._submit_text(self.entry.get()),
        ).grid(row=0, column=2)

    def _build_info(self, parent):
        info = ctk.CTkFrame(parent, fg_color="transparent")
        info.grid(row=0, column=1, sticky="nsew")
        info.grid_columnconfigure(0, weight=1)
        self._info_card(info, "SYSTEM STATUS", [
            ("Assistant core", "READY"),
            ("Voice output", "OFFLINE TTS"),
            ("Speech input", "ONLINE"),
        ], row=0)
        self._info_card(info, "QUICK COMMANDS", [
            ("Tell me the time", "what time is it"),
            ("Tell me the date", "what is the date"),
            ("Search the web", "search for Python projects"),
            ("Open Google", "open google"),
        ], row=1)
        note = ctk.CTkFrame(
            info,
            fg_color="#102126",
            border_color="#25464B",
            border_width=1,
            corner_radius=12,
        )
        note.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        ctk.CTkLabel(
            note,
            text="VOICE PRIVACY",
            text_color=ACCENT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=14, pady=(13, 5))
        ctk.CTkLabel(
            note,
            text="Voice recognition uses an online service. "
                 "Your microphone is only used when you press the mic button.",
            text_color="#A9BBC2",
            font=("Segoe UI", 10),
            wraplength=195,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 14))

    def _info_card(self, parent, title, rows, row):
        card = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=12,
        )
        card.grid(row=row, column=0, sticky="ew", pady=(0, 14))
        ctk.CTkLabel(
            card,
            text=title,
            text_color=MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))
        for label, value in rows:
            line = ctk.CTkFrame(card, fg_color="transparent")
            line.pack(fill="x", padx=14, pady=5)
            if title == "QUICK COMMANDS":
                ctk.CTkButton(
                    line,
                    text=label,
                    anchor="w",
                    fg_color="transparent",
                    hover_color=PANEL_LIGHT,
                    text_color="#C5D3D8",
                    font=("Segoe UI", 10),
                    command=lambda text=value: self._submit_text(text),
                ).pack(fill="x")
            else:
                ctk.CTkLabel(
                    line,
                    text=label,
                    text_color="#B8C6CC",
                    font=("Segoe UI", 10),
                ).pack(side="left")
                ctk.CTkLabel(
                    line,
                    text=value,
                    text_color="#8EDDB2",
                    font=("Segoe UI", 8, "bold"),
                ).pack(side="right")
        ctk.CTkFrame(card, height=8, fg_color="transparent").pack()

    def _add_message(self, speaker, text):
        is_user = speaker == "YOU"
        row = ctk.CTkFrame(self.history, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=6)
        bubble = ctk.CTkFrame(
            row,
            fg_color="#173039" if is_user else "#121E27",
            corner_radius=10,
        )
        bubble.pack(anchor="e" if is_user else "w", padx=(45, 0) if is_user else (0, 45))
        ctk.CTkLabel(
            bubble,
            text=speaker,
            text_color=ACCENT if not is_user else "#A8B8BE",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=12, pady=(9, 1))
        ctk.CTkLabel(
            bubble,
            text=text,
            text_color=TEXT,
            font=("Segoe UI", 11),
            wraplength=480,
            justify="left",
        ).pack(anchor="w", padx=12, pady=(0, 10))
        self.history.after(80, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        self.history._parent_canvas.yview_moveto(1.0)

    def _submit_entry(self, _event=None):
        self._submit_text(self.entry.get())

    def _submit_text(self, text):
        text = text.strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._add_message("YOU", text)
        reply = self.assistant.respond(text)
        self._add_message("JARVIS", reply)
        self.speech_jobs.put(reply)
        if self.assistant.is_exit_command(text):
            self.after(1800, self.destroy)

    def _start_listening(self):
        if self.listening:
            return
        self.listening = True
        self.status.configure(text="●  LISTENING…", text_color=ACCENT)
        self.mic_button.configure(state="disabled", text="…")
        threading.Thread(
            target=self._listen_worker,
            daemon=True,
        ).start()

    def _listen_worker(self):
        try:
            text = self.speech.listen_once()
            self.events.put(("heard", text))
        except sr.WaitTimeoutError:
            self.events.put(("error", "I didn't hear anything. Try again."))
        except sr.UnknownValueError:
            self.events.put(("error", "I couldn't understand that. Try again."))
        except sr.RequestError:
            self.events.put(("error", "Speech service unavailable. Check internet."))
        except OSError:
            self.events.put(("error", "Microphone unavailable. Check permissions."))
        except Exception as error:
            self.events.put(("error", f"Voice input error: {error}"))

    def _speech_worker(self):
        while True:
            text = self.speech_jobs.get()
            try:
                self.speech.speak(text)
            except Exception as error:
                self.events.put(("error", f"Speech output error: {error}"))

    def _poll_events(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "heard":
                    self.listening = False
                    self.status.configure(text="●  READY", text_color="#8EDDB2")
                    self.mic_button.configure(state="normal", text="🎙")
                    self._submit_text(value)
                else:
                    self.listening = False
                    self.status.configure(text="●  READY", text_color="#8EDDB2")
                    self.mic_button.configure(state="normal", text="🎙")
                    self._add_message("JARVIS", value)
        except queue.Empty:
            pass
        self.after(120, self._poll_events)