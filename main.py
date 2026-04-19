from task_manager import TaskManager
from ia_service import create_simple_tasks


def print_menu():
    print("\n--- Gestor de Tareas Inteligente ---")
    print("1. Añadir tarea")
    print("2. Añadir tarea compleja (con IA)")
    print("3. Listar tareas")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")


def main():

    manager = TaskManager()

    while True:

        print_menu()

        try:

            choice = int(input("Elige una opcion: "))

            match choice:
                case 1:
                    description = input("Descripcion de la tarea: ")
                    manager.add_task(description)

                case 2:
                    description = input("Descripcion de la tarea compleja: ")
                    substasks = create_simple_tasks(description)
                    for subtask in substasks:
                        if not subtask.startswith("Error:"):
                            manager.add_task(subtask)
                        else:
                            print(subtask)
                            break

                case 3:
                    manager.list_task()

                case 4:
                    id = int(input("ID de la tarea a completar: "))
                    manager.complete_task(id)

                case 5:
                    id = int(input("ID de la tarea a eliminar: "))
                    manager.delete_task(id)

                case 6:
                    print("Saliendo...")
                    break
                case _:
                    print("Opcion no valida. Seleccione otra.")

        except ValueError:
            print("Opcion no valida. Seleccione otra.")


if __name__ == "__main__":
    main()
