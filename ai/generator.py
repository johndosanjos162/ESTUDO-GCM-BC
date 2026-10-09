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
# ai/generator.py (trecho da função gerar_questoes)

from openai import APIStatusError

def gerar_questoes(disciplina: str, quantidade: int = 5, dificuldade: str = "medio", salvar: bool = True) -> list:
    try:
        # ... (lógica de geração de questões) ...
    except APIStatusError as e:
        if e.status_code == 429 and "credit_balance_exhausted" in str(e):
            raise Exception("Sua conta na OpenAI está sem créditos. Por favor, adicione fundos ou troque para um provedor gratuito como o Groq.") from e
        else:
            raise e
    except Exception as e:
        # ... (outros tratamentos de erro) ...
        raise e
