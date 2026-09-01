import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "http://localhost:8000"
KEY = "elite-concursos-hunter-2024"
questions = [
    {
        "concurso": "Banco Central (Bacen)", "materia": "Direito Administrativo", "banca": "Cebraspe",
        "dificuldade": "Difícil", "tipo": "Múltipla Escolha",
        "enunciado": "Qual princípio rege a atuação da administração pública?",
        "alternativas": {"A": "Legalidade", "B": "Liberdade absoluta", "C": "Informalidade", "D": "Arbitrariedade"},
        "resposta_correta": "A", "explicacao": "A administração pública deve obedecer ao princípio da legalidade.",
        "pegadinha_banca": "Confundir legalidade administrativa com liberdade do particular.",
        "diagnostico_erro": "Confusão entre a legalidade administrativa e a autonomia da vontade do particular.",
        "nucleo_acerto": "Princípios expressos da administração pública: legalidade."
    },
    {
        "concurso": "Transpetro", "materia": "Língua Portuguesa", "banca": "Cesgranrio",
        "dificuldade": "Médio", "tipo": "Múltipla Escolha",
        "enunciado": "Em qual alternativa a palavra destacada exerce função de advérbio?",
        "alternativas": {"A": "O trabalho eficiente", "B": "Ele chegou cedo", "C": "A chegada do navio", "D": "O bom resultado"},
        "resposta_correta": "B", "explicacao": "Cedo modifica o verbo chegou, funcionando como advérbio.",
        "pegadinha_banca": "Confundir adjetivo com advérbio.",
        "diagnostico_erro": "Identificação inadequada da classe gramatical conforme a função na frase.",
        "nucleo_acerto": "Advérbio modifica verbo, adjetivo ou outro advérbio; em B, cedo modifica chegou."
    },
    {
        "concurso": "PMDF", "materia": "Direito Constitucional", "banca": "Instituto AOCP",
        "dificuldade": "Médio", "tipo": "Múltipla Escolha",
        "enunciado": "Qual dos direitos abaixo é considerado fundamental pela Constituição Federal?",
        "alternativas": {"A": "Direito à vida", "B": "Direito à censura", "C": "Direito à arbitrariedade", "D": "Direito à discriminação"},
        "resposta_correta": "A", "explicacao": "A Constituição assegura a inviolabilidade do direito à vida.",
        "pegadinha_banca": "Apresentar restrições como se fossem direitos fundamentais.",
        "diagnostico_erro": "Não reconhecimento dos direitos e garantias fundamentais do artigo 5º.",
        "nucleo_acerto": "O direito à vida é garantia fundamental expressamente protegida pela Constituição."
    }
]

def call(method, path, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"X-API-KEY": KEY, "Content-Type": "application/json"}
    req = Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            return r.status, json.loads(raw) if raw else {}
    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {path}: {raw}")

status, result = call("POST", "/api/v1/ingest", {"questoes": questions})
print(f"POST /api/v1/ingest: HTTP {status}")
print(json.dumps(result, ensure_ascii=False))

for info_path in ("/info", "/api/v1/info"):
    try:
        status, info = call("GET", info_path)
        print(f"GET {info_path}: HTTP {status}")
        print(json.dumps(info, ensure_ascii=False))
        break
    except RuntimeError as e:
        if info_path == "/api/v1/info":
            raise

count = None
if isinstance(info, dict):
    for key in ("count", "total", "total_questions", "questoes_count", "question_count"):
        if isinstance(info.get(key), int):
            count = info[key]
            break
    if count is None:
        for value in info.values():
            if isinstance(value, dict):
                for key in ("count", "total", "total_questions"):
                    if isinstance(value.get(key), int):
                        count = value[key]
                        break
            if count is not None:
                break
print(f"FINAL QUESTION COUNT: {count if count is not None else 'unavailable (see /info response above)'}")
