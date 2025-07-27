import tkinter as tk
from tkinter import messagebox, simpledialog
from shared import *
import random

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=400, width=450)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class MoodPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Planner")
        self.root.geometry("480x700")
        self.root.resizable(False, False)

        self.custom_moods = load_custom_moods()
        self.tasks = load_tasks()
        self.all_moods = {**DEFAULT_MOODS, **self.custom_moods}

        self.title_label = tk.Label(root, text="Mood Planner 😊", font=("Segoe UI", 24))
        self.title_label.pack(pady=10)

        self.days_label = tk.Label(root, text=f"Days logged: {count_logged_days()}", font=("Segoe UI", 12))
        self.days_label.pack()

        self.quote_label = tk.Label(root, text=f"Quote: \"{get_daily_quote()}\"", font=("Segoe UI", 10), wraplength=450, justify="center")
        self.quote_label.pack(pady=5)

        self.mood_frame = ScrollableFrame(root)
        self.mood_frame.pack(pady=10, fill="both", expand=True)

        self.update_mood_buttons()

        control_frame = tk.Frame(root)
        control_frame.pack(side="bottom", pady=15)

        tk.Button(control_frame, text="Add/Edit/Remove Moods", command=self.edit_custom_moods, font=("Segoe UI", 12)).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Tasks", command=self.manage_tasks, font=("Segoe UI", 12)).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Info", command=self.show_info, font=("Segoe UI", 12)).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Quit", command=self.quit_app, font=("Segoe UI", 12)).grid(row=0, column=3, padx=5)

    def update_mood_buttons(self):
        for widget in self.mood_frame.scrollable_frame.winfo_children():
            widget.destroy()

        self.all_moods = {**DEFAULT_MOODS, **self.custom_moods}
        for emoji, name in self.all_moods.items():
            btn = tk.Button(self.mood_frame.scrollable_frame, text=f"{emoji}  {name}",
                            font=("Segoe UI", 14), width=28, height=2,
                            command=lambda e=emoji, n=name: self.log_and_alert(e, n))
            btn.pack(pady=3)

        self.days_label.config(text=f"Days logged: {count_logged_days()}")
        self.quote_label.config(text=f"Quote: \"{get_daily_quote()}\"")

    def log_and_alert(self, emoji, name):
        log_mood(emoji, name)
        self.ask_to_add_suggested_tasks(emoji)
        messagebox.showinfo("Mood Logged", f"✅ You logged: {emoji} {name}")
        self.days_label.config(text=f"Days logged: {count_logged_days()}")

    def ask_to_add_suggested_tasks(self, mood_emoji):
        suggestions = MOOD_TASKS_SUGGESTIONS.get(mood_emoji, [])
        if not suggestions:
            return
        count = min(3, len(suggestions))
        chosen = random.sample(suggestions, count)
        msg = "Suggested tasks for this mood:\n\n" + "\n".join(f"- {t}" for t in chosen)
        if messagebox.askyesno("Suggested Tasks", f"{msg}\n\nAdd these tasks to your task list?"):
            self.tasks.extend(chosen)
            save_tasks(self.tasks)
            messagebox.showinfo("Tasks Added", f"Added {len(chosen)} tasks to your task list.")

    def edit_custom_moods(self):
        action = simpledialog.askstring("Edit Moods", "Type 'add', 'edit', or 'remove':")
        if not action:
            return
        action = action.strip().lower()

        if action == "add":
            emoji = simpledialog.askstring("Add Mood", "Emoji:")
            name = simpledialog.askstring("Add Mood", "Name:")
            if emoji and name:
                self.custom_moods[emoji] = name
                save_custom_moods(self.custom_moods)
                self.update_mood_buttons()
        elif action == "edit":
            if not self.custom_moods:
                messagebox.showinfo("Edit Moods", "No custom moods to edit.")
                return
            keys = list(self.custom_moods.keys())
            options = "\n".join(f"{i+1}. {k} {self.custom_moods[k]}" for i, k in enumerate(keys))
            choice = simpledialog.askinteger("Edit Mood", f"Which mood to edit?\n{options}")
            if choice and 1 <= choice <= len(keys):
                old_key = keys[choice-1]
                new_emoji = simpledialog.askstring("Edit Mood", "New emoji:", initialvalue=old_key)
                new_name = simpledialog.askstring("Edit Mood", "New name:", initialvalue=self.custom_moods[old_key])
                if new_emoji and new_name:
                    del self.custom_moods[old_key]
                    self.custom_moods[new_emoji] = new_name
                    save_custom_moods(self.custom_moods)
                    self.update_mood_buttons()
        elif action == "remove":
            if not self.custom_moods:
                messagebox.showinfo("Remove Mood", "No custom moods to remove.")
                return
            keys = list(self.custom_moods.keys())
            options = "\n".join(f"{i+1}. {k} {self.custom_moods[k]}" for i, k in enumerate(keys))
            choice = simpledialog.askinteger("Remove Mood", f"Which mood to remove?\n{options}")
            if choice and 1 <= choice <= len(keys):
                key = keys[choice-1]
                del self.custom_moods[key]
                save_custom_moods(self.custom_moods)
                self.update_mood_buttons()

    def manage_tasks(self):
        def refresh_task_list():
            task_list.delete(0, tk.END)
            for t in self.tasks:
                task_list.insert(tk.END, t)
            self.days_label.config(text=f"Days logged: {count_logged_days()}")

        task_win = tk.Toplevel(self.root)
        task_win.title("Tasks")
        task_win.geometry("400x350")
        task_win.resizable(False, False)

        task_list = tk.Listbox(task_win, font=("Segoe UI", 12))
        task_list.pack(fill="both", expand=True, padx=10, pady=10)

        refresh_task_list()

        entry_frame = tk.Frame(task_win)
        entry_frame.pack(pady=5)

        task_entry = tk.Entry(entry_frame, font=("Segoe UI", 12), width=30)
        task_entry.grid(row=0, column=0, padx=5)

        def add_task():
            new_task = task_entry.get().strip()
            if new_task:
                self.tasks.append(new_task)
                save_tasks(self.tasks)
                task_entry.delete(0, tk.END)
                refresh_task_list()
                messagebox.showinfo("Task Added", "Task added successfully.")
            else:
                messagebox.showwarning("Input Error", "Task cannot be empty.")

        def remove_task():
            sel = task_list.curselection()
            if sel:
                index = sel[0]
                task = self.tasks.pop(index)
                save_tasks(self.tasks)
                refresh_task_list()
                messagebox.showinfo("Task Removed", f"Removed task:\n{task}")
            else:
                messagebox.showwarning("Selection Error", "No task selected.")

        add_btn = tk.Button(entry_frame, text="Add", font=("Segoe UI", 12), command=add_task)
        add_btn.grid(row=0, column=1, padx=5)

        rem_btn = tk.Button(task_win, text="Remove Selected Task", font=("Segoe UI", 12), command=remove_task)
        rem_btn.pack(pady=5)

    def show_info(self):
        info_text = (
            "📘 Mood Planner\n"
            "Author: Zachary\n\n"
            "Track moods with emojis, add/edit/remove custom moods,\n"
            "manage tasks, and see motivational daily quotes.\n\n"
            "Moods are saved in 'custom_moods.json',\n"
            "tasks in 'tasks.json', and\n"
            "logs in 'mood_log.txt'."
        )
        messagebox.showinfo("Info", info_text)

    def quit_app(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodPlannerGUI(root)
    root.mainloop()
