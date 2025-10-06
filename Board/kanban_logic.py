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


# Заголовки для txt файла
COLUMN_TITLES_RU = {
    "new": "Новые задачи",
    "executing": "В работе",
    "testing": "Тестирование",
    "done": "Завершено"
}

# Заголовки названий стадий исполнения проекта
COLUMN_TITLES_RU = {
    "new": "Новые задачи",
    "executing": "В работе",
    "testing": "Тестирование",
    "done": "Завершено"
}

# Экспортирует задачи в текстовый файл с заголовком проекта и сроками
def export_tasks_to_file(
    filename: str = "kanban_export.txt",
    project_name: str = "Без названия",
    deadline_from: str = "",
    deadline_to: str = ""
):
    with open(filename, "w", encoding="utf-8") as f:
        # Заголовок проекта и срок
        f.write(f"📌 Проект: {project_name}\n")
        f.write(f"🗓 Срок исполнения: с {deadline_from} по {deadline_to}\n\n")

        # Задачи по стадиям
        stages = ["new", "executing", "testing", "done"]
        for stage in stages:
            title_ru = COLUMN_TITLES_RU.get(stage, f"Стадия: {stage}")
            f.write(f"{'=' * 10} {title_ru} {'=' * 10}\n")
            for task in tasks_data:
                if task["status"] == stage:
                    line = f"{task['id']}. {task['text']} ({task['timestamp']})\n"
                    f.write(line)
            f.write("\n")

    print(f"✅ Экспорт завершён: {filename} ({len(tasks_data)} задач)")








