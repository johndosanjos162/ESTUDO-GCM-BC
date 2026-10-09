# ai/generator.py

from openai import OpenAI
# from config import OPENAI_API_KEY, OPENAI_MODEL # ajuste os imports conforme config.py

# Substitua a linha de criação do cliente
# _client = OpenAI(api_key=OPENAI_API_KEY)
# Por esta:
_client = OpenAI(
    api_key=OPENAI_API_KEY, # que agora contém a chave do Groq
    base_url="https://api.groq.com/openai/v1" # URL base da API do Groq
)
