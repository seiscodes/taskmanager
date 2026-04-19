import unittest
import json
import os
import tempfile
from io import StringIO
import sys
from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """Tests para la clase Task."""

    def test_task_creation(self):
        """Prueba que se crea una tarea correctamente."""
        task = Task(1, "Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Test task")
        self.assertFalse(task.completed)

    def test_task_creation_with_completed(self):
        """Prueba crear una tarea marcada como completada."""
        task = Task(1, "Test task", completed=True)
        self.assertTrue(task.completed)

    def test_task_str_representation_incomplete(self):
        """Prueba la representación en string de una tarea incompleta."""
        task = Task(1, "Test task")
        self.assertEqual(str(task), "[ ] #1: Test task")

    def test_task_str_representation_complete(self):
        """Prueba la representación en string de una tarea completada."""
        task = Task(1, "Test task", completed=True)
        self.assertEqual(str(task), "[✓] #1: Test task")


class TestTaskManagerAddTask(unittest.TestCase):
    """Tests para agregar tareas."""

    def setUp(self):
        """Configurar para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "task.json")
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.temp_file
        self.manager = TaskManager()

    def tearDown(self):
        """Limpiar después de cada test."""
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_add_single_task(self):
        """Prueba agregar una tarea."""
        self.manager.add_task("Comprar leche")
        self.assertEqual(len(self.manager._tasks), 1)
        self.assertEqual(self.manager._tasks[0].description, "Comprar leche")
        self.assertEqual(self.manager._tasks[0].id, 1)

    def test_add_multiple_tasks(self):
        """Prueba agregar múltiples tareas con IDs incrementales."""
        self.manager.add_task("Tarea 1")
        self.manager.add_task("Tarea 2")
        self.manager.add_task("Tarea 3")

        self.assertEqual(len(self.manager._tasks), 3)
        self.assertEqual(self.manager._tasks[0].id, 1)
        self.assertEqual(self.manager._tasks[1].id, 2)
        self.assertEqual(self.manager._tasks[2].id, 3)
        self.assertEqual(self.manager._next_id, 4)

    def test_task_id_increments(self):
        """Prueba que los IDs se incrementan correctamente."""
        for i in range(5):
            self.manager.add_task(f"Tarea {i+1}")

        for i, task in enumerate(self.manager._tasks, 1):
            self.assertEqual(task.id, i)


class TestTaskManagerListTask(unittest.TestCase):
    """Tests para listar tareas."""

    def setUp(self):
        """Configurar para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "task.json")
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.temp_file
        self.manager = TaskManager()

    def tearDown(self):
        """Limpiar después de cada test."""
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_list_empty_tasks(self):
        """Prueba listar tareas cuando no hay ninguna."""
        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.list_task()
        sys.stdout = sys.__stdout__

        self.assertIn("No hay tareas añadidas", captured_output.getvalue())

    def test_list_tasks_with_content(self):
        """Prueba listar tareas cuando hay contenido."""
        self.manager.add_task("Tarea 1")
        self.manager.add_task("Tarea 2")

        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.list_task()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("[ ] #1: Tarea 1", output)
        self.assertIn("[ ] #2: Tarea 2", output)

    def test_list_mixed_tasks(self):
        """Prueba listar tareas completadas e incompletas."""
        self.manager.add_task("Incompleta 1")
        self.manager.add_task("Incompleta 2")
        self.manager.add_task("Completada")
        self.manager.complete_task(3)

        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.list_task()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("[ ] #1: Incompleta 1", output)
        self.assertIn("[ ] #2: Incompleta 2", output)
        self.assertIn("[✓] #3: Completada", output)


class TestTaskManagerCompleteTask(unittest.TestCase):
    """Tests para completar tareas."""

    def setUp(self):
        """Configurar para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "task.json")
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.temp_file
        self.manager = TaskManager()

    def tearDown(self):
        """Limpiar después de cada test."""
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_complete_existing_task(self):
        """Prueba completar una tarea existente."""
        self.manager.add_task("Tarea a completar")
        self.manager.complete_task(1)

        self.assertTrue(self.manager._tasks[0].completed)

    def test_complete_nonexistent_task(self):
        """Prueba intentar completar una tarea que no existe."""
        self.manager.add_task("Tarea 1")

        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.complete_task(999)
        sys.stdout = sys.__stdout__

        self.assertIn("Tarea no encontrada: #999", captured_output.getvalue())

    def test_complete_already_completed_task(self):
        """Prueba completar una tarea que ya está completada."""
        self.manager.add_task("Tarea")
        self.manager.complete_task(1)
        self.assertTrue(self.manager._tasks[0].completed)

        self.manager.complete_task(1)
        self.assertTrue(self.manager._tasks[0].completed)


class TestTaskManagerDeleteTask(unittest.TestCase):
    """Tests para eliminar tareas."""

    def setUp(self):
        """Configurar para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "task.json")
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.temp_file
        self.manager = TaskManager()

    def tearDown(self):
        """Limpiar después de cada test."""
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_delete_existing_task(self):
        """Prueba eliminar una tarea existente."""
        self.manager.add_task("Tarea 1")
        self.manager.add_task("Tarea 2")

        self.manager.delete_task(1)

        self.assertEqual(len(self.manager._tasks), 1)
        self.assertEqual(self.manager._tasks[0].id, 2)

    def test_delete_nonexistent_task(self):
        """Prueba intentar eliminar una tarea que no existe."""
        self.manager.add_task("Tarea 1")

        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.delete_task(999)
        sys.stdout = sys.__stdout__

        self.assertEqual(len(self.manager._tasks), 1)
        self.assertIn("Tarea no encontrada: #999", captured_output.getvalue())

    def test_delete_multiple_tasks(self):
        """Prueba eliminar varias tareas."""
        self.manager.add_task("Tarea 1")
        self.manager.add_task("Tarea 2")
        self.manager.add_task("Tarea 3")

        self.manager.delete_task(1)
        self.manager.delete_task(3)

        self.assertEqual(len(self.manager._tasks), 1)
        self.assertEqual(self.manager._tasks[0].id, 2)


