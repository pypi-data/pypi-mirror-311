import requests
import os
import time
import keyring  # Librería para manejar almacenamiento seguro
from dotenv import load_dotenv
from story_dialogue_generator.config import config

load_dotenv()  # Cargar variables de entorno

class UserSession:
    SERVICE_NAME = "story_dialogue_generator"  # Nombre del servicio en keyring

    def __init__(self):
        # Obtener credenciales del entorno o archivo .env
        self.username = os.getenv("LIBRARY_USERNAME")
        self.password = os.getenv("LIBRARY_PASSWORD")

        if not self.username or not self.password:
            raise Exception("Credenciales no configuradas. Define LIBRARY_USERNAME y LIBRARY_PASSWORD en .env.")

        self.token = None
        self.token_expiration = None

        # Intentar cargar token desde keyring o autenticar
        self.load_token_from_keyring()
        if not self.token or time.time() >= self.token_expiration:
            self.authenticate()

    def authenticate(self):
        """
        Autentica al usuario y obtiene un nuevo token.
        """
        url = f"{config.USER_SERVICE_URL}/auth/token"
        response = requests.post(url, data={"username": self.username, "password": self.password})

        if response.status_code == 200:
            response_data = response.json()
            self.token = response_data.get("access_token")
            self.token_expiration = time.time() + 30 * 60  # Token válido por 30 minutos
            self.save_token_to_keyring()
        else:
            error_detail = response.json().get("detail", "Error desconocido")
            raise Exception(f"Error al autenticar usuario: {error_detail}")

    def save_token_to_keyring(self):
        """
        Guarda el token y su tiempo de expiración en keyring.
        """
        if self.token:
            # Guardar token y tiempo de expiración como datos separados en keyring
            keyring.set_password(self.SERVICE_NAME, f"{self.username}_token", self.token)
            keyring.set_password(self.SERVICE_NAME, f"{self.username}_token_expiration", str(self.token_expiration))

    def load_token_from_keyring(self):
        """
        Carga el token y su tiempo de expiración desde keyring.
        """
        try:
            self.token = keyring.get_password(self.SERVICE_NAME, f"{self.username}_token")
            token_expiration_str = keyring.get_password(self.SERVICE_NAME, f"{self.username}_token_expiration")
            if token_expiration_str:
                self.token_expiration = float(token_expiration_str)
        except Exception as e:
            self.token = None
            self.token_expiration = None

    def get_token(self):
        """
        Devuelve el token actual. Si está vencido, autentica nuevamente.
        """
        if not self.token or time.time() >= self.token_expiration:
            self.authenticate()
        return self.token
