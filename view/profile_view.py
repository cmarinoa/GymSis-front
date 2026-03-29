import customtkinter as ctk


class ProfileView(ctk.CTkFrame):
    """
    Profile screen.
    Displays user information (initially empty) and allows editing.
    """

    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username

        # Track mode (view vs edit)
        self.edit_mode = False

        # Store references to widgets
        self.value_labels = {}
        self.entries = {}

        self.build_ui()
        self.show_view_mode()

    """Creates static UI layout"""
    def build_ui(self):


        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        # Title
        self.title = ctk.CTkLabel(
            self.container,
            text="MY PROFILE",
            font=("Arial", 24, "bold")
        )
        self.title.pack(pady=(0, 20))

        # Fields definition (label text + key)
        self.fields = [
            ("Username", "username"),
            ("Height", "height"),
            ("Weight", "weight"),
            ("Chest", "chest"),
            ("Thighs", "thighs"),
            ("Waist", "waist"),
            ("Hips", "hips")
        ]

        # Frame for fields
        self.fields_frame = ctk.CTkFrame(self.container)
        self.fields_frame.pack(fill="both", expand=True)

        # Edit button
        self.edit_button = ctk.CTkButton(
            self.container,
            text="Edit",
            command=self.toggle_edit_mode
        )
        self.edit_button.pack(pady=20)

    """VIED MODE: Displays values"""
    def show_view_mode(self):

        self.clear_fields()

        for label_text, key in self.fields:
            row = ctk.CTkFrame(self.fields_frame)
            row.pack(fill="x", pady=5)

            label = ctk.CTkLabel(row, text=f"{label_text}:")
            label.pack(side="left")

            # Username shows actual value, others empty
            value = self.username if key == "username" else ""

            value_label = ctk.CTkLabel(row, text=value)
            value_label.pack(side="left", padx=10)

            self.value_labels[key] = value_label

    """EDIT MODE: Displays input fields for editing"""
    def show_edit_mode(self):

        self.clear_fields()

        for label_text, key in self.fields:
            row = ctk.CTkFrame(self.fields_frame)
            row.pack(fill="x", pady=5)

            label = ctk.CTkLabel(row, text=f"{label_text}:")
            label.pack(side="left")

            entry = ctk.CTkEntry(row)

            # Username prefilled, others empty
            if key == "username":
                entry.insert(0, self.username)

            entry.pack(side="left", padx=10)

            self.entries[key] = entry

    """
    Toggle between edit mode and view mode
    """
    def toggle_edit_mode(self):

        self.edit_mode = not self.edit_mode

        if self.edit_mode:
            self.edit_button.configure(text="Save")
            self.show_edit_mode()
        else:
            self.edit_button.configure(text="Edit")
            self.show_view_mode()

    """Helper method that removes all field widgets"""
    def clear_fields(self):

        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.value_labels.clear()
        self.entries.clear()