class TestTaskManagerPersistence(unittest.TestCase):
    """Tests para persistencia de datos (guardar y cargar)."""

    def setUp(self):
        """Configurar para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "task.json")
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.temp_file

    def tearDown(self):
        """Limpiar después de cada test."""
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_save_task_creates_file(self):
        """Prueba que guardar tareas crea el archivo JSON."""
        manager = TaskManager()
        manager.add_task("Tarea 1")

        self.assertTrue(os.path.exists(self.temp_file))

    def test_save_task_content(self):
        """Prueba que el contenido guardado es correcto."""
        manager = TaskManager()
        manager.add_task("Tarea 1")
        manager.add_task("Tarea 2")
        manager.complete_task(1)

        with open(self.temp_file, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], 1)
        self.assertEqual(data[0]["description"], "Tarea 1")
        self.assertTrue(data[0]["completed"])
        self.assertEqual(data[1]["id"], 2)
        self.assertEqual(data[1]["description"], "Tarea 2")
        self.assertFalse(data[1]["completed"])

    def test_load_tasks_from_file(self):
        """Prueba cargar tareas desde un archivo existente."""
        # Crear datos en el archivo
        tasks_data = [
            {"id": 1, "description": "Tarea 1", "completed": False},
            {"id": 2, "description": "Tarea 2", "completed": True},
        ]
        with open(self.temp_file, "w") as f:
            json.dump(tasks_data, f)

        # Cargar el gestor
        manager = TaskManager()

        self.assertEqual(len(manager._tasks), 2)
        self.assertEqual(manager._tasks[0].id, 1)
        self.assertEqual(manager._tasks[0].description, "Tarea 1")
        self.assertFalse(manager._tasks[0].completed)
        self.assertEqual(manager._tasks[1].id, 2)
        self.assertTrue(manager._tasks[1].completed)
        self.assertEqual(manager._next_id, 3)

    def test_load_tasks_nonexistent_file(self):
        """Prueba cargar tareas cuando el archivo no existe."""
        manager = TaskManager()
        self.assertEqual(len(manager._tasks), 0)
        self.assertEqual(manager._next_id, 1)

    def test_persistence_across_instances(self):
        """Prueba que los datos persisten entre instancias."""
        # Primera instancia
        manager1 = TaskManager()
        manager1.add_task("Tarea persistente")
        manager1.complete_task(1)

        # Segunda instancia
        manager2 = TaskManager()

        self.assertEqual(len(manager2._tasks), 1)
        self.assertEqual(manager2._tasks[0].description, "Tarea persistente")
        self.assertTrue(manager2._tasks[0].completed)


class TestTaskManagerIntegration(unittest.TestCase):
    """Tests de integración para flujos completos."""

    def setUp(self):
        """Configurar para cada test."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "task.json")
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.temp_file
        self.manager = TaskManager()

    def tearDown(self):
        """Limpiar después de cada test."""
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_complete_workflow(self):
        """Prueba un flujo completo de uso."""
        # Agregar tareas
        self.manager.add_task("Tarea 1")
        self.manager.add_task("Tarea 2")
        self.manager.add_task("Tarea 3")

        # Completar una
        self.manager.complete_task(2)

        # Listar tareas
        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.list_task()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("[ ] #1: Tarea 1", output)
        self.assertIn("[✓] #2: Tarea 2", output)
        self.assertIn("[ ] #3: Tarea 3", output)

        # Eliminar una
        self.manager.delete_task(1)
        self.assertEqual(len(self.manager._tasks), 2)

    def test_normal_id_management_after_deletion(self):
        """Prueba que los IDs nuevos no saltan después de una eliminación."""
        self.manager.add_task("Tarea 1")
        self.manager.add_task("Tarea 2")
        self.manager.add_task("Tarea 3")
        self.manager.delete_task(2)

        # El siguiente ID debe ser 4, no 3
        self.manager.add_task("Tarea 4")

        self.assertEqual(self.manager._tasks[-1].id, 4)
        self.assertEqual(len(self.manager._tasks), 3)

    def test_empty_to_full_workflow(self):
        """Prueba un flujo de tareas vacío a lleno."""
        self.assertEqual(len(self.manager._tasks), 0)

        for i in range(5):
            self.manager.add_task(f"Tarea {i+1}")

        self.assertEqual(len(self.manager._tasks), 5)

        for task in self.manager._tasks:
            self.manager.complete_task(task.id)

        self.assertTrue(all(task.completed for task in self.manager._tasks))


if __name__ == "__main__":
    unittest.main(verbosity=2)
