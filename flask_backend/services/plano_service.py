from flask_backend.database import db
from flask_backend.services.curriculo_service import obter_curriculo
from flask_backend.services import openai_service
from datetime import datetime, timedelta
import uuid
import math
from datetime import date


def _get_topic_name(val, chave):
    if isinstance(val, dict):
        if "titulo" in val and isinstance(val["titulo"], str):
            return val["titulo"]
        desc = val.get("descricao")
        if isinstance(desc, str):
            return desc
        if isinstance(desc, list):
            return ", ".join(str(x) for x in desc)
    return chave


def _get_subtopics(val):
    subs = []
    if isinstance(val, dict):
        for k, v in val.items():
            if k in ("descricao", "titulo"):
                continue
            if isinstance(v, str):
                subs.append(v)
            elif isinstance(v, list):
                subs.extend(str(x) for x in v if isinstance(x, str))
            elif isinstance(v, dict):
                subdesc = v.get("descricao")
                if isinstance(subdesc, str):
                    subs.append(subdesc)
    return subs


def _normalizar_curriculo(curr):
    disciplinas = []
    for slug, bloco in curr["disciplinas"].items():
        nome_disc = bloco.get("nome", slug.replace("_", " ").title())
        topicos = []
        for key, val in bloco.items():
            if key == "nome":
                continue
            if isinstance(val, str):
                topicos.append({"nome": val, "subtopicos": []})
            else:
                nome_top = _get_topic_name(val, key)
                subs = _get_subtopics(val)
                topicos.append({"nome": nome_top, "subtopicos": subs})
        disciplinas.append({"nome": nome_disc, "topicos": topicos})
    return disciplinas


def gerar_plano(usuario_id, concurso, cargo, tempo_disponivel=2, data_prova=None, disciplinas_foco=None):
    """Gera um plano de estudos personalizado."""
    plano_id = str(uuid.uuid4())

    # Buscar currículo do concurso
    try:
        curriculo = obter_curriculo(concurso, cargo)
        if not curriculo:
            raise ValueError(
                f"Currículo não encontrado para {concurso} - {cargo}")
    except Exception:
        curriculo = {"disciplinas": disciplinas_foco or ["Disciplina Geral"]}

    # Gerar plano usando OpenAI
    try:
        plano_openai = openai_service.gerar_plano_estudo(
            concurso=concurso,
            cargo=cargo,
            tempo_disponivel=tempo_disponivel,
            disciplinas_foco=disciplinas_foco
        )
    except Exception as e:
        # Fallback se OpenAI falhar
        plano_openai = _gerar_plano_fallback(
            concurso, cargo, tempo_disponivel, disciplinas_foco)

    # Calcular datas se data_prova foi fornecida
    cronograma = _calcular_cronograma(
        data_prova, tempo_disponivel) if data_prova else None

    plano_data = {
        "usuario_id": usuario_id,
        "concurso": concurso,
        "cargo": cargo,
        "tempo_disponivel": tempo_disponivel,
        "data_prova": data_prova,
        "disciplinas_foco": disciplinas_foco or [],
        "plano_gerado": plano_openai,
        "cronograma": cronograma,
        "data_criacao": datetime.utcnow(),
        "ativo": True,
        "progresso": 0
    }

    db.collection("planos").document(plano_id).set(plano_data)
    return plano_id


def listar_planos_usuario(usuario_id):
    """Lista planos de um usuário."""
    docs = db.collection("planos").where(
        "usuario_id", "==", usuario_id).where("ativo", "==", True).stream()

    planos = []
    for doc in docs:
        plano = doc.to_dict()
        plano["id"] = doc.id
        planos.append(plano)

    return planos


def obter_plano(plano_id):
    """Obtém um plano específico."""
    doc = db.collection("planos").document(plano_id).get()

    if not doc.exists:
        return None

    plano = doc.to_dict()
    plano["id"] = doc.id
    return plano


def atualizar_plano(plano_id, dados):
    """Atualiza um plano de estudos."""
    dados["data_atualizacao"] = datetime.utcnow()
    db.collection("planos").document(plano_id).update(dados)


def deletar_plano(plano_id):
    """Deleta um plano de estudos."""
    db.collection("planos").document(plano_id).update({"ativo": False})


def atualizar_progresso_plano(plano_id, progresso):
    """Atualiza o progresso de um plano."""
    db.collection("planos").document(plano_id).update({
        "progresso": progresso,
        "ultima_atualizacao": datetime.utcnow()
    })


def _gerar_plano_fallback(concurso, cargo, tempo_disponivel, disciplinas_foco):
    """Gera um plano básico caso a OpenAI falhe."""
    return {
        "cronograma": {
            "segunda": f"{tempo_disponivel//7} horas - Disciplina 1",
            "terca": f"{tempo_disponivel//7} horas - Disciplina 2",
            "quarta": f"{tempo_disponivel//7} horas - Disciplina 3",
            "quinta": f"{tempo_disponivel//7} horas - Disciplina 4",
            "sexta": f"{tempo_disponivel//7} horas - Revisão",
            "sabado": f"{tempo_disponivel//7} horas - Simulados",
            "domingo": f"{tempo_disponivel//7} horas - Descanso/Revisão"
        },
        "metas": [
            "Completar teoria básica em 30 dias",
            "Resolver 100 questões por semana",
            "Fazer 2 simulados por mês"
        ],
        "estrategias": [
            "Revisão espaçada",
            "Intercalar teoria e prática",
            "Simulados regulares"
        ],
        "materiais": [
            "Livros especializados",
            "Questões de concursos anteriores",
            "Videoaulas"
        ]
    }


def _calcular_cronograma(data_prova, tempo_disponivel):
    """Calcula cronograma baseado na data da prova."""
    try:
        data_prova_obj = datetime.strptime(data_prova, "%Y-%m-%d")
        dias_restantes = (data_prova_obj - datetime.now()).days

        if dias_restantes <= 0:
            return {"aviso": "Data da prova já passou ou é hoje"}

        total_horas = dias_restantes * tempo_disponivel

        return {
            "dias_restantes": dias_restantes,
            "total_horas_estudo": total_horas,
            "horas_por_semana": tempo_disponivel * 7,
            "fases": {
                "teoria": f"{int(total_horas * 0.6)} horas",
                "exercicios": f"{int(total_horas * 0.3)} horas",
                "revisao": f"{int(total_horas * 0.1)} horas"
            }
        }
    except ValueError:
        return {"erro": "Formato de data inválido. Use YYYY-MM-DD"}


def gerar_plano(concurso, cargo, dias=30):
    curr = curriculo_service.obter_curriculo(concurso, cargo)
    if not curr:
        return None

    disciplinas = _normalizar_curriculo(curr)
    # resto da lógica inalterada...
    subs = []
    for disc in disciplinas:
        for top in disc["topicos"]:
            if top["subtopicos"]:
                for sub in top["subtopicos"]:
                    subs.append({
                        "disciplina": disc["nome"],
                        "topico": top["nome"],
                        "subtopico": sub
                    })
            else:
                subs.append({
                    "disciplina": disc["nome"],
                    "topico": top["nome"],
                    "subtopico": top["nome"]
                })

    total = len(subs)
    per_day = math.ceil(total / dias)
    plano = []
    today = date.today()
    idx = 0
    for i in range(dias):
        dia = today + timedelta(days=i)
        slice_ = subs[idx: idx + per_day]
        if not slice_:
            break
        plano.append({"data": dia.isoformat(), "itens": slice_})
        idx += per_day

    return {
        "concurso": concurso,
        "cargo": cargo,
        "dias": len(plano),
        "plano": plano
    }
