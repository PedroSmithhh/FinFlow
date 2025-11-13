import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf

def limpar_texto(texto):
    return " ".join(texto.split())

def consultar_ia(prompt):
    response = model.generate_content(prompt)
    return response.text

def ler_pdf(file_storage):
    texto = ""
    try:
        reader = pypdf.PdfReader(file_storage)
        for page in reader.pages:
            texto += page.extract_text() or ""
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
    return texto

load_dotenv()

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_frontend = os.path.join(diretorio_atual, '../frontend')

app = Flask(__name__, template_folder=caminho_frontend, static_folder=caminho_frontend)

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None

    if request.method == 'POST':
        email_usuario = ""
        arquivo = None
        texto_input = None

        try:
            arquivo = request.files.get("email_file")
            texto_input = request.form.get('email_text')

            if arquivo and arquivo.filename != '':
                filename = arquivo.filename.lower()

                if filename.endswith('.pdf'):
                    email_usuario = ler_pdf(arquivo)
                elif filename.endswith('.txt'):
                    email_usuario = arquivo.read().decode('utf-8')

            elif texto_input.strip():
                email_usuario = texto_input

            else:
                return render_template('index.html', resultado={"erro": "Por favor, insira um texto ou anexe um arquivo."})

            if not email_usuario.strip():
                return render_template('index.html', resultado={"erro": "Nenhum contéudo fornecido"})
            
            email_limpo = " ".join(email_usuario.split())

            prompt_classificacao = f"""
            # FUNÇÃO
            Você é um sistema de triagem de emails em uma grande empresa do setor financeiro. Sua única função é classificar se um email precisa de atendimento ou não.

            # DEFINIÇÕES DE CLASSE
            1. PRODUTIVO
            - Definição: Emails que exigem uma ação, resposta, suporte técnico ou esclarecimento de dúvidas.
            - Critério: Se a equipe precisa parar para responder ou resolver algo, é PRODUTIVO.

            2. IMPRODUTIVO
            - Definição: Emails que não necessitam de ação imediata.
            - Critério: Agradecimentos ("Obrigado", "Valeu"), confirmações curtas ("Ok, recebido"), mensagens automáticas ou felicitações.

            # REGRA DE RESPOSTA OBRIGATÓRIA
            - Retorne APENAS uma única palavra como resposta.
            - As únicas respostas permitidas são: "PRODUTIVO" ou "IMPRODUTIVO".
            - Não coloque pontuação, não explique o motivo e não adicione nenhum outro texto.
            
            # EMAIL PARA ANÁLISE: {email_limpo}
            """

            categoria = consultar_ia(prompt_classificacao).strip()
            
            instrucao_resposta = f"""
            # PAPEL
            Você é um Especialista em Comunicação Corporativa em uma grande empresa do setor financeiro. Sua especialidade é redigir emails que são profissionais, mas que soam genuinamente humanos, empáticos e diretos.

            # TAREFA
            Sua tarefa é ler o email de entrada fornecido abaixo e redigir uma resposta completa e pronta para ser enviada.

            # DIRETRIZES DE ESTILO E TOM
            1.  Humanizado: Evite linguagem excessivamente robótica, formalismos arcaicos (como "Vimos por meio desta") ou frases genéricas de IA. Use um tom conversacional, porém respeitoso.
            2.  Contextual: A resposta deve demonstrar claramente que você leu e compreendeu os pontos específicos levantados no email original.
            3.  Profissional: Mantenha a polidez, clareza e objetividade.
            4.  Adaptabilidade: Se o email recebido for informal, responda de forma levemente informal (mas profissional). Se for formal, mantenha a formalidade.

            # RESTRIÇÕES RÍGIDAS (IMPORTANTE)
            1.  NUNCA inclua uma linha de assunto (Subject: ...). Comece diretamente pela saudação.
            2.  NUNCA inclua texto de preâmbulo ou conversa com o usuário (ex: "Aqui está a resposta:", "Claro, segue o email:"). Gere APENAS o corpo do email.
            3.  Espaços Reservados: Se precisar de uma informação que não possui (como uma data ou nome), use colchetes assim: [INSERIR DATA].
            4.  **Assinatura: Termine com "Atenciosamente," ou similar, e deixe o espaço para o nome do remetente como [Seu Nome].
            """

            prompt_resposta = f"""
            {instrucao_resposta}
            
            E-mail: "{email_limpo}"
            """
            resposta = consultar_ia(prompt_resposta)

            resultado = {
                "original": email_usuario,
                "categoria": categoria,
                "sugestao": resposta
            }

        except Exception as e:
                print(f"Erro interno: {e}")
                return render_template('index.html', resultado={"erro": "Ocorreu um erro interno ao processar sua solicitação."})
        
    return render_template('index.html', resultado=resultado)

    
if __name__ == '__main__':
    app.run(debug=True)
