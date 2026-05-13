import customtkinter as ctk


class ExerciseDetailView(ctk.CTkFrame):
    """
    Detail screen for one exercise.
    It can display the exercise or turn the fields into inputs for editing.
    """

    def __init__(self, parent, exercise, saved_exercises=None):
        super().__init__(parent)

        # Stores the exercise currently being displayed
        self.exercise = exercise
        self.saved_exercises = saved_exercises or []
        # Controls whether the screen is in normal mode or edit mode
        self.edit_mode = False
        # Stores the entry widgets created while editing
        self.entries = {}

        # Callbacks assigned by the parent view
        self.on_back = None
        self.on_update_exercise = None
        self.on_delete_exercise = None

        self.build_ui()
        self.show_view_mode()

    def build_ui(self):
        # Main title with the exercise name
        self.title = ctk.CTkLabel(
            self,
            text=self.exercise["name"],
            font=("Arial", 24, "bold")
        )
        self.title.pack(pady=(10, 20))

        # This frame is rebuilt when switching between view mode and edit mode
        self.fields_frame = ctk.CTkFrame(self)
        self.fields_frame.pack(fill="x", padx=20, pady=10)

        # These buttons stay visible in both modes
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=20)

        self.edit_button = ctk.CTkButton(
            self.buttons_frame,
            text="Edit",
            command=self.toggle_edit_mode
        )
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame,
            text="Delete",
            command=self.delete_exercise
        )
        self.delete_button.pack(side="left", padx=5)

        self.back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.go_back
        )
        self.back_button.pack(pady=10)

    def show_view_mode(self):
        # Rebuild the screen using plain labels
        self.clear_fields()

        for label_text, key, value in self.get_fields():
            row = ctk.CTkFrame(self.fields_frame)
            row.pack(fill="x", pady=5)

            label = ctk.CTkLabel(row, text=f"{label_text}:", font=("Arial", 14, "bold"))
            label.pack(side="left", padx=10)

            value_label = ctk.CTkLabel(row, text=str(value), font=("Arial", 14))
            value_label.pack(side="left", padx=10)

    def show_edit_mode(self):
        # Rebuild the screen using entry widgets
        self.clear_fields()

        for label_text, key, value in self.get_fields():
            if key == "exercise_type":
                # The exercise type is shown but not edited here
                continue

            row = ctk.CTkFrame(self.fields_frame)
            row.pack(fill="x", pady=5)

            label = ctk.CTkLabel(row, text=f"{label_text}:")
            label.pack(side="left", padx=10)

            if self.exercise["exercise_type"] == "weights" and key == "name":
                self.draw_weight_name_menu(row, value)
                continue

            entry = ctk.CTkEntry(row)
            entry.insert(0, str(value))
            entry.pack(side="left", padx=10)

            self.entries[key] = entry

    def draw_weight_name_menu(self, row, current_value):
        weight_options = []

        for exercise in self.saved_exercises:
            weight_options.append(exercise["name"])

        self.selected_weight_exercise = ctk.StringVar()

        if weight_options:
            if current_value in weight_options:
                self.selected_weight_exercise.set(current_value)
            else:
                self.selected_weight_exercise.set(weight_options[0])

            self.weight_name_menu = ctk.CTkOptionMenu(
                row,
                values=weight_options,
                variable=self.selected_weight_exercise
            )
            self.weight_name_menu.pack(side="left", padx=10)
        else:
            self.selected_weight_exercise.set("")
            self.weight_name_menu = ctk.CTkOptionMenu(
                row,
                values=["No saved exercises"],
                variable=self.selected_weight_exercise
            )
            self.weight_name_menu.pack(side="left", padx=10)
            self.weight_name_menu.configure(state="disabled")

    def get_fields(self):
        # Returns the fields that should appear depending on the exercise type
        if self.exercise["exercise_type"] == "cardio":
            fields = [
                ("Type", "exercise_type", "Cardio"),
                ("Name", "name", self.exercise["name"]),
                ("Time (min)", "time", self.exercise["time"])
            ]

            if self.exercise["name"] != "Swimming":
                fields.append(("Level", "level", self.exercise["level"]))

            if self.exercise["name"] == "Treadmill":
                fields.append(("Incline", "incline", self.exercise["incline"]))

            return fields

        return [
            ("Type", "exercise_type", "Weights"),
            ("Name", "name", self.exercise["name"]),
            ("Weight (kg)", "weight", self.exercise["weight"]),
            ("Reps", "reps", self.exercise["reps"])
        ]

    def toggle_edit_mode(self):
        # Switch between normal display and editable display
        if not self.edit_mode:
            self.edit_mode = True
            self.edit_button.configure(text="Save")
            self.show_edit_mode()
        else:
            if self.save_changes():
                self.edit_mode = False
                self.edit_button.configure(text="Edit")
                self.show_view_mode()

    def save_changes(self):
        updated_exercise = self.exercise.copy()

        for key, entry in self.entries.items():
            # Read all the new values entered by the user
            updated_exercise[key] = entry.get()

        if self.exercise["exercise_type"] == "weights":
            updated_exercise["name"] = self.selected_weight_exercise.get()

        if self.on_update_exercise:
            saved_exercise = self.on_update_exercise(updated_exercise)

            if not saved_exercise:
                return False

            # Only update the local screen after the controller accepts the data
            self.exercise = saved_exercise
            self.title.configure(text=self.exercise["name"])

        return True

    def delete_exercise(self):
        if self.on_delete_exercise:
            # The parent view decides what to do with the delete action
            self.on_delete_exercise(self.exercise)

    def go_back(self):
        if self.on_back:
            self.on_back()

    def clear_fields(self):
        # Remove old labels or entries before drawing the screen again
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.entries.clear()
