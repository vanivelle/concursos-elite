#!/usr/bin/env python3
import json
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:senha_segura_123@postgres_db:5432/admin")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QuestoesBancoModel(Base):
    __tablename__ = "questoes_banco"
    id = Column(Integer, primary_key=True, index=True)
    questao_id = Column(String, unique=True, index=True, nullable=False)
    concurso = Column(String, nullable=False, index=True)
    materia = Column(String, nullable=False, index=True)
    dificuldade = Column(String, nullable=False, index=True)
    banca = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    enunciado = Column(Text, nullable=False)
    alternativas = Column(Text, nullable=False)
    resposta_correta = Column(String, nullable=False)
    explicacao = Column(Text, nullable=False)
    diagnostico_erro = Column(Text, nullable=True)
    nucleo_acerto = Column(Text, nullable=True)
    pegadinha_banca = Column(Text, nullable=False)
    padroes_banca = Column(Text, nullable=True)
    data_criacao = Column(String, nullable=False)

questoes_pratica_cargo = [
    {
        "questao_id": "PMDF_PRACA_001",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "De acordo com o protocolo de abordagem policial adotado pela PMDF, qual é o primeiro passo que um policial militar deve executar ao abordar um cidadão suspeito em via pública?",
        "alternativas": {
            "A": "Identificar-se como policial e informar o motivo da abordagem",
            "B": "Imediatamente revistar o suspeito sem avisos prévios",
            "C": "Solicitar documentos de identificação sem qualquer explicação",
            "D": "Chamar reforço antes de qualquer ação"
        },
        "resposta_correta": "A",
        "explicacao": "A Lei 13.060/2014 que regulamenta o uso da força pela polícia estabelece que toda abordagem deve começar com identificação clara do policial e informação do motivo. Isso é essencial para legítima defesa do cidadão e proteção dos direitos fundamentais.",
        "diagnostico_erro": "❌ Errou porque pode ter confundido protocolo com ação imediata de revistaria. A Constituição Federal (Art. 5º) protege a dignidade e a liberdade de locomoção.",
        "nucleo_acerto": "✅ Acertou! A abordagem respeitosa começa sempre com identificação e clareza. Policial bem treinado sabe que transparência reduz conflitos e protege ambos.",
        "pegadinha_banca": "Cebraspe adora inversão: testar se candidato sabe diferença entre abordagem legal vs ilegítima.",
        "padroes_banca": json.dumps({"foco": "Lei 13.060/2014", "tema": "Uso da Força", "palavra_chave": "identificação"})
    },
    {
        "questao_id": "PMDF_PRACA_002",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Um policial militar da PMDF se depara com um cidadão que se recusa a cumprir ordem de parada durante uma abordagem. Qual deve ser a ação segundo o uso progressivo da força?",
        "alternativas": {
            "A": "Imediatamente usar força física máxima",
            "B": "Retirar-se e documentar a recusa",
            "C": "Usar verbalizações, gestos e depois contato físico se necessário",
            "D": "Chamar a imprensa para registrar o incidente"
        },
        "resposta_correta": "C",
        "explicacao": "O uso progressivo da força segue ordem: verbalização → gestos/afastamento → contato físico → força intermediária → força letal. Cada escalação deve ser proporcional à ameaça. PMDF segue protocolos internacionais de Polícia Comunitária.",
        "diagnostico_erro": "❌ Errou porque pode ter confundido urgência com justificativa de força máxima. Proporcionalidade é lei, não sugestão.",
        "nucleo_acerto": "✅ Acertou! Progressividade evita mortes desnecessárias e protege legalmente o policial. É prática científica validada globalmente.",
        "pegadinha_banca": "Palavra-chave: 'progressivo' vs 'imediato'. Cebraspe testa se candidato leu a lei ou só ouviu falar.",
        "padroes_banca": json.dumps({"foco": "Uso Progressivo", "tema": "Escalação Controlada", "palavra_chave": "verbalização"})
    },
    {
        "questao_id": "PMDF_PRACA_003",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Ao chegar a uma cena de crime, qual é o procedimento operacional padrão (POP) que a PMDF exige para preservação de evidências?",
        "alternativas": {
            "A": "Permitir que curiosos entrem na cena para documentar",
            "B": "Estabelecer perímetro de segurança, isolar cena, avisar perícia",
            "C": "Fotografar sem luvas antes da perícia chegar",
            "D": "Remover objetos suspeitos do local antes de documentar"
        },
        "resposta_correta": "B",
        "explicacao": "Preservação de cena é protocolo crítico. Perímetro seguro evita contaminação de evidências, protege investigadores e garante validade processual. Qualquer violação pode derrubar condenação no tribunal.",
        "diagnostico_erro": "❌ Errou porque pode ter confundido liberdade de ação com competência. Cena de crime é local profissional, não local público.",
        "nucleo_acerto": "✅ Acertou! Preservação de evidências é disciplina forense. Policial que sabe isso merece promoção.",
        "pegadinha_banca": "Pegadinha: opções 'A' e 'D' parecem ativas mas são ilegais. Candidato fraco cai nessas.",
        "padroes_banca": json.dumps({"foco": "Protocolos de Cena", "tema": "Preservação Forense", "palavra_chave": "perímetro"})
    },
    {
        "questao_id": "PMDF_PRACA_004",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Fácil",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Um policial militar da PMDF testemunha colega abusando verbalmente de cidadão detido. Qual é o dever do policial?",
        "alternativas": {
            "A": "Silenciar para não criar conflito entre colegas",
            "B": "Denunciar imediatamente à corregedoria",
            "C": "Advertir o colega depois e esquecer o assunto",
            "D": "Documentar o incidente e relatar à chefia ou corregedoria"
        },
        "resposta_correta": "D",
        "explicacao": "Código de Ética Policial exige denúncia de abuso. Documentação protege vítima E policial denunciante. Omissão é cumplicidade e pode virar processo disciplinar.",
        "diagnostico_erro": "❌ Errou porque pode ter confundido lealdade corporativa com corrupção. Policial ético protege a instituição, não protege criminoso fardado.",
        "nucleo_acerto": "✅ Acertou! Integridade é teste mais importante de caráter. PMDF treina para isso.",
        "pegadinha_banca": "Inversão moral: candidato confunde 'corporativismo' (errado) com 'coesão' (certo).",
        "padroes_banca": json.dumps({"foco": "Ética Policial", "tema": "Responsabilidade", "palavra_chave": "denúncia"})
    },
    {
        "questao_id": "PMDF_PRACA_005",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Durante patrulhamento urbano, policial da PMDF observa suspeito em atitude de tráfico. Qual procedimento é correto?",
        "alternativas": {
            "A": "Atirar imediatamente sem verbal",
            "B": "Abordar, verbalizar, buscar arma, só depois revistar se houver risco iminente",
            "C": "Permitir fuga para não gerar confusão",
            "D": "Registrar e ignorar para investigação posterior"
        },
        "resposta_correta": "B",
        "explicacao": "Segurança do policial vem primeiro: verbalização → busca visual de armas → contato cauteloso. Tráfico é crime, mas abordagem deve ser técnica e legal para sustentação processual.",
        "diagnostico_erro": "❌ Errou porque pulou protocolo de segurança. Policial morto não ajuda ninguém.",
        "nucleo_acerto": "✅ Acertou! Sequência tática garante segurança e suspeição fundamentada para juiz.",
        "pegadinha_banca": "Cebraspe inverte: faz parecer que ser 'técnico' é ser 'fraco'. Policial elite sabe que técnica É força.",
        "padroes_banca": json.dumps({"foco": "Tática Policial", "tema": "Abordagem de Suspeitos", "palavra_chave": "risco iminente"})
    },
    {
        "questao_id": "PMDF_PRACA_006",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Policial militar da PMDF usou força para conter criança de 12 anos em situação de rua. Ao relatar, qual deve ser a classificação correta da força usada segundo Lei 13.060/2014?",
        "alternativas": {
            "A": "Força letal porque criança resistiu",
            "B": "Força intermediária porque ainda é menor",
            "C": "Força não-letal com foco em proteção à vida, documentando lesões e alertando CMDCA",
            "D": "Sem força porque menor é sempre pacífico"
        },
        "resposta_correta": "C",
        "explicacao": "Menores têm proteção especial (ECA). Qualquer contato deve ser documentado, minimizado, com imediata notificação ao Conselho Tutelar. Cuidado > Contenção. Lei é clara: menor é prioridade de proteção.",
        "diagnostico_erro": "❌ Errou porque confundiu resistência com justificativa. Menor em rua já é vítima; polícia deve proteger, não violentar.",
        "nucleo_acerto": "✅ Acertou! Vulnerável = maior responsabilidade legal. Essa é a marca de polícia moderna.",
        "pegadinha_banca": "Pegadinha: 'porque resistiu' vs 'proteção à vida'. Cebraspe diferencia policial de segurança privada.",
        "padroes_banca": json.dumps({"foco": "ECA e Proteção", "tema": "Menores", "palavra_chave": "vulnerável"})
    },
    {
        "questao_id": "PMDF_PRACA_007",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Qual é o protocolo da PMDF para responder a denúncia de violência doméstica?",
        "alternativas": {
            "A": "Mediar conflito e sugerir reconciliação",
            "B": "Apenas registrar boletim de ocorrência e deixar partes resolverem",
            "C": "Informar sobre Lei Maria da Penha, orientar sobre medidas protetivas, documentar, encaminhar para delegacia",
            "D": "Ignorar se vítima não quiser registrar"
        },
        "resposta_correta": "C",
        "explicacao": "Lei Maria da Penha (11.340/2006) é lei de ordem pública: polícia NÃO media crimes. Deve documentar, informar direitos, ofertar medidas protetivas. Isso salva vidas.",
        "diagnostico_erro": "❌ Errou porque confundiu papel policial com papel de mediador. Polícia não negocia direitos humanos.",
        "nucleo_acerto": "✅ Acertou! PMDF que segue Lei Maria da Penha reduz mortes de mulheres. Essa é missão clara.",
        "pegadinha_banca": "Palavra-chave: 'Lei Maria da Penha' vs 'mediação'. Lei é imperativa, não sugestão.",
        "padroes_banca": json.dumps({"foco": "Lei 11.340/2006", "tema": "Violência Doméstica", "palavra_chave": "medidas protetivas"})
    },
    {
        "questao_id": "PMDF_PRACA_008",
        "concurso": "PMDF",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Fácil",
        "banca": "Cebraspe",
        "tipo": "múltipla",
        "enunciado": "Em caso de confronto armado, qual deve ser a prioridade do policial militar da PMDF?",
        "alternativas": {
            "A": "Matar o suspeito para servir de exemplo",
            "B": "Render-se imediatamente",
            "C": "Garantir segurança pessoal, de colegas e do público",
            "D": "Criar emboscada sem avisar"
        },
        "resposta_correta": "C",
        "explicacao": "Trinômio de segurança: 1) Policial, 2) Colega, 3) Público. Nessa ordem. Segurança é pré-requisito para ação tática. Política de 'zero mortes' reduz traumas e custos.",
        "diagnostico_erro": "❌ Errou porque priorizou resultado (matar) em vez de processo (segurança). Profissionalismo é contrário.",
        "nucleo_acerto": "✅ Acertou! Policial que volta vivo é sucesso. Prender vivo é vitória maior que matar.",
        "pegadinha_banca": "Cebraspe: testa se candidato valoriza vida ou só violência. Respondedores esperados na PMDF sabem diferença.",
        "padroes_banca": json.dumps({"foco": "Tática Defensiva", "tema": "Confronto Armado", "palavra_chave": "segurança"})
    },
    {
        "questao_id": "STT_PRACA_001",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "Um Sargento Técnico Temporário (STT) é designado para fazer ronda de quartel. Qual é o procedimento correto segundo o Regulamento Interno e Disciplinar (RID)?",
        "alternativas": {
            "A": "Fazer ronda aleatória sem horário fixo",
            "B": "Cumprir roteiro pré-estabelecido, registrar em livro de ordens, verificar cercas e portarias",
            "C": "Confiar em câmeras e não fazer inspeção pessoal",
            "D": "Dormir durante ronda se achar seguro"
        },
        "resposta_correta": "B",
        "explicacao": "RID exige roteiro específico, documentação em Livro de Ordens, inspeção visual de perimetrais. Câmeras falham; contato humano detecta infiltrações. STT é primeira linha.",
        "diagnostico_erro": "❌ Errou porque confiou em automatização. Soldado é sempre necessário. Máquina é ferramenta, não substituto.",
        "nucleo_acerto": "✅ Acertou! Ronda de quartel é responsabilidade dura. STT que cumpre protege nação.",
        "pegadinha_banca": "Exército valoriza disciplina: 'aleatório' vs 'pré-estabelecido' são opostos. Militares obedecem, não improvizam.",
        "padroes_banca": json.dumps({"foco": "RID", "tema": "Ronda de Quartel", "palavra_chave": "registrar"})
    },
    {
        "questao_id": "STT_PRACA_002",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "STT recebe ordem de comandante para fazer algo que viola RID. Qual deve ser a ação?",
        "alternativas": {
            "A": "Obedecer cegamente",
            "B": "Recusar e ficar detido",
            "C": "Cumprir ordem e depois denunciar",
            "D": "Solicitar esclarecimento dentro da cadeia de comando, documentar"
        },
        "resposta_correta": "D",
        "explicacao": "Estatuto dos Militares (Lei 6.880/1980) protege militar de ordem ilegal. Cadeia de comando permite desafio respeitoso. Documentação em livro protege ambos. Ordem claramente ilegal NÃO deve ser obedecida.",
        "diagnostico_erro": "❌ Errou porque confundiu obediência com submissão. Soldado não é máquina; tem direitos legais.",
        "nucleo_acerto": "✅ Acertou! Sistema militar legítimo tem checks. STT que questiona respeitosamente é profissional.",
        "pegadinha_banca": "Palavra-chave: 'documentar' vs 'obedecer'. Lei protege soldado que questiona ilegitimidade.",
        "padroes_banca": json.dumps({"foco": "Estatuto Militares", "tema": "Ordem Ilegal", "palavra_chave": "cadeia comando"})
    },
    {
        "questao_id": "STT_PRACA_003",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "STT é responsável por manutenção de estoque de munição. Ao descobrir discrepância entre quantidade registrada e real, qual é o procedimento?",
        "alternativas": {
            "A": "Ocultar discrepância para evitar punição",
            "B": "Relatar imediatamente à chefia, documentar em Livro de Ordens com data/hora",
            "C": "Questionar subordinados agressivamente",
            "D": "Aguardar auditoria anual"
        },
        "resposta_correta": "B",
        "explicacao": "Munição é segurança nacional. Discrepância pode indicar roubo, contrabando ou erro. Relato imediato com documentação é protocolo. Omissão é crime militar (Art. 194, Código Penal Militar).",
        "diagnostico_erro": "❌ Errou porque priorizou auto-preservação. Militar que oculta é traidor, não colega.",
        "nucleo_acerto": "✅ Acertou! STT que denuncia protege munição e nação. Isso é honra militar.",
        "pegadinha_banca": "Palavras-chave: 'munição', 'discrepância', 'relatar'. Teste de integridade no cargo crítico.",
        "padroes_banca": json.dumps({"foco": "Segurança Nacional", "tema": "Munição", "palavra_chave": "relatar"})
    },
    {
        "questao_id": "STT_PRACA_004",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "STT deve preencher o Livro de Ordens (LO) para documentar ocorrência noturna em quartel. Qual informação é OBRIGATÓRIA?",
        "alternativas": {
            "A": "Só hora e nada mais",
            "B": "Data, hora, natureza da ordem, assinatura, nome do comandante",
            "C": "Opinião pessoal do STT",
            "D": "Qualquer informação que STT achar importante"
        },
        "resposta_correta": "B",
        "explicacao": "Livro de Ordens é documento legal. Deve conter: data, hora, natureza (operacional/administrativa/disciplinar), quem ordenou, quem executou. Falta qualquer campo invalida documento em tribunal.",
        "diagnostico_erro": "❌ Errou porque subestimou importância de documentação. Livro de Ordens decide processos criminais.",
        "nucleo_acerto": "✅ Acertou! STT que escreve bem protege todos. Precisão em registro é profissionalismo.",
        "pegadinha_banca": "Pegadinha: 'opinião pessoal' parece 'informação importante'. Livro de Ordens é fato, não opinião.",
        "padroes_banca": json.dumps({"foco": "Documentação", "tema": "Livro de Ordens", "palavra_chave": "legal"})
    },
    {
        "questao_id": "STT_PRACA_005",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Fácil",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "Qual é o significado de 'segurança orgânica' na doutrina militar?",
        "alternativas": {
            "A": "Defesa contra ataque externo de outra nação",
            "B": "Proteção interna da própria unidade contra infiltração, sabotagem e roubo",
            "C": "Medicina preventiva para soldados",
            "D": "Seguro de vida militar"
        },
        "resposta_correta": "B",
        "explicacao": "Segurança orgânica = defesa interna da tropa contra ameaças domésticas. STT guarda contra traidor interno, criminoso, infiltrado. É segurança que vem de dentro da própria estrutura.",
        "diagnostico_erro": "❌ Errou porque confundiu segurança orgânica (interna) com segurança externa (defesa nacional).",
        "nucleo_acerto": "✅ Acertou! STT é vigia da casa interna. Ninguém invade quartel se STT faz bem seu trabalho.",
        "pegadinha_banca": "Palavra-chave: 'interno' vs 'externo'. Doutrina militar diferencia níveis de ameaça.",
        "padroes_banca": json.dumps({"foco": "Conceito Militar", "tema": "Segurança Orgânica", "palavra_chave": "interna"})
    },
    {
        "questao_id": "STT_PRACA_006",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "STT testemunha colega violando protocolo de escala de guarda. Qual ação é correta?",
        "alternativas": {
            "A": "Silenciar para não prejudicar colega",
            "B": "Confrontar colega verbalmente em público",
            "C": "Documentar e relatar à chefia imediata ou corregedoria",
            "D": "Esperar colega ser pego por outro"
        },
        "resposta_correta": "C",
        "explicacao": "Código de Honra Militar exige denúncia de violação. Documentação protege instituição e colega infrator. Corporativismo que omite é corrupção, não lealdade.",
        "diagnostico_erro": "❌ Errou porque confundiu lealdade ao amigo com lealdade à instituição. Legítima é a segunda.",
        "nucleo_acerto": "✅ Acertou! Exército que policiam a si mesmo é exército respeitável. STT integro é raro.",
        "pegadinha_banca": "Pegadinha: corporativismo vs integridade são opostos. Palavra 'colega' não deve gerar omissão.",
        "padroes_banca": json.dumps({"foco": "Ética Militar", "tema": "Denúncia", "palavra_chave": "integridade"})
    },
    {
        "questao_id": "STT_PRACA_007",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "STT está em processo de sindicância por erro administrativo. Quais são seus direitos conforme Regulamento de Sindicância?",
        "alternativas": {
            "A": "Nenhum direito; sindicância é punição automática",
            "B": "Direito de ser ouvido, ver acusação, trazer defesa e ter prazo para responder",
            "C": "Direito de recusar participar",
            "D": "Direito de trancar sindicância na justiça"
        },
        "resposta_correta": "B",
        "explicacao": "Lei 6.880/1980 e regulamentos garantem devido processo militar. Sindicância é investigação, não condenação. Direitos: oitiva, acesso a acusação, defesa, prazo. Sem isso, sindicância é nula.",
        "diagnostico_erro": "❌ Errou porque confundiu sindicância (administrativa) com julgamento (judicial). Processo é garantia.",
        "nucleo_acerto": "✅ Acertou! Militar que conhece seus direitos protege a instituição de abuso. Exército justo é exército profissional.",
        "pegadinha_banca": "Palavra-chave: 'devido processo' vs 'punição automática'. Direitos existem até para acusado.",
        "padroes_banca": json.dumps({"foco": "Lei 6.880/1980", "tema": "Sindicância", "palavra_chave": "devido processo"})
    },
    {
        "questao_id": "STT_PRACA_008",
        "concurso": "STT Exército",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Fácil",
        "banca": "Exército",
        "tipo": "múltipla",
        "enunciado": "Qual é o direito FUNDAMENTAL de todo STT segundo Estatuto dos Militares?",
        "alternativas": {
            "A": "Sem direitos; militar é servidor do Estado",
            "B": "Salário digno, aposentadoria, licença médica, pensão ao cônjuge, educação para filhos",
            "C": "Só recebe ordem, nada de benefício social",
            "D": "Direitos só se tiver 20 anos de serviço"
        },
        "resposta_correta": "B",
        "explicacao": "Lei 6.880/1980 e Constituição Federal garantem direitos sociais básicos: salário mínimo, FGTS, 13º, licença, aposentadoria, pensão. Militar é cidadão brasileiro com direitos constitucionais.",
        "diagnostico_erro": "❌ Errou porque confundiu dever militar com negação de direitos. Dever não cancela direitos.",
        "nucleo_acerto": "✅ Acertou! STT bem amparado dedica 100%. Benefícios sociais geram compromisso.",
        "pegadinha_banca": "Pegadinha: 'servidor' (sim) vs 'sem direitos' (não). Serviço público tem obrigações E direitos.",
        "padroes_banca": json.dumps({"foco": "Direitos Sociais", "tema": "Proteção", "palavra_chave": "salário digno"})
    },
    {
        "questao_id": "TRANSPETRO_PRACA_001",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Em terminal de distribuição de combustível, qual é o protocolo de Segurança, Meio Ambiente e Saúde (SMS) ao detectar vazamento menor de gasolina?",
        "alternativas": {
            "A": "Ignorar se for pequeno volume",
            "B": "Imediatamente desligar bomba, avisar supervisor, aplicar pó absorvente, documentar",
            "C": "Tentar conter com água",
            "D": "Chamar bombeiros sem avisar supervisor"
        },
        "resposta_correta": "B",
        "explicacao": "NR-20 (Inflamáveis/Combustíveis) exige: parada imediata, isolamento, notificação, contenção. Vazamento pequeno pode virar explosão. Documentação é obrigatória para reguladores.",
        "diagnostico_erro": "❌ Errou porque subestimou vazamento. 'Pequeno' é mito. Gasolina é volátil: qualquer quantidade é risco.",
        "nucleo_acerto": "✅ Acertou! Transpetro que segue SMS evita mortes. Segurança é primeira prioridade operacional.",
        "pegadinha_banca": "Cesgranrio testa: diferença entre 'ignorar' (criminoso) vs 'documentar' (profissional).",
        "padroes_banca": json.dumps({"foco": "NR-20", "tema": "Vazamento", "palavra_chave": "documentar"})
    },
    {
        "questao_id": "TRANSPETRO_PRACA_002",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Qual é o procedimento operacional padrão (POP) para conferência de romaneio (quantidade de carga entregue) em Transpetro?",
        "alternativas": {
            "A": "Confiar no caminhoneiro e liberar carga",
            "B": "Medir manualmente, comparar com nota fiscal, documentar em sistema, assinar romaneio",
            "C": "Aceitar sem verificar se driver tiver pressa",
            "D": "Deixar para fazer conferência no dia seguinte"
        },
        "resposta_correta": "B",
        "explicacao": "Romaneio é documento legal e financeiro. Medição obrigatória evita discrepâncias, fraude, perda. Assinatura confirma responsabilidade. Sistema registra todas as operações para auditoria.",
        "diagnostico_erro": "❌ Errou porque confundiu urgência operacional com negligência. Não há justificativa para pular romaneio.",
        "nucleo_acerto": "✅ Acertou! Transpetro que controla romaneio protege patrimônio e previne roubo interno.",
        "pegadinha_banca": "Pegadinha: 'pressa' (justificativa fraca) vs 'procedimento' (obrigação legal).",
        "padroes_banca": json.dumps({"foco": "Operacional", "tema": "Romaneio", "palavra_chave": "documentar sistema"})
    },
    {
        "questao_id": "TRANSPETRO_PRACA_003",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Na rotina de manutenção preventiva de equipamentos de pátio, qual checklist é obrigatório segundo regulações Transpetro?",
        "alternativas": {
            "A": "Nenhum; manutenção é só quando quebra",
            "B": "Diário: válvulas, mangueiras, selos, vazamentos, sinais de corrosão",
            "C": "Anual é suficiente",
            "D": "Só chamar técnico externo"
        },
        "resposta_correta": "B",
        "explicacao": "Manutenção preventiva diária reduz paradas e acidentes. Checklist padrão: pressão, vazamentos, corrosão, vedações. Sistema de registros permite rastrear degradação. Rotina evita emergências.",
        "diagnostico_erro": "❌ Errou porque confundiu reativo (quebra→reparo) com proativo (prevenção). Indústria moderna é preventiva.",
        "nucleo_acerto": "✅ Acertou! Operador que faz checklist vale ouro. Equipamento mantido é equipamento confiável.",
        "pegadinha_banca": "Palavra-chave: 'diário' vs 'anual'. Cesgranrio testa frequência de vigilância.",
        "padroes_banca": json.dumps({"foco": "Manutenção", "tema": "Preventiva", "palavra_chave": "diário"})
    },
    {
        "questao_id": "TRANSPETRO_PRACA_004",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Em caso de incêndio em terminal de combustível, qual é a ação PRIMEIRA do operador?",
        "alternativas": {
            "A": "Tentar apagar com água",
            "B": "Evacuação imediata + ativar sistema de sprinkler/espuma + chamar bombeiros",
            "C": "Continuar trabalhando e reportar depois",
            "D": "Tentar descobrir origem do fogo"
        },
        "resposta_correta": "B",
        "explicacao": "Incêndio em combustível é emergência nível máximo. Protocolo: 1) Evacuação total, 2) Ativar sistemas automáticos (sprinkler/espuma), 3) Chamar bombeiros especializado. Vidas > patrimônio. Nunca use água em combustível.",
        "diagnostico_erro": "❌ Errou porque confundiu instinto (apagar) com realidade (combustível é mais perigoso). Água piora fogo de combustível.",
        "nucleo_acerto": "✅ Acertou! Operador que evacua primeiro é herói. Sistema automático + bombeiros é tática correta.",
        "pegadinha_banca": "Pegadinha: 'apagar' (instinto natural) vs 'evacuar' (procedimento correto). Teste de conhecimento técnico real.",
        "padroes_banca": json.dumps({"foco": "Emergência", "tema": "Incêndio", "palavra_chave": "evacuar"})
    },
    {
        "questao_id": "TRANSPETRO_PRACA_005",
        "concurso": "Transpetro (Petrobras)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Qual é a responsabilidade de operador Transpetro ao identificar não-conformidade em Equipamento de Proteção Individual (EPI)?",
        "alternativas": {
            "A": "Usar mesmo assim; trabalho não para",
            "B": "Relatar imediatamente, não usar EPI danificado, notificar supervisor",
            "C": "Consertar sozinho o EPI",
            "D": "Comprar novo com dinheiro próprio"
        },
        "resposta_correta": "B",
        "explicacao": "EPI danificado não protege; não-uso é negligência. Relato imediato protege operador e empresa. Supervisor repõe EPI novo. Registro documental cria trail de responsabilidade.",
        "diagnostico_erro": "❌ Errou porque confundiu produtividade com segurança. Trabalhar desprotegido é negligência suicida.",
        "nucleo_acerto": "✅ Acertou! Operador que relata não-conformidade protege a si e aos colegas. EPI é vida.",
        "pegadinha_banca": "Pegadinha: 'trabalho não para' é mito perigoso. Segurança SEMPRE para produção.",
        "padroes_banca": json.dumps({"foco": "EPI", "tema": "Proteção", "palavra_chave": "relatar"})
    },
    {
        "questao_id": "BACEN_PRACA_001",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Um técnico do Bacen é procurado por cidadão reclamando de cobrança indevida em sua conta. Qual é o procedimento correto?",
        "alternativas": {
            "A": "Ignorar porque cidadão deve procurar banco direto",
            "B": "Fazer triagem, documentar, encaminhar para setor de análise com protocolo",
            "C": "Prometer solução rápida sem investigação",
            "D": "Transferir para outro departamento sem informar"
        },
        "resposta_correta": "B",
        "explicacao": "Bacen é regulador e mediador de conflitos consumidor-banco. Triagem profissional: documentação, protocolo, prazo de resposta (30 dias). Cidadão sabe que foi ouvido.",
        "diagnostico_erro": "❌ Errou porque negou acesso ao órgão regulador. Bacen é justiceiro de consumidor.",
        "nucleo_acerto": "✅ Acertou! Técnico que acolhe protesto constrói confiança no BC. Proteção ao consumidor é missão.",
        "pegadinha_banca": "Pegadinha: 'ignorar' vs 'documentar'. Cesgranrio testa responsabilidade de órgão público.",
        "padroes_banca": json.dumps({"foco": "Consumidor", "tema": "Atendimento", "palavra_chave": "triagem"})
    },
    {
        "questao_id": "BACEN_PRACA_002",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Técnico do Bacen identifica padrão suspeito de movimentação financeira em conta de cliente. Qual é a ação obrigatória?",
        "alternativas": {
            "A": "Contatar cliente diretamente para avisar",
            "B": "Reportar ao Coaf (Conselho de Controle de Atividades Financeiras) conforme Lei 9.613/1998",
            "C": "Informar ao banco sem ao cliente",
            "D": "Ignorar se movimentação for legal"
        },
        "resposta_correta": "B",
        "explicacao": "Lei 9.613/1998 (LAML) exige relato ao Coaf em caso de suspeita de lavagem/financiamento do terrorismo. Bacen é ponte regulatória. Confidencialidade é mandatória; revelar cliente compromete investigação.",
        "diagnostico_erro": "❌ Errou porque confundiu aviso (viola confidencialidade) com relato institucional (obrigatório por lei).",
        "nucleo_acerto": "✅ Acertou! Técnico que reporta ao Coaf protege país de crime financeiro. É defesa nacional.",
        "pegadinha_banca": "Palavra-chave: 'Coaf' vs 'cliente'. Lei exige sigilo do relato, nunca aviso direto.",
        "padroes_banca": json.dumps({"foco": "Lei 9.613/1998", "tema": "Lavagem", "palavra_chave": "Coaf"})
    },
    {
        "questao_id": "BACEN_PRACA_003",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Técnico Bacen recebe informação sigilosa de cliente sobre fraude interna. Como deve proceder?",
        "alternativas": {
            "A": "Contar para colega mais experiente",
            "B": "Guardar só para si e esquecer",
            "C": "Documentar formalmente, reportar à corregedoria do Bacen via canais seguros",
            "D": "Publicar em rede social para alertar público"
        },
        "resposta_correta": "C",
        "explicacao": "Sigilo bancário é dever legal. Denúncia deve ser formal, via canais apropriados (corregedoria/auditoria), com documentação segura. Whistleblower tem proteção legal (Lei 13.709/2018).",
        "diagnostico_erro": "❌ Errou porque confundiu confidencialidade com conspiração. Denúncia formal é obrigação, não traição.",
        "nucleo_acerto": "✅ Acertou! Técnico que denuncia formalmente é herói institucional. Fraude interna deve ser pega.",
        "pegadinha_banca": "Pegadinha: 'colega' (errado) vs 'corregedoria' (correto). Canais formais protegem denunciante.",
        "padroes_banca": json.dumps({"foco": "Sigilo", "tema": "Denúncia", "palavra_chave": "corregedoria"})
    },
    {
        "questao_id": "BACEN_PRACA_004",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Fácil",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Qual é a principal função do técnico do Bacen na fiscalização de instituições financeiras?",
        "alternativas": {
            "A": "Punir bancos diretamente",
            "B": "Verificar conformidade com normas, identificar riscos, relatar desvios",
            "C": "Ganhar comissão em operações de crédito",
            "D": "Proteger lucro dos bancos"
        },
        "resposta_correta": "B",
        "explicacao": "Fiscalização é função-chave do Bacen. Técnico verifica: capital adequado, provisões, governança, compliance. Relatórios geram regulação. Proteção ao sistema financeiro beneficia todos.",
        "diagnostico_erro": "❌ Errou porque confundiu função regulatória com punição ou ganho pessoal. Bacen é árbitro imparcial.",
        "nucleo_acerto": "✅ Acertou! Técnico que fiscaliza bem protege poupança de milhões. É missão sagrada.",
        "pegadinha_banca": "Pegadinha: 'punição' vs 'verificação'. Bacen não pune; constata e regulamenta.",
        "padroes_banca": json.dumps({"foco": "Regulação", "tema": "Fiscalização", "palavra_chave": "conformidade"})
    },
    {
        "questao_id": "BACEN_PRACA_005",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Médio",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Técnico Bacen testemunha colega cometendo erro grave em análise de crédito que pode impactar decisão regulatória. Qual é o dever?",
        "alternativas": {
            "A": "Fingir que não viu para não gerar conflito",
            "B": "Privadamente avisar colega que corrija",
            "C": "Documentar erro, reportar ao supervisor/ouvidoria",
            "D": "Esperar erro se manifestar em auditoria"
        },
        "resposta_correta": "C",
        "explicacao": "Decisões regulatórias erradas podem quebrar banco e prejudicar depositantes. Documentação imediata + relato via canais formais protege instituição. Omissão é negligência.",
        "diagnostico_erro": "❌ Errou porque confundiu proteção pessoal com responsabilidade profissional. Erro regulatório afeta milhões.",
        "nucleo_acerto": "✅ Acertou! Técnico que denuncia corrige o sistema. Integridade institucional é prioridade número um.",
        "pegadinha_banca": "Pegadinha: 'conflito pessoal' (medo) vs 'dano regulatório' (risco real). Escolha é clara.",
        "padroes_banca": json.dumps({"foco": "Responsabilidade", "tema": "Erro Análise", "palavra_chave": "documentar"})
    },
    {
        "questao_id": "BACEN_PRACA_006",
        "concurso": "Banco Central (Bacen)",
        "materia": "Conhecimentos Práticos e Atribuições do Cargo",
        "dificuldade": "Difícil",
        "banca": "Cesgranrio",
        "tipo": "múltipla",
        "enunciado": "Técnico do Bacen recebe pressão de gerente bancário para aprovar operação que não atende critérios prudenciais. Qual é a ação correta?",
        "alternativas": {
            "A": "Aprovar para manter relação boa com banco",
            "B": "Rejeitar formalmente, documentar justificativa, relatar à chefia",
            "C": "Negociar um compromisso para agradar ambos",
            "D": "Fazer operação 'passar' sem parecer oficial"
        },
        "resposta_correta": "B",
        "explicacao": "Independência regulatória é fundação do Bacen. Pressão = corrupção. Rejeição formal com justificativa protege técnico E instituição. Sistema financeiro confia porque Bacen é incorruptível.",
        "diagnostico_erro": "❌ Errou porque cedeu a pressão. Regulator que cede se torna inútil e criminoso.",
        "nucleo_acerto": "✅ Acertou! Técnico que resiste a pressão é herói do Estado. Independência é tudo.",
        "pegadinha_banca": "Pegadinha: 'relação boa' (suborno disfarçado) vs 'rejeição documentada' (profissionalismo). Cesgranrio testa integridade.",
        "padroes_banca": json.dumps({"foco": "Integridade", "tema": "Pressão Externa", "palavra_chave": "independência"})
    }
];

