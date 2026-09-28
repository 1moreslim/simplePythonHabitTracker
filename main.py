import tkinter as tk
from tkinter import ttk, messagebox
from tracker import TrackerManager
from utils import validate_date, InvalidDateError


class ModernHabitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker By s31368")
        self.root.geometry("600x550")
        self.manager = TrackerManager()


        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_window(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()

        frame = tk.Frame(self.main_container, pady=120)
        frame.pack()

        tk.Label(frame, text="🌟 Welcome to Habit Tracker", font=("Helvetica", 18, "bold")).pack(pady=10)
        tk.Label(frame, text="Enter your username to load your data:").pack(pady=5)

        self.entry_user = ttk.Entry(frame, font=("Helvetica", 12), width=20)
        self.entry_user.pack(pady=10)
        self.entry_user.bind('<Return>', lambda event: self.process_login())

        ttk.Button(frame, text="Login / Register", command=self.process_login).pack(pady=15)


        try:
            self.login_image = tk.PhotoImage(file="icon.png")
            img_label = tk.Label(self.main_container, image=self.login_image)
            img_label.place(relx=1.0, rely=1.0, anchor="se", x=-15, y=-15)
        except tk.TclError:
            print("[SYSTEM LOG] icon.png not found. Continuing without image.")

    def process_login(self):
        user = self.entry_user.get().strip()
        if not user:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        self.manager.login(user)
        self.show_dashboard()


    def show_dashboard(self):
        self.clear_window()


        header = tk.Frame(self.main_container, bg="#2c3e50", pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"👤 Logged in as: {self.manager.current_user}", fg="white", bg="#2c3e50",
                 font=("Helvetica", 12, "bold")).pack(side="left", padx=15)
        ttk.Button(header, text="Logout", command=self.show_login_screen).pack(side="right", padx=15)


        notebook = ttk.Notebook(self.main_container)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        tab_manage = ttk.Frame(notebook)
        tab_view = ttk.Frame(notebook)

        notebook.add(tab_manage, text="📝 Manage Habits")
        notebook.add(tab_view, text="📊 My Tracks & Details")

        self.build_manage_tab(tab_manage)
        self.build_view_tab(tab_view)

    def build_manage_tab(self, parent):

        frame_add = ttk.LabelFrame(parent, text="Add a New Habit", padding=15)
        frame_add.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_add, text="Name:").grid(row=0, column=0, sticky="w")
        self.entry_name = ttk.Entry(frame_add, width=15)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Frequency:").grid(row=0, column=2, sticky="w")
        self.entry_freq = ttk.Entry(frame_add, width=15)
        self.entry_freq.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_add, text="Type:").grid(row=1, column=0, sticky="w")
        self.combo_type = ttk.Combobox(frame_add, values=["Good", "Bad"], state="readonly", width=12)
        self.combo_type.current(0)
        self.combo_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_add, text="➕ Add Habit", command=self.add_habit).grid(row=1, column=3, pady=10)


        frame_mark = ttk.LabelFrame(parent, text="Track an Activity", padding=15)
        frame_mark.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_mark, text="Habit Name:").grid(row=0, column=0, sticky="w")


        self.combo_mark_name = ttk.Combobox(frame_mark, state="readonly", width=13)
        self.combo_mark_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_mark, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
        self.entry_mark_date = ttk.Entry(frame_mark, width=15)
        self.entry_mark_date.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_mark, text="✅ Log Track", command=self.mark_completed).grid(row=1, column=2, padx=15)


        self.update_habit_dropdown()

    def build_view_tab(self, parent):

        filter_frame = tk.Frame(parent, pady=5)
        filter_frame.pack(fill="x", padx=10)

        ttk.Button(filter_frame, text="View All", command=self.refresh_table).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="View Good Habits", command=lambda: self.refresh_table("Good")).pack(side="left",
                                                                                                           padx=5)
        ttk.Button(filter_frame, text="View Bad Habits", command=lambda: self.refresh_table("Bad")).pack(side="left",
                                                                                                         padx=5)


        columns = ("Name", "Type", "Frequency", "Total Logs", "Log Dates")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        self.tree.heading("Name", text="Habit Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Frequency", text="Frequency")
        self.tree.heading("Total Logs", text="Total Logs")
        self.tree.heading("Log Dates", text="Dates Tracked")

        self.tree.column("Name", width=100)
        self.tree.column("Type", width=70)
        self.tree.column("Frequency", width=80)
        self.tree.column("Total Logs", width=80)
        self.tree.column("Log Dates", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_table()


    def update_habit_dropdown(self):
        """Helper method to refresh the habit selection dropdown."""
        habit_names = list(self.manager.habits.keys())
        self.combo_mark_name['values'] = habit_names

        if habit_names:
            self.combo_mark_name.current(0)
        else:
            self.combo_mark_name.set('')

    def add_habit(self):
        name = self.entry_name.get().strip()
        freq = self.entry_freq.get().strip()
        h_type = self.combo_type.get()

        if not name or not freq:
            messagebox.showwarning("Input Error", "Name and frequency are required.")
            return

        try:
            self.manager.add_habit(name, freq, h_type)
            messagebox.showinfo("Success", f"{h_type} habit '{name}' added!")
            self.entry_name.delete(0, tk.END)
            self.entry_freq.delete(0, tk.END)
            self.refresh_table()


            self.update_habit_dropdown()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mark_completed(self):

        name = self.combo_mark_name.get().strip()
        date_str = self.entry_mark_date.get().strip()

        if not name or not date_str:
            messagebox.showwarning("Input Error", "Habit name and date are required.")
            return

        try:
            validate_date(date_str)
            self.manager.mark_completed(name, date_str)
            messagebox.showinfo("Success", f"Logged '{name}' on {date_str}!")
            self.entry_mark_date.delete(0, tk.END)
            self.refresh_table()
        except KeyError as e:
            messagebox.showerror("Not Found", "Habit not found in your list.")
        except InvalidDateError as e:
            messagebox.showerror("Invalid Date", str(e))

    def refresh_table(self, filter_type=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if filter_type:
            habits = list(self.manager.get_habits_by_type(filter_type))
        else:
            habits = self.manager.get_sorted_habits()

        for h in habits:
            dates = ", ".join(sorted(h.dates_completed)) if h.dates_completed else "No tracks yet"
            self.tree.insert("", "end", values=(h.name, h.habit_type, h.frequency, len(h.dates_completed), dates))


def main():
    root = tk.Tk()
    app = ModernHabitApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()