from view.login_view import LoginView
from view.register_view import RegisterView
from view.menu_view import MenuView
from view.sessions_view import SessionsView
from view.exercises_view import ExercisesView

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_view = None
        self.current_user = None

        self.show_login()

    def clear_view(self):
        if self.current_view:
            self.current_view.destroy()

    def show_login(self):
        self.clear_view()
        view = LoginView(self.root)

        view.signup_label.bind("<Button-1>", lambda e: self.show_register())
        view.signin_button.configure(
            command=lambda: self.show_menu("UsuarioDemo")
        )

        self.current_view = view
        view.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_view()
        view = RegisterView(self.root)

        view.on_back = self.show_login
        view.on_signup = self.show_login
        view.on_login = self.show_login

        self.current_view = view
        view.pack(fill="both", expand=True)

    def show_menu(self, username):
        self.clear_view()
        view = MenuView(self.root, username)
        self.current_user = username

        # navigation callbacks
        view.on_logout = self.show_login
        view.on_open_sessions = lambda: view.show_sessions(self.handle_session_selected)
        view.on_open_profile = view.show_profile

        self.current_view = view
        view.pack(fill="both", expand=True)

        # Show sessions upon login
        view.show_sessions(self.handle_session_selected)

    def show_sessions(self):
        self.clear_view()
        view = SessionsView(self.root, self.current_user)
        view.on_session_selected = self.handle_session_selected
        view.on_add_session = lambda: print("Add session clicked")  # Replace with backend logic

        # Example placeholder sessions
        sessions = [
            {"session_number": 1, "date": "2026-04-01"},
            {"session_number": 2, "date": "2026-04-02"}
        ]
        view.display_sessions(sessions)

        self.current_view = view
        view.pack(fill="both", expand=True)

    def show_profile(self):
        self.current_view.show_profile()

    def handle_session_selected(self, session_data):
        # Navigate to ExercisesView with the selected session
        self.clear_view()
        view = ExercisesView(self.root, self.current_user, session_data)

        # To be implemented
        exercises = []
        view.display_exercises(exercises)

        # Back navigation
        view.on_back = self.show_sessions

        self.current_view = view
        view.pack(fill="both", expand=True)