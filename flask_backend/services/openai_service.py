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


def gerar_conteudo_completo(disciplina: str, topico: str, nivel: str = "intermediario", num_questoes: int = 10, num_flashcards: int = 8):
    """
    Gera conteúdo completo para estudo: resumo, quiz e flashcards
    """
    prompt = f"""
    Você é um tutor especializado em {disciplina}. Gere conteúdo completo para estudo sobre "{topico}" no nível {nivel}.

    Retorne **apenas** o JSON no formato abaixo, sem texto adicional:

    {{
        "resumo": {{
            "titulo": "Título do resumo",
            "conteudo": "Explicação detalhada do tópico...",
            "pontos_chave": ["Ponto 1", "Ponto 2", "Ponto 3"],
            "exemplos": ["Exemplo 1", "Exemplo 2"]
        }},
        "quiz": [
            {{
                "pergunta": "Pergunta sobre o tópico?",
                "opcoes": ["A) Opção A", "B) Opção B", "C) Opção C", "D) Opção D"],
                "resposta_correta": 0,
                "explicacao": "Explicação da resposta correta"
            }}
        ],
        "flashcards": [
            {{
                "pergunta": "Pergunta para revisão?",
                "resposta": "Resposta detalhada",
                "dica": "Dica opcional"
            }}
        ]
    }}

    Gere {num_questoes} questões para o quiz e {num_flashcards} flashcards.
    As questões devem ser de múltipla escolha com 4 opções (A, B, C, D).
    O resumo deve ser didático e completo.
    """

    try:
        client = _get_openai_client()
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um tutor especializado que gera conteúdo educacional em JSON estruturado."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        conteudo = resp.choices[0].message.content
        data = json.loads(conteudo)
        
        return {
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "resumo": data.get("resumo", {}),
            "quiz": data.get("quiz", []),
            "flashcards": data.get("flashcards", [])
        }
    except (OpenAIError, RuntimeError, json.JSONDecodeError) as e:
        return {"erro": str(e)}


def gerar_resumo_estudo(disciplina: str, topico: str, nivel: str = "intermediario"):
    """
    Gera apenas um resumo de estudo sobre o tópico
    """
    prompt = f"""
    Você é um tutor especializado em {disciplina}. Crie um resumo didático sobre "{topico}" no nível {nivel}.

    Retorne **apenas** o JSON no formato abaixo:

    {{
        "titulo": "Título do resumo",
        "conteudo": "Explicação detalhada e didática do tópico...",
        "pontos_chave": ["Ponto importante 1", "Ponto importante 2", "Ponto importante 3"],
        "exemplos": ["Exemplo prático 1", "Exemplo prático 2"],
        "dicas": ["Dica de estudo 1", "Dica de estudo 2"]
    }}
    """

    try:
        client = _get_openai_client()
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um tutor especializado que cria resumos didáticos em JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        conteudo = resp.choices[0].message.content
        data = json.loads(conteudo)
        
        return {
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "resumo": data
        }
    except (OpenAIError, RuntimeError, json.JSONDecodeError) as e:
        return {"erro": str(e)}


def gerar_quiz_ia(disciplina: str, topico: str, num_questoes: int = 10, nivel: str = "intermediario"):
    """
    Gera apenas um quiz sobre o tópico
    """
    prompt = f"""
    Você é um gerador de questões de concurso. Gere {num_questoes} questões objetivas 
    nível {nivel} sobre "{topico}" da disciplina "{disciplina}".

    Retorne **apenas** o JSON no formato abaixo:

    {{
        "questoes": [
            {{
                "pergunta": "Pergunta sobre o tópico?",
                "opcoes": ["A) Opção A", "B) Opção B", "C) Opção C", "D) Opção D"],
                "resposta_correta": 0,
                "explicacao": "Explicação da resposta correta"
            }}
        ]
    }}
    """

    try:
        client = _get_openai_client()
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um gerador de questões de concurso em JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        conteudo = resp.choices[0].message.content
        data = json.loads(conteudo)
        
        return {
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "questoes": data.get("questoes", [])
        }
    except (OpenAIError, RuntimeError, json.JSONDecodeError) as e:
        return {"erro": str(e)}


def gerar_flashcards_ia(disciplina: str, topico: str, num_flashcards: int = 8, nivel: str = "intermediario"):
    """
    Gera apenas flashcards sobre o tópico
    """
    prompt = f"""
    Você é um tutor especializado em {disciplina}. Gere {num_flashcards} flashcards 
    para revisão sobre "{topico}" no nível {nivel}.

    Retorne **apenas** o JSON no formato abaixo:

    {{
        "flashcards": [
            {{
                "pergunta": "Pergunta para revisão?",
                "resposta": "Resposta detalhada e didática",
                "dica": "Dica opcional para ajudar na memorização"
            }}
        ]
    }}
    """

    try:
        client = _get_openai_client()
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um tutor especializado que cria flashcards educacionais em JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        conteudo = resp.choices[0].message.content
        data = json.loads(conteudo)
        
        return {
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "flashcards": data.get("flashcards", [])
        }
    except (OpenAIError, RuntimeError, json.JSONDecodeError) as e:
        return {"erro": str(e)}
