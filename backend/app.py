import os
from flask import Flask, render_template, request, session, redirect, url_for
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf
from database import init_db, salvar_historico, get_dados_dashboard

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

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

app.secret_key = os.getenv("FLASK_SECRET_KEY")

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = session.pop('resultado', None)

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

            prompt = f"""
            # TAREFA GERAL
            Você é um assistente de IA avançado para uma empresa do setor financeiro.
            Sua tarefa é ler o email abaixo e realizar DUAS ações em sequência:
            1.  Primeiro, classificar o email (Ação 1).
            2.  Segundo, redigir uma sugestão de resposta (Ação 2).

            # EMAIL PARA ANÁLISE:
            "{email_limpo}"

            # FORMATO DE SAÍDA OBRIGATÓRIO (ESSENCIAL)
            1.  Na LINHA 1: APENAS a classificação (uma única palavra: "PRODUTIVO" ou "IMPRODUTIVO").
            2.  Na LINHA 2: APENAS o separador "---".
            3.  Da LINHA 3 em diante: O corpo da resposta sugerida.

            ---
            # AÇÃO 1: INSTRUÇÕES DE CLASSIFICAÇÃO
            -   **Papel:** Sistema de triagem de emails.
            -   **Definição PRODUTIVO:** Emails que exigem uma ação, resposta, suporte técnico ou esclarecimento de dúvidas. (Critério: Se a equipe precisa parar para responder ou resolver algo).
            -   **Definição IMPRODUTIVO:** Emails que não necessitam de ação imediata. (Critério: Agradecimentos, confirmações curtas, mensagens automáticas, felicitações).
            -   **Resultado da Ação 1:** A palavra única ("PRODUTIVO" ou "IMPRODUTIVO") que você colocará na Linha 1.

            ---
            # AÇÃO 2: INSTRUÇÕES DE SUGESTÃO DE RESPOSTA
            -   **Papel:** Especialista em Comunicação Corporativa.
            -   **Estilo e Tom:**
                1.  Humanizado: Evite linguagem robótica ou formalismos arcaicos. Tom conversacional, porém respeitoso.
                2.  Contextual: A resposta deve demonstrar que o email original foi lido e compreendido.
                3.  Profissional: Mantenha a polidez, clareza e objetividade.
                4.  Adaptabilidade: Adapte o tom (formal/informal) ao email recebido, mantendo o profissionalismo.
            -   **Restrições Rígidas:**
                1.  NUNCA inclua linha de assunto (Subject: ...).
                2.  Comece DIRETAMENTE pela saudação (ex: "Prezado...").
                3.  NUNCA inclua preâmbulo (ex: "Aqui está a resposta:").
                4.  Use colchetes [ASSIM] para informações que você não possui (ex: [INSERIR DATA]).
                5.  Termine com "Atenciosamente," (ou similar) e "[Seu Nome]".
            -   **Resultado da Ação 2:** O corpo do email que você colocará a partir da Linha 3.
            """
            resposta = consultar_ia(prompt).strip()

            if "---" not in resposta:
                categoria = "PRODUTIVO"
                resposta = "A IA não conseguiu gerar uma resposta formatada corretamente."
            else:
                partes = resposta.split("---", 1)
                categoria = partes[0].strip()
                resposta = partes[1].strip()

            # Salva o histórico independentemente do formato da resposta
            try:
                salvar_historico(categoria)
            except Exception as e:
                print(f"Erro ao salvar histórico: {e}")

            resultado_final = {
                "original": email_usuario[:500] + "..." if len(email_usuario) > 500 else email_usuario,
                "categoria": categoria,
                "sugestao": resposta
            }

            # PRG
            session['resultado'] = resultado_final
            return redirect(url_for('index'))

        except Exception as e:
            print(f"Erro interno: {e}")
            session['resultado'] = {"erro": f"Ocorreu um erro interno: {str(e)}"}
            return redirect(url_for('index'))

    return render_template('index.html', resultado=resultado)

@app.route('/dashboard')
def dashboard():
    # 1. Busca os dados no banco
    dados_db = get_dados_dashboard()
    
    # 2. Envia os dados para o novo template
    return render_template('dashboard.html', dados_dashboard=dados_db)


init_db()

    
if __name__ == '__main__':
    app.run(debug=True)
