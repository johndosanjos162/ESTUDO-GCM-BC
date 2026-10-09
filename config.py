# config.py

# Substitua as chaves da OpenAI pelas do Groq
# GROQ_API_KEY: str = _get("GROQ_API_KEY") # Você pode usar este nome
# GROQ_MODEL: str = _get("GROQ_MODEL", "llama-3.3-70b-versatile") # Modelo gratuito

# Mantenha a estrutura, mas aponte para as novas variáveis
# Exemplo:
OPENAI_API_KEY: str = _get("GROQ_API_KEY") # Mude o nome da variável de ambiente
OPENAI_MODEL: str = _get("GROQ_MODEL", "llama-3.3-70b-versatile")
