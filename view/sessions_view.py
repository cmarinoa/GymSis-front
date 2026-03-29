import customtkinter as ctk
from datetime import datetime

class SessionsView(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        self.on_session_selected = None
        self.on_add_session = None  # Callback for adding a new session

        # Title
        self.title = ctk.CTkLabel(self, text=f"{self.username}'s sessions", font=("Arial", 20, "bold"))
        self.title.pack(pady=10)

        # Scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add session button
        self.add_button = ctk.CTkButton(self, text="Add session", command=self.add_session)
        self.add_button.pack(pady=10)

    def display_sessions(self, sessions):
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display each session as a button
        for session in sessions:
            btn = ctk.CTkButton(
                self.scrollable_frame,
                text=f"Session #{session['session_number']} - {session['date']}",
                command=lambda s=session: self.on_session_selected(s)  # callback
            )
            btn.pack(fill="x", pady=5)

    def add_session(self):
        if self.on_add_session:
            self.on_add_session()
        else:
            print("To be implemented")