import customtkinter as ctk
from view.sessions_view import SessionsView
from view.profile_view import ProfileView
from view.exercises_view import ExercisesView

class MenuView(ctk.CTkFrame):
    """
    This class is the one the user navigates to after a successful login
    It acts as a layout manager.
    """
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username

        # store session callback
        self._session_callback = None

        # Callbacks assigned by controller
        # Allows the view to communicate user actions

        self.on_logout = None
        self.on_open_sessions = None
        self.on_open_profile = None

        # State of the side menu (default closed)
        self.menu_open = False
        self.menu_width = 200

        # Build UI method
        self.build_ui()

        # Create menu buttons
        self.setup_menu()


    """
    Creates the layout structure:
    1. Top bar
    2. Hamburger menu
    3. Dynamic content container
    """
    def build_ui(self):
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        self.top_bar = ctk.CTkFrame(self.main_container, height=60)
        self.top_bar.pack(fill="x")

        # Hamburger button
        self.menu_button = ctk.CTkButton(
            self.top_bar, text="☰", width=50, command=self.toggle_menu
        )
        self.menu_button.pack(side="left", padx=10)

        self.user_label = ctk.CTkLabel(
            self.top_bar, text=f"👤 {self.username}"
        )
        self.user_label.pack(side="right", padx=15)

        # Main content frame (side menu + dynamic content area)
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(fill="both", expand=True)

        # Side menu
        self.side_menu = ctk.CTkFrame(self.content_frame, width=0)
        self.side_menu.pack(side="left", fill="y")

        self.side_menu.pack_propagate(False)

        # Dynamic content area
        self.dynamic_container = ctk.CTkFrame(self.content_frame)
        self.dynamic_container.pack(side="left", fill="both", expand=True)

    """
    Creates menu buttons but doesn't pack them
    they are packed when the menu is opened
    """
    def setup_menu(self):
        self.menu_widgets = []

        items = [
            ("My GYM", lambda: self.on_open_sessions()),
            ("MY PROFILE", lambda: self.on_open_profile()),
            ("LOG OUT", lambda: self.on_logout())
        ]

        for text, cmd in items:
            btn = ctk.CTkButton(
                self.side_menu,
                text=text,
                command=cmd,
                anchor="w"
            )
            self.menu_widgets.append(btn)

    """
    If menu open -> close it
    If menu closed -> open it and pack widgets
    """
    def toggle_menu(self):
        if self.menu_open:
            # CLOSE
            self.side_menu.configure(width=0)

            for widget in self.menu_widgets:
                widget.pack_forget()

            self.menu_open = False

        else:
            # OPEN
            self.side_menu.configure(width=self.menu_width)

            for widget in self.menu_widgets:
                widget.pack(fill="x", padx=10, pady=5)

            self.menu_open = True

    """
    Clears all the widgets from the dynamic content area.
    Used before loading a new view.
    """
    def clear(self):
        for w in self.dynamic_container.winfo_children():
            w.destroy()

    # NAVIGATION HANDLERS

    """
    Called when user clicks "MY GYM"
    callback: function to call when a session is selected
    """

    def show_sessions(self, callback=None):
        self._session_callback = callback  # store it for later use
        self.clear()
        view = SessionsView(self.dynamic_container, self.username)
        view.on_session_selected = self._session_callback
        view.pack(fill="both", expand=True)

    """
    Called when user clicks "MY PROFILE"
    """
    def show_profile(self):
        self.clear()
        view = ProfileView(self.dynamic_container, self.username)
        view.pack(fill="both", expand=True)

    """
    Displays ExercisesView for a selected session
    """
    def show_exercises(self, session_data):
        self.clear()
        view = ExercisesView(self.dynamic_container, self.username, session_data)
        # Set back button callback to reload sessions with stored callback
        view.on_back = lambda: self.show_sessions(self._session_callback)
        view.pack(fill="both", expand=True)