import customtkinter as ctk

class ExercisesView(ctk.CTkFrame):
    def __init__(self, parent, username, session_data):
        super().__init__(parent)
        self.username = username
        self.session_data = session_data
        self.on_back = None
        self.on_edit_exercise = None  # Callback for editing an exercise

        # Header with back button
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", pady=10, padx=10)

        self.back_button = ctk.CTkButton(header_frame, text="← Atrás", width=80, command=self.go_back)
        self.back_button.pack(side="left")

        self.title = ctk.CTkLabel(header_frame, text=f"Ejercicios - Sesión #{session_data['session_number']}", font=("Arial", 18, "bold"))
        self.title.pack(side="left", padx=10)

        # Scrollable container for exercises
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def display_exercises(self, exercises):
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display each exercise
        for ex in exercises:
            btn = ctk.CTkButton(
                self.scrollable_frame,
                text=ex["name"],
                command=lambda e=ex: self.edit_exercise(e)
            )
            btn.pack(fill="x", pady=5)

    def go_back(self):
        if self.on_back:
            self.on_back()

    def edit_exercise(self, exercise):
        if self.on_edit_exercise:
            self.on_edit_exercise(exercise)
        else:
            print("To be implemented")