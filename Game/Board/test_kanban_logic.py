# test_kanban_logic

# Модуль юнит-тестов для логики задач Kanban-доски
import unittest
from kanban_logic import tasks_data, add_task, change_status, delete_task


class TestKanbanLogic(unittest.TestCase):
    # Подготовка перед каждым тестом: очищаем список задач
    def setUp(self):
        tasks_data.clear()

    # Проверяем добавление новой задачи
    def test_add_task(self):
        task = add_task("Новая задача")
        self.assertEqual(task["text"], "Новая задача")
        self.assertEqual(task["status"], "new")

    # Проверяем смену статуса задачи
    def test_change_status(self):
        task = add_task("Задача")
        updated = change_status(task["id"], "executing")
        self.assertEqual(updated["status"], "executing")

    # Проверяем удаление задачи
    def test_delete_task(self):
        task = add_task("Удалить")
        delete_task(task["id"])
        self.assertEqual(len(tasks_data), 0)


# Запускаем тесты при прямом запуске файла
if __name__ == "__main__":
    unittest.main()
