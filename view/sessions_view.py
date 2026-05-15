import calendar
import customtkinter as ctk
from datetime import date, datetime

class SessionsView(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        self.on_session_selected = None
        self.on_add_session = None  # Callback for adding a new session
        self.on_edit_session = None
        self.on_delete_session = None
        self.on_filter_sessions = None
        # Stores the function that receives the selected date
        self.calendar_callback = None
        self.current_year = date.today().year
        self.current_month = date.today().month
        # Stores the dates currently selected in the filter area
        self.date_from = ""
        self.date_to = ""

        # Title
        self.title = ctk.CTkLabel(self, text=f"{self.username}'s sessions", font=("Arial", 20, "bold"))
        self.title.pack(pady=10)

        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.from_row = ctk.CTkFrame(self.filter_frame)
        self.from_row.pack(fill="x", padx=10, pady=(10, 5))

        self.from_label = ctk.CTkLabel(self.from_row, text="From date", width=80, anchor="w")
        self.from_label.pack(side="left", padx=(0, 10))

        self.from_button = ctk.CTkButton(
            self.from_row,
            text="Select date",
            command=lambda: self.open_calendar(self.set_from_date)
        )
        self.from_button.pack(side="left", fill="x", expand=True)

        self.to_row = ctk.CTkFrame(self.filter_frame)
        self.to_row.pack(fill="x", padx=10, pady=5)

        self.to_label = ctk.CTkLabel(self.to_row, text="To date", width=80, anchor="w")
        self.to_label.pack(side="left", padx=(0, 10))

        self.to_button = ctk.CTkButton(
            self.to_row,
            text="Select date",
            command=lambda: self.open_calendar(self.set_to_date)
        )
        self.to_button.pack(side="left", fill="x", expand=True)

        self.search_button = ctk.CTkButton(
            self.filter_frame,
            text="Search",
            width=120,
            command=self.apply_filters
        )
        self.search_button.pack(pady=(5, 10))

        # Scrollable container
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add session button
        self.add_button = ctk.CTkButton(self, text="Add session", command=self.add_session)
        self.add_button.pack(pady=10)

    def format_date_for_display(self, date_text):
        if not date_text:
            return ""

        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d")
            return parsed_date.strftime("%d/%m/%Y")
        except ValueError:
            return date_text

    def display_sessions(self, sessions):
        # Clear previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display each session as a button
        for session in sessions:
            row = ctk.CTkFrame(self.scrollable_frame)
            row.pack(fill="x", pady=5)

            btn = ctk.CTkButton(
                row,
                text=f"Session #{session['session_number']} - {session['date']}",
                command=lambda s=session: self.on_session_selected(s)  # callback
            )
            btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

            menu = ctk.CTkOptionMenu(
                row,
                values=["Edit", "Delete"],
                width=40,
                command=None
            )
            menu.configure(command=lambda action, s=session, m=menu: self.handle_session_action(action, s, m))
            menu.set("")
            menu.pack(side="right")

    def add_session(self):
        if self.on_add_session:
            self.open_calendar(self.on_add_session)
        else:
            print("To be implemented")

    def set_filter_dates(self, date_from, date_to):
        self.date_from = date_from or ""
        self.date_to = date_to or ""
        self.update_filter_buttons()

    def update_filter_buttons(self):
        if self.date_from:
            self.from_button.configure(text=self.format_date_for_display(self.date_from))
        else:
            self.from_button.configure(text="Select date")

        if self.date_to:
            self.to_button.configure(text=self.format_date_for_display(self.date_to))
        else:
            self.to_button.configure(text="Select date")

    def set_from_date(self, selected_date):
        self.date_from = selected_date
        self.update_filter_buttons()

    def set_to_date(self, selected_date):
        self.date_to = selected_date
        self.update_filter_buttons()

    def apply_filters(self):
        if self.on_filter_sessions:
            self.on_filter_sessions(self.date_from, self.date_to)

    def handle_session_action(self, action, session, menu):
        # Reset the visible text so the control keeps looking like an arrow-only menu
        menu.set("")

        if action == "Edit" and self.on_edit_session:
            # Reuse the same calendar window for editing a date
            self.open_calendar(lambda selected_date: self.on_edit_session(session, selected_date))

        if action == "Delete" and self.on_delete_session:
            self.on_delete_session(session)

    def open_calendar(self, callback):
        self.calendar_callback = callback
        self.calendar_window = ctk.CTkToplevel(self)
        self.calendar_window.title("Select date")
        self.calendar_window.geometry("320x300")

        self.calendar_frame = ctk.CTkFrame(self.calendar_window)
        self.calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month_name = calendar.month_name[self.current_month]

        header = ctk.CTkFrame(self.calendar_frame)
        header.pack(fill="x", pady=5)

        previous_button = ctk.CTkButton(header, text="<", width=40, command=self.previous_month)
        previous_button.pack(side="left")

        title = ctk.CTkLabel(header, text=f"{month_name} {self.current_year}")
        title.pack(side="left", expand=True)

        next_button = ctk.CTkButton(header, text=">", width=40, command=self.next_month)
        next_button.pack(side="right")

        days_frame = ctk.CTkFrame(self.calendar_frame)
        days_frame.pack(fill="both", expand=True)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for column, day_name in enumerate(days):
            label = ctk.CTkLabel(days_frame, text=day_name)
            label.grid(row=0, column=column, padx=2, pady=2)

        month_days = calendar.monthcalendar(self.current_year, self.current_month)

        for row, week in enumerate(month_days, start=1):
            for column, day_number in enumerate(week):
                if day_number == 0:
                    label = ctk.CTkLabel(days_frame, text="")
                    label.grid(row=row, column=column, padx=2, pady=2)
                else:
                    button = ctk.CTkButton(
                        days_frame,
                        text=str(day_number),
                        width=36,
                        command=lambda d=day_number: self.select_date(d)
                    )
                    button.grid(row=row, column=column, padx=2, pady=2)

    def previous_month(self):
        self.current_month -= 1

        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1

        self.draw_calendar()

    def next_month(self):
        self.current_month += 1

        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1

        self.draw_calendar()

    def select_date(self, day):
        selected_date = date(self.current_year, self.current_month, day)
        self.calendar_window.destroy()
        # Return the chosen date to whoever opened the calendar
        self.calendar_callback(selected_date.isoformat())
