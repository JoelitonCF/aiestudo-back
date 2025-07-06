# flask_backend/services/openai_service.py
import os
import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()


def _get_openai_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY não definido. Exporte ou coloque no .env"
        )
    return OpenAI(api_key=key)


def gerar_desafio_ia(usuario: str, disciplina: str, subtopico: str, nivel: str):
    prompt = (
        f"Você é um gerador de questões de concurso. Gere **3 questões objetivas** "
        f"nível {nivel} sobre o sub-tópico \"{subtopico}\" da disciplina \"{disciplina}\". "
        "Retorne **apenas** o JSON no formato abaixo, sem texto adicional:\n\n"
        "{\n"
        "  \"questoes\": [\n"
        "    {\n"
        "      \"pergunta\": \"...\",\n"
        "      \"opcoes\": [\"A\", \"B\", \"C\", \"D\"],\n"
        "      \"resposta_correta\": \"A\",\n"
        "      \"explicacao\": \"...\"\n"
        "    },\n"
        "    {...},\n"
        "    {...}\n"
        "  ]\n"
        "}"
    )
    try:
        client = _get_openai_client()
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "Você é um gerador de questões de concurso em JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        conteudo = resp.choices[0].message.content
        data = json.loads(conteudo)
        return {
            "usuario": usuario,
            "disciplina": disciplina,
            "subtopico": subtopico,
            "questoes": data["questoes"]
        }
    except (OpenAIError, RuntimeError) as e:
        return {"erro": str(e)}
