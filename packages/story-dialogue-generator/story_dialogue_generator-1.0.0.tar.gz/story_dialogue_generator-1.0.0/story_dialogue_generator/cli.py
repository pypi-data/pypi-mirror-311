import argparse
import json
from story_dialogue_generator import UserSession, DialogueService, StoryService

def main():
    parser = argparse.ArgumentParser(
        description="Story Dialogue Generator CLI - Genera diálogos e historias desde la terminal."
    )

    # Comando para autenticación
    parser.add_argument(
        "--authenticate",
        action="store_true",
        help="Autentica al usuario con las credenciales configuradas en el archivo .env"
    )

    # Comando para generar un diálogo
    parser.add_argument(
        "--generate-dialogue",
        type=str,
        metavar="DIALOGUE_JSON_PATH",
        help="Ruta al archivo JSON con los datos para generar un diálogo"
    )

    # Comando para generar una historia
    parser.add_argument(
        "--generate-story",
        type=str,
        metavar="STORY_JSON_PATH",
        help="Ruta al archivo JSON con los datos para generar una historia"
    )

    args = parser.parse_args()

    if args.authenticate:
        # Autenticación del usuario
        try:
            user_session = UserSession()
            print(f"Autenticación exitosa. Token: {user_session.get_token()}")
        except Exception as e:
            print(f"Error durante la autenticación: {e}")

    elif args.generate_dialogue:
        # Generación de diálogo
        try:
            user_session = UserSession()
            with open(args.generate_dialogue, "r") as f:
                dialogue_data = json.load(f)
            
            story = dialogue_data.get("story")
            dialogue_context = dialogue_data.get("dialogue_context")
            settings = dialogue_data.get("settings")
            characters = dialogue_data.get("characters")

            dialogue_service = DialogueService(
                user_session,
                story,
                dialogue_context,
                settings,
                characters
            )
            response = dialogue_service.generate_dialogue()
            print("Diálogo generado con éxito:")
            print(response)
        except Exception as e:
            print(f"Error al generar el diálogo: {e}")

    elif args.generate_story:
        # Generación de historia
        try:
            user_session = UserSession()
            with open(args.generate_story, "r") as f:
                story_data = json.load(f)

            title = story_data.get("title")
            settings = story_data.get("settings")
            characters = story_data.get("characters")
            plots = story_data.get("plots", 1)
            endings = story_data.get("endings", 1)

            story_service = StoryService(
                user_session,
                title,
                settings,
                characters,
                plots,
                endings
            )
            response = story_service.generate_story()
            print("Historia generada con éxito:")
            print(response)
        except Exception as e:
            print(f"Error al generar la historia: {e}")

    else:
        parser.print_help()
