from shared import *
import sys
import random

def display_info():
    print("\n📘 Mood Planner by Zachary")
    print("Track moods, add/edit/remove custom moods, tasks, and see quotes!")
    print("Moods saved in 'custom_moods.json'. Tasks in 'tasks.json'. Logs in 'mood_log.txt'.\n")

def edit_custom_moods(custom_moods):
    while True:
        print("\n🛠 Custom Mood Editor")
        print("1. Add mood")
        print("2. Edit mood")
        print("3. Remove mood")
        print("4. Back to main menu")
        choice = input("Choose an option: ")

        if choice == "1":
            emoji = input("Enter emoji: ").strip()
            name = input("Enter name: ").strip()
            if emoji and name:
                custom_moods[emoji] = name
                save_custom_moods(custom_moods)
                print("✅ Mood added.")
            else:
                print("❌ Invalid input.")
        elif choice == "2":
            if not custom_moods:
                print("No custom moods to edit.")
                continue
            for i, (e, n) in enumerate(custom_moods.items(), 1):
                print(f"{i}. {e} {n}")
            try:
                index = int(input("Choose mood number to edit: ")) - 1
                keys = list(custom_moods.keys())
                if 0 <= index < len(keys):
                    new_emoji = input("New emoji: ").strip()
                    new_name = input("New name: ").strip()
                    if new_emoji and new_name:
                        old_key = keys[index]
                        del custom_moods[old_key]
                        custom_moods[new_emoji] = new_name
                        save_custom_moods(custom_moods)
                        print("✅ Mood edited.")
                    else:
                        print("❌ Invalid input.")
                else:
                    print("❌ Invalid number.")
            except:
                print("❌ Invalid input.")
        elif choice == "3":
            if not custom_moods:
                print("No custom moods to remove.")
                continue
            for i, (e, n) in enumerate(custom_moods.items(), 1):
                print(f"{i}. {e} {n}")
            try:
                index = int(input("Choose mood number to remove: ")) - 1
                keys = list(custom_moods.keys())
                if 0 <= index < len(keys):
                    del custom_moods[keys[index]]
                    save_custom_moods(custom_moods)
                    print("🗑️ Mood removed.")
                else:
                    print("❌ Invalid number.")
            except:
                print("❌ Invalid input.")
        elif choice == "4":
            break
        else:
            print("❌ Invalid option.")

def edit_tasks(tasks):
    while True:
        print("\n🗒️ Task Manager")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Back to main menu")
        choice = input("Choose an option: ")

        if choice == "1":
            if tasks:
                print("\nYour Tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("No tasks added yet.")
        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                tasks.append(task)
                save_tasks(tasks)
                print("✅ Task added.")
            else:
                print("❌ Task cannot be empty.")
        elif choice == "3":
            if not tasks:
                print("No tasks to remove.")
                continue
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
            try:
                index = int(input("Choose task number to remove: ")) - 1
                if 0 <= index < len(tasks):
                    removed = tasks.pop(index)
                    save_tasks(tasks)
                    print(f"🗑️ Removed task: {removed}")
                else:
                    print("❌ Invalid number.")
            except:
                print("❌ Invalid input.")
        elif choice == "4":
            break
        else:
            print("❌ Invalid option.")

def suggest_tasks_for_mood(mood_emoji, tasks):
    suggestions = MOOD_TASKS_SUGGESTIONS.get(mood_emoji, [])
    if suggestions:
        count = min(3, len(suggestions))
        chosen = random.sample(suggestions, count)
        print("\n💡 Suggested tasks for this mood:")
        for i, task in enumerate(chosen, 1):
            print(f"{i}. {task}")
        add_choice = input("Add these tasks to your task list? (y/n): ").strip().lower()
        if add_choice == "y":
            tasks.extend(chosen)
            save_tasks(tasks)
            print(f"✅ Added {len(chosen)} tasks to your task list.")

def main():
    custom_moods = load_custom_moods()
    tasks = load_tasks()

    while True:
        all_moods = {**DEFAULT_MOODS, **custom_moods}
        print("\n--- Mood Planner ---")
        print(f"Logged days: {count_logged_days()}")
        print("Daily Quote:", get_daily_quote())
        for i, (emoji, name) in enumerate(all_moods.items(), 1):
            print(f"{i}. {emoji} {name}")
        print("a. ➕ Add/Edit/Remove custom moods")
        print("t. 🗒️ Tasks")
        print("i. ℹ️ Info")
        print("q. ❎ Quit")

        choice = input("Choose a number or option: ").strip().lower()

        if choice == "q":
            print("\n👋 Take care! See you next time.\n")
            input("Press Enter to exit...")
            sys.exit()
        elif choice == "i":
            display_info()
        elif choice == "a":
            edit_custom_moods(custom_moods)
        elif choice == "t":
            edit_tasks(tasks)
        else:
            try:
                idx = int(choice) - 1
                emoji, name = list(all_moods.items())[idx]
                log_mood(emoji, name)
                print(f"📝 Logged: {emoji} {name}")
                suggest_tasks_for_mood(emoji, tasks)
            except:
                print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
