"""Servicio de integración con Google Gemini API para generación de respuestas IA."""
import os
from typing import List

import google.generativeai as genai
from app.domain import IGeminiService
from app.domain.entities import ChatMessage, Product


class GeminiService(IGeminiService):
    """Servicio para integración con Google Generative AI (Gemini).

    Maneja la comunicación con la API de Google Gemini para generar
    respuestas contextuales de atención al cliente basadas en productos
    disponibles e historial de conversación.
    """

    def __init__(self, api_key: str) -> None:
        """Inicializa el servicio con la API key de Google Gemini.

        Parámetros:
            api_key: Clave de autenticación para acceder a Google Generative AI.

        Excepciones:
            ValueError: Si la API key es vacía o None.
        """
        if not api_key:
            raise ValueError("API key de Gemini no puede estar vacía")

        self.api_key = api_key
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(model_name)

    def _build_prompt(
        self,
        user_message: str,
        history: List[ChatMessage],
        products: List[Product],
    ) -> str:
        """Construye el prompt formateado para enviar a Gemini.

        Combina la instrucción del sistema, historial de conversación,
        productos disponibles y mensaje actual en un prompt cohesivo.

        Parámetros:
            user_message: Mensaje actual del usuario.
            history: Historial de mensajes anteriores de la conversación.
            products: Lista de productos disponibles para recomendar.

        Retorna:
            String formateado con el prompt completo para Gemini.
        """
        # Instrucción del sistema
        system_instruction = """Eres un asistente de atención al cliente de una tienda de zapatos online.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.
Responde de forma amigable, coherente y basada en los productos disponibles.
Si no tienes el producto que busca, sugiere alternativas.
Si solicita una compra, confirma detalles (talla, cantidad, precio).
Mantén respuestas concisas pero informativas."""

        # Formatear productos disponibles
        products_text = "Productos disponibles:\n"
        if products:
            for product in products:
                products_text += f"- {product.name} ({product.brand}): Talla {product.size}, Color {product.color}, Precio ${product.price}, Stock {product.stock}\n"
        else:
            products_text += "- No hay productos disponibles en este momento.\n"

        # Formatear historial de conversación
        history_text = "Historial de conversación:\n"
        if history:
            for msg in history:
                role_label = "Cliente" if msg.is_user_message() else "Asistente"
                history_text += f"{role_label}: {msg.message}\n"
        else:
            history_text += "- Esta es la primera pregunta del cliente.\n"

        # Construir prompt completo
        prompt = f"""{system_instruction}

{products_text}

{history_text}

Cliente: {user_message}

Responde como un asistente amable y profesional de la tienda:"""

        return prompt

    def get_response(
        self,
        user_message: str,
        history: List[ChatMessage],
        products: List[Product],
    ) -> str:
        """Obtiene una respuesta de Gemini basada en el contexto de la conversación.

        Envía un prompt formateado a Google Gemini incluyendo el historial
        de conversación y los productos disponibles.

        Parámetros:
            user_message: Mensaje actual del usuario.
            history: Historial de mensajes de la sesión.
            products: Lista de productos disponibles en el catálogo.

        Retorna:
            String con la respuesta generada por Gemini.

        Excepciones:
            Exception: Si hay un error en la comunicación con Gemini API.
        """
        try:
            prompt = self._build_prompt(user_message, history, products)
            response = self.model.generate_content(
                prompt,
                request_options={"timeout": 30},
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error al comunicarse con Gemini API: {str(e)}")
