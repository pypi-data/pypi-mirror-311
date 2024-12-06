import importlib

# Функция для загрузки заданий
def load_task_function(task_number):
    module_name = f"{task_number}_task"  # Модули называются 1_task, 2_task и так далее
    try:
        # Динамический импорт модуля (например, 1_task.py, 2_task.py)
        module = importlib.import_module(f".{module_name}", package="sceepy")
        # Получаем функцию t1, t2 и т.д.
        task_function = getattr(module, f"t{task_number}")
        return task_function
    except ModuleNotFoundError:
        raise ImportError(f"Модуль {module_name} не найден.")
    except AttributeError:
        raise AttributeError(f"Функция t{task_number} не найдена в модуле {module_name}.")

# Динамическое добавление всех функций t1-t6 в глобальное пространство
for task_number in range(1, 7):  # Для задач с 1 по 6
    task_function = load_task_function(task_number)
    globals()[f"t{task_number}"] = task_function
