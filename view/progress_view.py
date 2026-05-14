import customtkinter as ctk


class ProgressView(ctk.CTkFrame):
    def __init__(self, parent, exercises=None, progress_entries=None):
        super().__init__(parent)
        self.exercises = exercises or []
        self.progress_entries = progress_entries or []
        self.selected_exercise = ctk.StringVar()
        self.on_exercise_selected = None

        self.build_ui()
        self.display_exercises(self.exercises)
        self.display_progress(self.progress_entries)

    def build_ui(self):
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        self.title = ctk.CTkLabel(
            self.container,
            text="MY PROGRESS",
            font=("Arial", 24, "bold")
        )
        self.title.pack(pady=(0, 20))

        self.exercise_label = ctk.CTkLabel(self.container, text="Exercise")
        self.exercise_label.pack(anchor="w")

        self.exercise_menu = ctk.CTkOptionMenu(
            self.container,
            values=["No exercises available"],
            variable=self.selected_exercise,
            command=self.handle_exercise_selected
        )
        self.exercise_menu.pack(fill="x", pady=(5, 20))
        self.exercise_menu.configure(state="disabled")

        self.list_frame = ctk.CTkFrame(self.container)
        self.list_frame.pack(fill="both", expand=True)

    def display_exercises(self, exercises):
        self.exercises = exercises

        if not exercises:
            self.selected_exercise.set("No exercises available")
            self.exercise_menu.configure(values=["No exercises available"], state="disabled")
            return

        exercise_names = []

        for exercise in exercises:
            exercise_names.append(exercise["name"])

        self.selected_exercise.set(exercise_names[0])
        self.exercise_menu.configure(values=exercise_names, state="normal")

    def display_progress(self, progress_entries):
        self.progress_entries = progress_entries

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not progress_entries:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No progress data yet"
            )
            empty_label.pack(pady=20)
            return

        header = ctk.CTkFrame(self.list_frame)
        header.pack(fill="x", pady=(0, 10))

        date_header = ctk.CTkLabel(header, text="Date", font=("Arial", 14, "bold"))
        date_header.pack(side="left", padx=10, pady=10)

        weight_header = ctk.CTkLabel(header, text="Max weight (kg)", font=("Arial", 14, "bold"))
        weight_header.pack(side="right", padx=10, pady=10)

        for entry in progress_entries:
            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", pady=5)

            date_label = ctk.CTkLabel(row, text=entry["date"])
            date_label.pack(side="left", padx=10, pady=10)

            weight_label = ctk.CTkLabel(row, text=entry["weight"])
            weight_label.pack(side="right", padx=10, pady=10)

    def handle_exercise_selected(self, selected_name):
        if not self.on_exercise_selected:
            return

        for exercise in self.exercises:
            if exercise["name"] == selected_name:
                self.on_exercise_selected(exercise)
                break
