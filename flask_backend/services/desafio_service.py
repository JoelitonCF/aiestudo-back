import random


def gerar_desafio_diario(disciplina, subtopico, nivel="intermediario", usuario="Aluno"):
    """Gera um desafio diário sem usar OpenAI (versão mock)."""

    questoes_exemplo = {
        "Matemática": {
            "Porcentagem": "Calcule 15% de 200.",
            "Regra de Três": "Se 3 operários fazem um trabalho em 6 dias, quantos dias levarão 2 operários?",
            "Equações": "Resolva a equação: 2x + 5 = 15"
        },
        "Língua Portuguesa": {
            "Concordância Verbal": "Complete: Os livros que comprei _____ muito interessantes.",
            "Crase": "Indique onde usar crase: Vou a escola.",
            "Pontuação": "Pontue corretamente: João meu amigo chegou cedo"
        }
    }

    # Buscar questão específica ou usar genérica
    if disciplina in questoes_exemplo and subtopico in questoes_exemplo[disciplina]:
        questao = questoes_exemplo[disciplina][subtopico]
    else:
        questao = f"Questão de {nivel} sobre {subtopico} em {disciplina}"

    return {
        "questao": questao,
        "resposta": "Resposta detalhada seria fornecida aqui.",
        "dicas": [
            f"Revise os conceitos básicos de {subtopico}",
            f"Pratique exercícios similares de {disciplina}",
            "Faça resumos dos pontos principais"
        ],
        "material_complementar": [
            f"Livro de {disciplina}",
            f"Exercícios de {subtopico}",
            "Questões de concursos anteriores"
        ],
        "nivel": nivel,
        "disciplina": disciplina,
        "subtopico": subtopico
    }
