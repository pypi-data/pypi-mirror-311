#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptado para manejar descargas mediante el backend.
"""

import requests
import os
from dotenv import dotenv_values
import pkg_resources


class RTD:
    def __init__(self):
        """
        Inicializa la clase con el ID del usuario y la URL base del backend.
        """
        # Carga las variables de entorno desde el archivo .env dentro del paquete
        self._cargar_variables_entorno()

        # Accede a las variables de entorno
        self.user_id = os.getenv("USER_ID")
        self.base_url = os.getenv("BASE_URL")

    def _cargar_variables_entorno(self):
        """
        Carga las variables de entorno desde el archivo .env incluido en el paquete.
        Utiliza pkg_resources para obtener la ruta del archivo .env dentro del paquete.
        """
        env_path = pkg_resources.resource_filename(
           "FlyBaseDownloads", '.env'  # __name__ hace referencia al nombre del paquete actual
        )
        config = dotenv_values(env_path)  # Carga las variables de entorno como un diccionario

        # Establecer las variables de entorno para que estén disponibles globalmente
        for key, value in config.items():
            os.environ[key] = value  # Establece cada variable de entorno

    def save_reg(self, file_path):
        """
        Guarda un registro de descarga para el usuario en el backend.
        """
        endpoint = f"{self.base_url}/downloads/"
        data = {"user_id": self.user_id, "filename": file_path}

        response = requests.post(endpoint, json=data)
        if response.status_code != 200:
            print(f"Error al registrar la descarga: {response.status_code} - {response.text}")

    def def_reg(self):
        """
        Elimina todos los registros de descargas asociados al usuario.
        """
        endpoint = f"{self.base_url}/downloads/{self.user_id}"
        response = requests.delete(endpoint)

        if response.status_code != 200:
            print(f"Error al eliminar los registros: {response.status_code} - {response.text}")