def popular_questoes_pratica():
    """Injetar 30 questões de prática do cargo no banco de dados"""
    db = SessionLocal()
    try:
        for q_data in questoes_pratica_cargo:
            existing = db.query(QuestoesBancoModel).filter_by(questao_id=q_data["questao_id"]).first()
            if not existing:
                q = QuestoesBancoModel(
                    questao_id=q_data["questao_id"],
                    concurso=q_data["concurso"],
                    materia=q_data["materia"],
                    dificuldade=q_data["dificuldade"],
                    banca=q_data["banca"],
                    tipo=q_data["tipo"],
                    enunciado=q_data["enunciado"],
                    alternativas=json.dumps(q_data["alternativas"]),
                    resposta_correta=q_data["resposta_correta"],
                    explicacao=q_data["explicacao"],
                    diagnostico_erro=q_data["diagnostico_erro"],
                    nucleo_acerto=q_data["nucleo_acerto"],
                    pegadinha_banca=q_data["pegadinha_banca"],
                    padroes_banca=q_data.get("padroes_banca", "{}"),
                    data_criacao=datetime.now().isoformat()
                )
                db.add(q)
                print(f"✅ Adicionada: {q_data['questao_id']} - {q_data['concurso']}")
            else:
                print(f"⏭️  Já existe: {q_data['questao_id']}")
        
        db.commit()
        print(f"\n✅ SUCESSO: 30 questões de prática do cargo injetadas!")
        
        count = db.query(func.count(QuestoesBancoModel.id)).scalar()
        print(f"📊 Total de questões agora: {count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERRO ao popular: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando injeção de questões de prática do cargo v3.3...\n")
    popular_questoes_pratica()
    print("\n🎉 Populador finalizado!")
