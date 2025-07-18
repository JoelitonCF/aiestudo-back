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


def gerar_desafio_diario(disciplina, subtopico, nivel="intermediario", usuario="Aluno"):
    """Gera um desafio diário personalizado usando OpenAI."""
    client = _get_openai_client()

    prompt = f"""
    Crie um desafio de estudo para {usuario} sobre:
    - Disciplina: {disciplina}
    - Subtópico: {subtopico}
    - Nível: {nivel}
    
    O desafio deve incluir:
    1. Uma questão prática ou teórica
    2. Explicação detalhada da resposta
    3. Dicas de estudo relacionadas
    4. Material complementar sugerido
    
    Formato: JSON com as chaves: questao, resposta, dicas, material_complementar
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em educação e concursos públicos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        content = response.choices[0].message.content

        # Tentar fazer parse do JSON
        try:
            desafio = json.loads(content)
        except json.JSONDecodeError:
            # Se não for JSON válido, retornar como texto
            desafio = {
                "questao": content,
                "resposta": "Consulte materiais de estudo",
                "dicas": ["Estude regularmente", "Pratique exercícios"],
                "material_complementar": ["Livros da disciplina", "Questões de concursos anteriores"]
            }

        return desafio

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")


def gerar_plano_estudo(concurso, cargo, tempo_disponivel, disciplinas_foco=None):
    """Gera um plano de estudos personalizado."""
    client = _get_openai_client()

    disciplinas_texto = ", ".join(
        disciplinas_foco) if disciplinas_foco else "todas as disciplinas do edital"

    prompt = f"""
    Crie um plano de estudos personalizado para:
    - Concurso: {concurso}
    - Cargo: {cargo}
    - Tempo disponível: {tempo_disponivel} horas por dia
    - Foco em: {disciplinas_texto}
    
    O plano deve incluir:
    1. Cronograma semanal detalhado
    2. Distribuição de tempo por disciplina
    3. Metas semanais e mensais
    4. Estratégias de revisão
    5. Material de estudo recomendado
    
    Formato: JSON estruturado com cronograma, metas, estrategias, materiais
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em planejamento de estudos para concursos públicos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.6
        )

        content = response.choices[0].message.content

        try:
            plano = json.loads(content)
        except json.JSONDecodeError:
            plano = {
                "cronograma": content,
                "metas": ["Estudar consistentemente", "Resolver questões"],
                "estrategias": ["Revisão espaçada", "Simulados regulares"],
                "materiais": ["Livros especializados", "Questões de concursos"]
            }

        return plano

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")


def gerar_questoes_quiz(disciplina, subtopico, num_questoes=5, nivel="intermediario"):
    """Gera questões para um quiz usando OpenAI."""
    client = _get_openai_client()

    prompt = f"""
    Crie {num_questoes} questões de múltipla escolha sobre:
    - Disciplina: {disciplina}
    - Subtópico: {subtopico}
    - Nível: {nivel}
    
    Cada questão deve ter:
    - Enunciado claro
    - 5 alternativas (A, B, C, D, E)
    - Resposta correta
    - Explicação da resposta
    
    Formato: JSON array com objetos contendo: enunciado, alternativas, resposta_correta, explicacao
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em elaboração de questões para concursos públicos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        content = response.choices[0].message.content

        try:
            questoes = json.loads(content)
        except json.JSONDecodeError:
            # Fallback se não conseguir fazer parse
            questoes = [{
                "enunciado": "Questão sobre " + subtopico,
                "alternativas": ["A) Opção A", "B) Opção B", "C) Opção C", "D) Opção D", "E) Opção E"],
                "resposta_correta": "A",
                "explicacao": "Consulte material de estudo específico."
            }]

        return questoes

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")


def gerar_resumo(disciplina, topico, nivel="intermediario"):
    """Gera um resumo didático sobre um tópico."""
    client = _get_openai_client()

    prompt = f"""
    Crie um resumo didático sobre:
    - Disciplina: {disciplina}
    - Tópico: {topico}
    - Nível: {nivel}
    
    O resumo deve incluir:
    1. Conceitos principais
    2. Pontos importantes para memorizar
    3. Exemplos práticos
    4. Dicas para concursos
    
    Formato: Texto bem estruturado e didático
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um professor especialista em concursos públicos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.6
        )

        return response.choices[0].message.content

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")


def gerar_plano_aula(disciplina, topico, nivel="intermediario"):
    """Gera um plano de aula estruturado."""
    client = _get_openai_client()

    prompt = f"""
    Crie um plano de aula sobre:
    - Disciplina: {disciplina}
    - Tópico: {topico}
    - Nível: {nivel}
    
    O plano deve incluir:
    1. Objetivos da aula
    2. Conteúdo programático
    3. Metodologia
    4. Atividades práticas
    5. Avaliação
    6. Bibliografia
    
    Formato: JSON estruturado
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "Você é um especialista em planejamento educacional."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.6
        )

        content = response.choices[0].message.content

        try:
            plano = json.loads(content)
        except json.JSONDecodeError:
            plano = {
                "objetivos": ["Compreender " + topico],
                "conteudo": content,
                "metodologia": "Aula expositiva e exercícios",
                "atividades": ["Leitura", "Exercícios"],
                "avaliacao": "Questionário",
                "bibliografia": ["Material especializado"]
            }

        return plano

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")


def gerar_exercicios(disciplina, topico, nivel="intermediario"):
    """Gera uma lista de exercícios práticos."""
    client = _get_openai_client()

    prompt = f"""
    Crie uma lista de exercícios práticos sobre:
    - Disciplina: {disciplina}
    - Tópico: {topico}
    - Nível: {nivel}
    
    Os exercícios devem incluir:
    1. 5 exercícios variados
    2. Diferentes tipos (cálculo, análise, aplicação)
    3. Gabarito com resolução
    4. Dicas de resolução
    
    Formato: JSON array com objetos contendo: enunciado, tipo, resolucao, dicas
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em elaboração de exercícios educacionais."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        content = response.choices[0].message.content

        try:
            exercicios = json.loads(content)
        except json.JSONDecodeError:
            exercicios = [{
                "enunciado": f"Exercício sobre {topico}",
                "tipo": "aplicacao",
                "resolucao": "Consulte material específico",
                "dicas": ["Revise conceitos básicos", "Pratique regularmente"]
            }]

        return exercicios

    except OpenAIError as e:
        raise RuntimeError(f"Erro na API OpenAI: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {str(e)}")
