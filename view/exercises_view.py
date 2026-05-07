import customtkinter as ctk


class ExercisesView(ctk.CTkFrame):
    def __init__(self, parent, username, session_data):
        super().__init__(parent)
        self.username = username
        self.session_data = session_data
        self.on_back = None
        self.on_add_exercise = None
        self.on_edit_exercise = None  # Callback for editing an exercise

        # Header with back button
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", pady=10, padx=10)

        self.back_button = ctk.CTkButton(header_frame, text="< Back", width=80, command=self.go_back)
        self.back_button.pack(side="left")

        self.title = ctk.CTkLabel(
            header_frame,
            text=f"Exercises - Session #{session_data['session_number']}",
            font=("Arial", 18, "bold")
        )
        self.title.pack(side="left", padx=10)

        # Scrollable container for exercises
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add exercise button
        self.add_button = ctk.CTkButton(self, text="Add exercise", command=self.open_exercise_form)
        self.add_button.pack(pady=10)

    def display_exercises(self, exercises):
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display each exercise
        for exercise in exercises:
            button = ctk.CTkButton(
                self.scrollable_frame,
                text=self.get_exercise_text(exercise),
                command=lambda e=exercise: self.edit_exercise(e)
            )
            button.pack(fill="x", pady=5)

    def get_exercise_text(self, exercise):
        if exercise["exercise_type"] == "cardio":
            if exercise["name"] == "Swimming":
                return f"{exercise['name']} - {exercise['time']} min"

            text = f"{exercise['name']} - Level {exercise['level']} - {exercise['time']} min"

            if exercise["name"] == "Treadmill":
                text += f" - Incline {exercise['incline']}"

            return text

        return f"{exercise['name']} - {exercise['weight']} kg - {exercise['reps']} reps"

    def open_exercise_form(self):
        self.form_window = ctk.CTkToplevel(self)
        self.form_window.title("Add exercise")
        self.form_window.geometry("360x420")

        self.form_frame = ctk.CTkFrame(self.form_window)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.exercise_type = ctk.StringVar(value="Cardio")

        type_label = ctk.CTkLabel(self.form_frame, text="Exercise type")
        type_label.pack(anchor="w")

        self.type_menu = ctk.CTkOptionMenu(
            self.form_frame,
            values=["Cardio", "Weights"],
            variable=self.exercise_type,
            command=lambda value: self.draw_exercise_fields()
        )
        self.type_menu.pack(fill="x", pady=(5, 15))

        self.fields_frame = ctk.CTkFrame(self.form_frame)
        self.fields_frame.pack(fill="both", expand=True)

        self.draw_exercise_fields()

    def draw_exercise_fields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        if self.exercise_type.get() == "Cardio":
            self.draw_cardio_fields()
        else:
            self.draw_weight_fields()

    def draw_cardio_fields(self):
        current_cardio = "Treadmill"

        if hasattr(self, "cardio_name"):
            current_cardio = self.cardio_name.get()

        self.cardio_name = ctk.StringVar(value=current_cardio)

        name_label = ctk.CTkLabel(self.fields_frame, text="Cardio exercise")
        name_label.pack(anchor="w")

        self.cardio_menu = ctk.CTkOptionMenu(
            self.fields_frame,
            values=["Treadmill", "Bike", "Stairmaster", "Elliptical", "Rowing machine", "Swimming"],
            variable=self.cardio_name,
            command=lambda value: self.draw_exercise_fields()
        )
        self.cardio_menu.pack(fill="x", pady=(5, 10))

        if self.cardio_name.get() == "Swimming":
            self.level_entry = None
        else:
            self.level_entry = self.create_entry("Level")

        self.time_entry = self.create_entry("Time")

        self.incline_frame = ctk.CTkFrame(self.fields_frame)
        self.incline_frame.pack(fill="x")
        self.show_incline_field()

        save_button = ctk.CTkButton(self.fields_frame, text="Save", command=self.save_cardio_exercise)
        save_button.pack(pady=15)

    def show_incline_field(self):
        for widget in self.incline_frame.winfo_children():
            widget.destroy()

        if self.cardio_name.get() == "Treadmill":
            label = ctk.CTkLabel(self.incline_frame, text="Incline")
            label.pack(anchor="w")

            self.incline_entry = ctk.CTkEntry(self.incline_frame)
            self.incline_entry.pack(fill="x", pady=(5, 10))
        else:
            self.incline_entry = None

    def draw_weight_fields(self):
        self.name_entry = self.create_entry("Exercise name")
        self.weight_entry = self.create_entry("Weight")
        self.reps_entry = self.create_entry("Reps")

        save_button = ctk.CTkButton(self.fields_frame, text="Save", command=self.save_weight_exercise)
        save_button.pack(pady=15)

    def create_entry(self, label_text):
        label = ctk.CTkLabel(self.fields_frame, text=label_text)
        label.pack(anchor="w")

        entry = ctk.CTkEntry(self.fields_frame)
        entry.pack(fill="x", pady=(5, 10))

        return entry

    def save_cardio_exercise(self):
        exercise = {
            "exercise_type": "cardio",
            "name": self.cardio_name.get(),
            "level": "0",
            "time": self.time_entry.get(),
            "incline": "0"
        }

        if self.level_entry:
            exercise["level"] = self.level_entry.get()

        if self.incline_entry:
            exercise["incline"] = self.incline_entry.get()

        self.save_exercise(exercise)

    def save_weight_exercise(self):
        exercise = {
            "exercise_type": "weights",
            "name": self.name_entry.get(),
            "weight": self.weight_entry.get(),
            "reps": self.reps_entry.get()
        }

        self.save_exercise(exercise)

    def save_exercise(self, exercise):
        if self.on_add_exercise:
            self.form_window.destroy()
            self.on_add_exercise(exercise)

    def go_back(self):
        if self.on_back:
            self.on_back()

    def edit_exercise(self, exercise):
        if self.on_edit_exercise:
            self.on_edit_exercise(exercise)
        else:
            print("To be implemented")
