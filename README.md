# **FinFlow AI**

**Uma ferramenta inteligente de triagem e resposta de e-mails para o setor financeiro, potencializada por IA Generativa.**

## **Sumário**

* [Sobre o Projeto](#sobre-o-projeto)  
* [Principais Funcionalidades](#principais-funcionalidades)  
* [Como Funciona](https://www.google.com/search?q=%23-como-funciona)  
* [Diagrama da Arquitetura](#como-funciona)  
* [Tech Stack](#tech-stack)  
* [Instalação e Execução](#instalação-e-execução)  
* [Estrutura do Projeto](#estrutura-do-projeto)

## **Sobre o Projeto**

O **FinFlow** foi desenvolvido para enfrentar um desafio crítico em equipes de finanças e atendimento: o alto volume de e-mails que exigem triagem manual. A ferramenta automatiza esse processo usando um modelo de linguagem avançado (LLM) para classificar e-mails e sugerir respostas, liberando tempo da equipe para focar em tarefas de maior valor.

O sistema não apenas classifica um e-mail como "Produtivo" ou "Improdutivo", mas também gera uma resposta profissional e contextualizada, pronta para ser usada. Além disso, fornece um dashboard gerencial com métricas sobre o volume e a natureza das solicitações recebidas.

## **Principais Funcionalidades**

* **Triagem por Múltiplas Entradas:** Aceita e-mails colados diretamente em texto ou via upload de arquivos **.txt** e **.pdf**.  
* **Classificação e Resposta com IA:** Utiliza um prompt único e otimizado para o **Google Gemini** que, em uma só chamada, classifica o e-mail e gera uma sugestão de resposta humanizada, seguindo diretrizes de tom corporativo.  
* **Dashboard Gerencial:** Uma página de dashboard que exibe métricas em tempo real sobre os e-mails processados, incluindo:  
  * Um gráfico de pizza com a **distribuição percentual** de e-mails "Produtivos" vs. "Improdutivos".  
  * Um gráfico de barras mostrando o **volume de e-mails processados** nos últimos 7 dias.  
* **Interface Robusta e Segura:**  
  * **Validação no Frontend:** Limita o tamanho de arquivos (10MB) e a contagem de caracteres (15.000) para prevenir abusos e garantir performance.  
  * **Validação no Backend:** Impõe um limite de 10MB (MAX\_CONTENT\_LENGTH) no Flask para proteger o servidor.  
  * **Padrão Post/Redirect/Get (PRG):** Evita o reenvio de formulários ao recarregar a página, proporcionando uma experiência de usuário fluida.  
* **Histórico Persistente:** Cada classificação é salva automaticamente em um banco de dados **SQLite**, que alimenta o dashboard.

## **Como Funciona**

O fluxo de dados da aplicação é simples e eficiente:

1. **Entrada:** O usuário insere um texto ou faz upload de um arquivo na página principal (index.html).  
2. **Requisição:** O formulário é enviado via POST para o servidor **Flask** (app.py).  
3. **Processamento:**  
   * O Flask recebe os dados. Se for um arquivo, o pypdf extrai o texto.  
   * O texto limpo é inserido em um **prompt único** otimizado.  
   * O servidor faz **uma única chamada** à API do Google Gemini.  
   * A API retorna uma string formatada (ex: PRODUTIVO---Prezado...).  
4. **Armazenamento:**  
   * O Flask divide a string. A categoria (PRODUTIVO) é enviada para o database.py e salva no banco historico.db.  
   * O resultado completo (categoria \+ sugestão) é salvo na session do usuário.  
5. **Redirecionamento (PRG):** O servidor redireciona o usuário de volta para a página principal.  
6. **Exibição:**  
   * A página (index.html) é recarregada via GET.  
   * O Flask lê o resultado da session e o injeta no HTML com o Jinja2, mostrando o card de sucesso.  
   * Como a session é limpa após a leitura (session.pop), recarregar a página (F5) não mostra o resultado novamente.  
7. **Dashboard:**  
   * Ao acessar /dashboard, o Flask chama get\_dados\_dashboard().  
   * O database.py consulta o historico.db e retorna os dados agregados.  
   * Os dados são passados para o dashboard.html como um JSON seguro (tojson | safe).  
   * O dashboard.js lê o JSON e desenha os gráficos com **Chart.js**.

## **Diagrama da Arquitetura**

*(Este é um espaço reservado para você adicionar seu diagrama de blocos. Você pode criar um no draw.io (agora diagrams.net) ou similar e salvar a imagem na pasta frontend/img/)*

\[Insira seu diagrama de arquitetura aqui. Ex: (Usuário) \-\> (Flask) \-\> (Gemini AI) / (SQLite)\]

## **Tech Stack**

| Categoria | Tecnologia | Propósito |
| :---- | :---- | :---- |
| **Backend** | **Python** | Linguagem principal da aplicação. |
|  | **Flask** | Micro-framework web para o servidor e rotas. |
|  | **Google Gemini** | Modelo de IA Generativa para classificação e resposta. |
|  | **SQLite3** | Banco de dados leve (baseado em arquivo) para persistência do histórico. |
|  | **pypdf** | Biblioteca para extração de texto de arquivos .pdf. |
|  | **python-dotenv** | Gerenciamento de chaves de API e segredos em um arquivo .env. |
| **Frontend** | **HTML5** | Estrutura semântica das páginas. |
|  | **CSS3** | Estilização profissional, layout (Flexbox/Grid) e responsividade. |
|  | **JavaScript (ES6+)** | Interatividade da UI (validação de formulário, feedback de upload, lógica de cópia). |
| **Visualização** | **Chart.js** | Biblioteca para renderização dos gráficos do dashboard. |
|  | **chartjs-plugin-datalabels** | Plugin para exibir porcentagens e valores dentro dos gráficos. |

## **Instalação e Execução**

Siga os passos abaixo para executar o projeto em seu ambiente local.

### **1. Pré-requisitos**

* [Python 3.9+](https://www.python.org/downloads/)  
* [Git](https://www.google.com/search?q=https://git-scm.com/downloads)

### **2. Clonar o Repositório**

```bash
   git clone https://github.com/pedrosmithhh/FinFlow.git
```
### **3. Configurar Ambiente Virtual**

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

# Criar um ambiente virtual

```
   python \-m venv venv
```

### **4. Instalar Dependências**

Instale todas as bibliotecas Python necessárias listadas no requirements.txt.

```
   pip install -r requirements.txt
```

### **5. Configurar Variáveis de Ambiente**

Crie um arquivo chamado .env dentro da pasta backend/. Este arquivo armazenará suas chaves secretas e não deve ser enviado ao GitHub.

Adicione o seguinte conteúdo ao arquivo backend/.env:

#### Obtenha sua chave de API no Google AI Studio ([https://aistudio.google.com/](https://aistudio.google.com/))

```env
   API_KEY=SUA_CHAVE_SECRETA_DO_GEMINI_AQUI
```

###### Use qualquer string longa e aleatória para a segurança da sessão Flask  

```env
FLASK_SECRET_KEY=SUA_CHAVE_SECRETA_ALEATORIA_DO_FLASK
```

### **6. Executar a Aplicação**

Navegue até a pasta do backend e inicie o servidor Flask.

```bash
cd backend  
python app.py
```

Abra seu navegador e acesse [http://127.0.0.1:5000](https://www.google.com/search?q=http://127.0.0.1:5000) para ver a aplicação em funcionamento.

## **Estrutura do Projeto**

A estrutura de pastas é organizada para separar claramente o backend (lógica do servidor) do frontend (arquivos do cliente).

FinFlow/  
│  
├── backend/  
│   ├── app.py             # Arquivo principal do Flask (rotas, lógica da IA)  
│   ├── database.py        # Lógica de conexão e queries com o SQLite  
│   ├── .env               # (Seu arquivo local de segredos)  
│  
├── data/  
│   └── historico.db       # Banco de dados SQLite  
│  
├── frontend/  
│   ├── dashboard.css      # Estilos do dashboard  
│   ├── dashboard.html     # Página do dashboard  
│   ├── dashboard.js       # JS dos gráficos (Chart.js)  
│   ├── img/  
│   │   └── logo.png       # Logotipo e outros assets  
│   ├── index.html         # Página principal (classificador)  
│   ├── script.js          # JS da página principal  
│   └── style.css          # Estilos globais  
│  
├── .gitignore             # Arquivos ignorados pelo Git  
├── requirements.txt       # Dependências do Python  
└── README.md              # Este arquivo  
