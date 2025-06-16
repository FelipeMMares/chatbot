from flask import Flask, request, jsonify
from ollama import Client
import time
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Configuração do Ollama
client = Client(host='http://localhost:11434')

# Base de conhecimento do FAQ (otimizada para TinyLlama)
FAQ = {
    "1": "Cursos com vagas:\n- Bacharelado em Sistemas de Informação: 9 vagas\n- Educação Física: 27 vagas\n- Letras Libras: 33 vagas",
    "2": "Edital disponível em:\nhttps://www.ifbaiano.edu.br/unidades/itapetinga/",
    "3": "Quais são os requisitos para participar do processo seletivo? \nO processo seletivo é destinado a candidatos(as) que concluíram o Ensino Médio. A comprovação de conclusão será exigida no ato da matrícula.",
    "4":"É preciso ter feito o ENEM para participar do processo de vagas remanescentes?\nNão. Você só precisa ter concluído o Ensino Médio e anexar seu histórico escolar durante o ato de inscrição.",
    "5": "Como a nota final do processo seletivo é calculada?\nPara alunos do Ensino Médio regular, a NOTA FINAL é a média aritmética das notas de Língua Portuguesa e Matemática da última série do Ensino Médio.\nPara candidatos que obtiveram certificação do Ensino Médio via ENCCEJA, Comissões Permanentes de Avaliação (CPA) ou exames supletivos, a NOTA FINAL é a média das notas das áreas de Linguagens e Matemática.\nA NOTA FINAL será divulgada em uma escala de 0,0 a 100,0 pontos.\nSe as notas no histórico estiverem em escala de 0,0 a 10,0, elas serão convertidas multiplicando-se por 10\nO sistema de inscrição aceitará apenas uma casa decimal após a vírgula. Se sua nota tiver mais de uma casa decimal, informe apenas a primeira, sem arredondamentos.",
    "6": "O que acontece se houver empate na pontuação final?\nEm caso de empate, os critérios de desempate, por ordem de prioridade, são: maior nota em Língua Portuguesa ou Linguagens, e maior idade (considerando ano, mês e dia, com referência à data de publicação do Edital). Se o empate persistir, será considerada a ordem de inscrição.",
    "7": "Quando e como posso me inscrever?\nO período de inscrição é de 16/06/2025 a 18/07/2025.\nAs inscrições serão realizadas de forma on-line, preenchendo e submetendo os documentos em https://sgc.ifbaiano.edu.br/.",
    "8": "Quais documentos preciso anexar para a inscrição?\nVocê deverá anexar, em formato PDF, o histórico escolar do ensino médio com certificado de conclusão.\nSe você obteve a conclusão do Ensino Médio via ENCCEJA, CPA ou exames supletivos, deve anexar o certificado de conclusão correspondente.\nCandidatos que optarem por vagas V (Pessoas com Deficiência) devem anexar laudo médico original, em PDF, emitido nos últimos 12 meses, atestando o tipo, grau ou nível de deficiência, com referência ao CID.\nCandidatos que optarem por vagas LB_PPI, LB_Q, LB_PCD, LB_EP, LI_PPI, LI_Q, LI_PCD ou LI_EP, devem seguir as instruções específicas para cada caso, que incluem autodeclaração e/ou comprovação de renda, e laudo médico para PCD.",
    "9": "Posso me inscrever para mais de um curso?\nNão, é proibida a inscrição para mais de um curso. Se você fizer mais de uma inscrição, apenas a última, que cumpra todas as regras do edital, será validada.",
    "10": "O que é o procedimento de heteroidentificação étnico-racial?\nEste procedimento é para candidatos que se inscreverem para vagas de ações afirmativas. O objetivo é confirmar a autodeclaração de candidatos(as) autodeclarados(as) pretos e pardos, com base unicamente em características fenotípicas.",
    "11": "Quando será o resultado preliminar do processo seletivo?\nO resultado preliminar do processo seletivo será divulgado em 10/09/2025.",
    "12": "Posso entrar com recurso contra o resultado preliminar?\nSim, o período de recurso contra o resultado preliminar do processo seletivo é 11 e 12/09/2025.",
    "13": "Quando será o resultado final e a convocação para matrícula?\nO Resultado Final do Processo Seletivo e a Convocação para a Matrícula (1ª chamada) serão em 17/09/2025.",
    "14": "O que acontece se eu não comparecer à primeira semana de aula após a convocação?\nSerá considerado abandono do curso e você perderá automaticamente o direito à vaga.",
    "15": "Os cursos são presenciais ou a distância?\nOs três cursos com vagas remanescentes ofertadas no processo seletivo são presenciais.",
    "16": "Qual o horário das aulas?\nBacharelado em Sistemas de Informação: de segunda a sexta, das 7:30 às 17:30 h; aos sábados, das 7:30 às 11:50 h.\nLetras: Libras: de segunda à sexta, das 18:00 às 22: 40 h; aos sábados, das 7:30 às 11:50 h.\nEducação Física: de segunda à sexta, das 17:50 h às 22:50 h; aos sábados, das 7:30 às 11: 50 h.",
    # Adicione todas as outras perguntas no mesmo formato
    "17": "Dúvidas? Email:\nprosel@itapetinga.ifbaiano.edu.br"
}

def gerar_menu():
    """Menu otimizado para modelos leves"""
    menu = "🔍 *IF Baiano - Vagas Remanescentes* 🔍\n"
    for num, resposta in FAQ.items():
        menu += f"\n{num}. {resposta.splitlines()[0][:50]}..."  # Mostra apenas início da pergunta
    menu += "\n\n📝 Digite o *número* da pergunta (ex: 1)"
    return menu

def responder_tinyllama(prompt):
    """Obtém resposta do TinyLlama com configurações otimizadas"""
    try:
        response = client.generate(
            model="tinyllama",
            prompt=f"[INST] Seja conciso. Responda em até 3 linhas. {prompt} [/INST]",
            options={
                "temperature": 0.3,  # Reduz criatividade para respostas mais objetivas
                "num_ctx": 512       # Metade do contexto padrão para economizar memória
            }
        )
        return response['response']
    except Exception as e:
        return f"⚠️ Erro ao processar: {str(e)}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    mensagem = request.values.get('Body', '').strip()
    
    # Respostas pré-definidas
    if mensagem.lower() in ['menu', 'oi', 'ola']:
        resposta = gerar_menu()
    elif mensagem in FAQ:
        resposta = f"*Resposta:*\n{FAQ[mensagem]}\n\nDigite outro número ou *menu*"
    else:
        # Usa o TinyLlama para outras perguntas
        resposta = responder_tinyllama(mensagem)
    
    # Formata para WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(resposta)
    return str(twilio_resp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
