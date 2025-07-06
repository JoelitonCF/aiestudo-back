import math
from datetime import date, timedelta
from flask_backend.services import curriculo_service


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
