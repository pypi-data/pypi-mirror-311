# narrify-library

# **Story Dialogue Generator**

Librería para generar diálogos e historias utilizando modelos de lenguaje.

## **Descripción**

`story-dialogue-generator` es una librería de Python diseñada para facilitar la generación de diálogos e historias estructuradas. Ideal para proyectos creativos, videojuegos, y aplicaciones que requieran narrativa dinámica o interactiva, esta herramienta permite integrarse con un modelo de lenguaje a través de endpoints personalizados.

---

## **Características**

- **Generación de diálogos:** Crea diálogos basados en contexto, personajes, y configuraciones específicas.
- **Generación de historias:** Genera historias completas con estructura narrativa (introducción, conflicto, clímax, etc.).
- **CLI incluida:** Ejecuta funcionalidades directamente desde la terminal.
- **Autenticación integrada:** Manejo seguro de tokens de usuario.
- **Soporte para JSON:** Configura entradas directamente con archivos JSON o parámetros.

---

## **Instalación**

Para instalar la librería, utiliza `pip`:

```bash
pip install story-dialogue-generator

´´´

## **Uso Básico**

### **1. Configuración Inicial**

Agrega tus credenciales al archivo `.env` en el directorio raíz de tu proyecto:

```plaintext
LIBRARY_USERNAME=tu_usuario
LIBRARY_PASSWORD=tu_contraseña

2. Generar un Diálogo
Entrada como Parámetros
python
Copy code
from story_dialogue_generator import UserSession, DialogueService

user_session = UserSession()

story = "A hero embarks on a journey to save the kingdom."
dialogue_context = "The hero confronts the villain in an epic battle."
settings = {
    "location": "castle",
    "time_of_day": "night",
    "number_of_scenes": 3,
    "number_of_characters": 2
}
characters = [
    {
        "name": "Hero",
        "role": "protagonist",
        "attributes": [{"key": "bravery", "value": "high"}]
    },
    {
        "name": "Villain",
        "role": "antagonist",
        "attributes": [{"key": "intelligence", "value": "high"}]
    }
]

# Generar el diálogo
dialogue_service = DialogueService(user_session, story, dialogue_context, settings, characters)
response = dialogue_service.generate_dialogue()
print(response)
Entrada desde un Archivo JSON
Crea un archivo dialogue.json con el siguiente contenido:

json
Copy code
{
    "story": "A knight defends the kingdom.",
    "dialogue_context": "The knight meets a mysterious stranger.",
    "settings": {
        "location": "forest",
        "time_of_day": "dusk",
        "number_of_scenes": 2,
        "number_of_characters": 2
    },
    "characters": [
        {
            "name": "Knight",
            "role": "protagonist",
            "attributes": [{"key": "strength", "value": "high"}]
        },
        {
            "name": "Stranger",
            "role": "ally",
            "attributes": [{"key": "wisdom", "value": "high"}]
        }
    ]
}
Luego, carga el JSON en Python:

python
Copy code
import json
from story_dialogue_generator import UserSession, DialogueService

# Crear la sesión del usuario
user_session = UserSession()

# Cargar los datos del archivo JSON
with open("dialogue.json", "r") as f:
    dialogue_data = json.load(f)

# Crear y usar el servicio de diálogo
dialogue_service = DialogueService(
    user_session,
    dialogue_data["story"],
    dialogue_data["dialogue_context"],
    dialogue_data["settings"],
    dialogue_data["characters"]
)
response = dialogue_service.generate_dialogue()
print(response)
3. Generar una Historia
Entrada como Parámetros
python
Copy code
from story_dialogue_generator import UserSession, StoryService

# Crear la sesión del usuario
user_session = UserSession()

# Datos para la historia
title = "The Great Adventure"
settings = {
    "size": "large",
    "attributes": [{"key": "theme", "value": "courage"}]
}
characters = [
    {
        "name": "Knight",
        "attributes": [{"key": "role", "value": "protector"}]
    },
    {
        "name": "Wizard",
        "attributes": [{"key": "skill", "value": "magic"}]
    }
]

# Generar la historia
story_service = StoryService(user_session, title, settings, characters)
response = story_service.generate_story()
print(response)
Entrada desde un Archivo JSON
Crea un archivo story.json con el siguiente contenido:

json
Copy code
{
    "title": "The Great Adventure",
    "settings": {
        "size": "large",
        "attributes": [{"key": "theme", "value": "courage"}]
    },
    "characters": [
        {
            "name": "Knight",
            "attributes": [{"key": "role", "value": "protector"}]
        },
        {
            "name": "Wizard",
            "attributes": [{"key": "skill", "value": "magic"}]
        }
    ]
}
Luego, carga el JSON en Python:

python
Copy code
import json
from story_dialogue_generator import UserSession, StoryService

# Crear la sesión del usuario
user_session = UserSession()

# Cargar los datos del archivo JSON
with open("story.json", "r") as f:
    story_data = json.load(f)

# Crear y usar el servicio de historia
story_service = StoryService(
    user_session,
    story_data["title"],
    story_data["settings"],
    story_data["characters"]
)
response = story_service.generate_story()
print(response)
Uso de la CLI
Autenticación
Autentica al usuario configurado en el archivo .env:

bash
Copy code
story-dialogue-cli --authenticate
Generar un Diálogo
Proporciona un archivo JSON con los datos del diálogo:

bash
Copy code
story-dialogue-cli --generate-dialogue ./dialogue.json
Generar una Historia
Proporciona un archivo JSON con los datos de la historia:

bash
Copy code
story-dialogue-cli --generate-story ./story.json
Requisitos
Python 3.7 o superior
Dependencias:
requests
python-dotenv
keyring
