import os
import importlib

# Папка с задачами
TASKS_DIR = os.path.dirname(__file__)

# Функция для загрузки задания и функции
def load_task_function(task_number):
    module_name = f"task{task_number}"  # Модули называются task1, task2, ...
    try:
        # Динамический импорт модуля (например, task1.py, task2.py)
        module = importlib.import_module(f".{module_name}", package="sceepy")
        # Получаем функцию (например, t1, t2 и т.д.)
        task_function = getattr(module, f"t{task_number}")
        return task_function
    except ModuleNotFoundError:
        return f"Задача {task_number} не найдена."
    except AttributeError:
        return f"Функция t{task_number} не найдена в модуле {module_name}."

# Динамическое добавление всех функций t1-t6 в глобальное пространство
for task_number in range(1, 7):  # Для задач с 1 по 6
    task_function = load_task_function(task_number)
    globals()[f"t{task_number}"] = task_function
