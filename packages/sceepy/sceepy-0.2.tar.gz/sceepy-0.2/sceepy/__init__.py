import importlib

# Загружаем функции из task1.py, task2.py и т.д.
def load_task_function(task_number):
    module_name = f"task{task_number}"
    try:
        # Динамический импорт модуля task1, task2 и т.д.
        module = importlib.import_module(f".{module_name}", package="sceepy")
        # Получаем функцию t1, t2 и т.д.
        task_function = getattr(module, f"t{task_number}")
        return task_function
    except ModuleNotFoundError:
        raise ImportError(f"Модуль task{task_number} не найден.")
    except AttributeError:
        raise AttributeError(f"Функция t{task_number} не найдена в модуле {module_name}.")

# Динамическое добавление всех функций t1-t6 в глобальное пространство
for task_number in range(1, 7):  # Для задач с 1 по 6
    task_function = load_task_function(task_number)
    globals()[f"t{task_number}"] = task_function
