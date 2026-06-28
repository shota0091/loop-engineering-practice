import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todo.json"


def load_tasks() -> list[dict]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_add(title: str) -> None:
    tasks = load_tasks()
    task = {"id": len(tasks) + 1, "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: [{task['id']}] {title}")


def cmd_list() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}. {task['title']}")


def cmd_done(task_id: int) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Done: [{task_id}] {task['title']}")
            return
    print(f"Task {task_id} not found.")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: python todo.py <command> [args]")
        print("Commands: add <title>, list, done <id>")
        sys.exit(1)

    command = args[0]

    if command == "add":
        if len(args) < 2:
            print("Usage: python todo.py add <title>")
            sys.exit(1)
        cmd_add(" ".join(args[1:]))
    elif command == "list":
        cmd_list()
    elif command == "done":
        if len(args) < 2:
            print("Usage: python todo.py done <id>")
            sys.exit(1)
        try:
            cmd_done(int(args[1]))
        except ValueError:
            print("ID must be an integer.")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        print("Commands: add <title>, list, done <id>")
        sys.exit(1)


if __name__ == "__main__":
    main()
