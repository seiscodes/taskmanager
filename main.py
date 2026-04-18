from task_manager import TaskManager


def print_menu():
    print("\n--- Gestor de Tareas Inteligente ---")
    print("1. Añadir tarea")
    print("2. Listar tareas")
    print("3. Completar tarea")
    print("4. Eliminar tarea")
    print("5. Salir")


def main():

    manager = TaskManager()

    while True:

        print_menu()

        choice = input("Elige una opcion: ")

        match choice:
            case "1":
                description = input("Descripcion de la tarea: ")
                manager.add_task(description)

            case "2":
                manager.list_task()

            case "3":
                id = input("ID de la tarea a completar: ")
                manager.complete_task(id)

            case "4":
                id = input("ID de la tarea a eliminar: ")
                manager.delete_task(id)

            case "5":
                print("Saliendo...")
                break
            case _:
                print("Opcion no valida. Seleccione otra.")


if __name__ == "__main__":
    main()
