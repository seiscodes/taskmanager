import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=api_key)


def create_simple_tasks(description):
    if not api_key:
        return ["Error: La api de gemini no esta configurada"]

    try:
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accionables.

Tarea: {description}

Formato de respuesta:
    - Subtarea 1
    - Subtarea 2
    - etc.

Responde solo con la lista de subtareas, una por línea, empezando cada línea con un guión."""

        response = cliente.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction="Eres un asistente de gestión de tareas. Responde SOLO con la lista de subtareas en formato de guión, sin introducción ni repetir la tarea original.",
                max_output_tokens=1024,
                temperature=0.7,
            )
        )

        content = response.text.strip()

        subtasks = []

        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)

        return subtasks if subtasks else ["Error: No se han podido generar las subtareas."]

    except Exception:
        return ["Error: No se ha podido conectar con gemini"]
