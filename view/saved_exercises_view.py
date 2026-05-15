import customtkinter as ctk


class SavedExercisesView(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        self.on_add_exercise = None
        self.on_edit_exercise = None
        self.on_delete_exercise = None
        self.on_search_exercises = None

        # Stores the exercises currently shown on screen
        self.saved_exercises = []

        self.build_ui()

    def build_ui(self):
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        self.title = ctk.CTkLabel(
            self.container,
            text="MY EXERCISES",
            font=("Arial", 24, "bold")
        )
        self.title.pack(pady=(0, 20))

        self.search_frame = ctk.CTkFrame(self.container)
        self.search_frame.pack(fill="x", pady=(0, 20))

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search exercises by name"
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self.search_exercises())
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_exercises())

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            command=self.search_exercises
        )
        self.search_button.pack(side="left")

        self.scrollable_frame = ctk.CTkScrollableFrame(self.container)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.add_frame = ctk.CTkFrame(self.container)
        self.add_frame.pack(fill="x", pady=(20, 0))

        self.name_label = ctk.CTkLabel(self.add_frame, text="Exercise name")
        self.name_label.pack(anchor="w")

        self.name_entry = ctk.CTkEntry(self.add_frame)
        self.name_entry.pack(fill="x", pady=(5, 10))

        self.add_button = ctk.CTkButton(
            self.add_frame,
            text="Add exercise",
            command=self.add_exercise
        )
        self.add_button.pack()

    def display_exercises(self, saved_exercises):
        self.saved_exercises = saved_exercises

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not saved_exercises:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No saved exercises yet"
            )
            empty_label.pack(pady=20)
            return

        for exercise in saved_exercises:
            row = ctk.CTkFrame(self.scrollable_frame)
            row.pack(fill="x", pady=5)

            name_label = ctk.CTkLabel(
                row,
                text=exercise["name"],
                anchor="w"
            )
            name_label.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

            menu = ctk.CTkOptionMenu(
                row,
                values=["Edit", "Delete"],
                width=40,
                command=None
            )
            menu.configure(command=lambda action, e=exercise, m=menu: self.handle_exercise_action(action, e, m))
            menu.set("")
            menu.pack(side="right", padx=10)

    def set_search_text(self, search_text):
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, search_text)

    def search_exercises(self):
        if self.on_search_exercises:
            self.on_search_exercises(self.search_entry.get())

    def add_exercise(self):
        exercise_name = self.name_entry.get()

        if self.on_add_exercise:
            if self.on_add_exercise(exercise_name):
                if self.name_entry.winfo_exists():
                    self.name_entry.delete(0, "end")

    def handle_exercise_action(self, action, exercise, menu):
        # Reset the visible text so the control keeps looking like an arrow-only menu
        menu.set("")

        if action == "Edit" and self.on_edit_exercise:
            self.open_edit_window(exercise)

        if action == "Delete" and self.on_delete_exercise:
            self.on_delete_exercise(exercise)

    def open_edit_window(self, exercise):
        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.title("Edit exercise")
        self.edit_window.geometry("320x160")
        self.edit_window.transient(self)
        self.edit_window.lift()
        self.edit_window.focus()
        self.edit_window.grab_set()

        self.edit_frame = ctk.CTkFrame(self.edit_window)
        self.edit_frame.pack(fill="both", expand=True, padx=20, pady=20)

        label = ctk.CTkLabel(self.edit_frame, text="Exercise name")
        label.pack(anchor="w")

        self.edit_entry = ctk.CTkEntry(self.edit_frame)
        self.edit_entry.insert(0, exercise["name"])
        self.edit_entry.pack(fill="x", pady=(5, 15))

        save_button = ctk.CTkButton(
            self.edit_frame,
            text="Save",
            command=lambda: self.save_edited_exercise(exercise)
        )
        save_button.pack()

    def save_edited_exercise(self, exercise):
        new_name = self.edit_entry.get()

        if self.on_edit_exercise:
            if self.on_edit_exercise(exercise, new_name):
                self.edit_window.destroy()
