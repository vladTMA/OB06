# kanban_logic.py

# Логика управления задачами Kanban-доски:
# Содержит функции добавления, изменения статуса, удаления и экспорта задач
from datetime import datetime

# Хранилище всех задач и счётчик ID
tasks_data = []
task_counter = 1


# Добавляет новую задачу в список задач
def add_task(text: str):
    global task_counter
    if text.strip():
        number = f"{task_counter:02d}" # Формируем ID с ведущими нулями
        task ={
            "id": number,
            "text": text.strip(),
            "status": "new", # Начальный статус
            "timestamp": None # Метка времени появится при смене статуса
        }
        tasks_data.append(task)
        task_counter += 1
        return task
    return None


# Обновляет статус задачи и проставляет метку времени
def change_status(task_id: str, new_status: str):
    for task in tasks_data:
        if task["id"] == task_id:
            task["status"] = new_status
            task["timestamp"] = datetime.now().strftime("%d. %m.%Y %H:%M")
            return task
    return None


# Удаляет задачу по её ID
def delete_task(task_id: str):
    global tasks_data
    tasks_data[:] = [t for t in tasks_data if t["id"] !=task_id]


# Экспортирует задачи в текстовый файл, сгруппированные по статусам
def export_tasks_to_file(filename: str = "kanban_export.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        stages = ["new", "executing", "testing", 'done']
        for stage in stages:
            f.write(f"=== {stage.upper()} ===\n")
            for task in tasks_data:
                if task["status"] == stage:
                    line = f"{task['id']}. {task['text']} ({task['timestamp']})\n"
                    f.write(line)
            f.write("\n")
            print("Экспортируем задачу:", len(tasks_data))



