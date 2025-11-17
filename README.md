# **FinFlow AI**

**Uma ferramenta inteligente de triagem e resposta de e-mails, potencializada por IA Generativa e com deploy automatizado no Google Cloud.**

## **📖 Índice**

* [Sobre o Projeto](#sobre-o-projeto)  
* [Principais Funcionalidades](#principais-funcionalidades)  
* [Como Funciona](#️como-funciona)  
* [Tech Stack](#tech-stack)  
* [Rodando Localmente](#rodando-localmente)  
* [Deploy em Produção (GCP)](#️deploy-em-produção-gcp)  

## **Sobre o Projeto**

O **FinFlow** foi desenvolvido para enfrentar um desafio crítico em equipes de finanças e atendimento: o alto volume de e-mails que exigem triagem manual. A ferramenta automatiza esse processo usando um modelo de linguagem avançado (LLM) para classificar e-mails e sugerir respostas, liberando tempo da equipe para focar em tarefas de maior valor.

O sistema não apenas classifica um e-mail, mas também gera uma resposta profissional e contextualizada. O projeto é "production-ready", utilizando um banco de dados PostgreSQL (via Supabase) e um pipeline de deploy (CI/CD) totalmente automatizado no Google Cloud Run.

## **Principais Funcionalidades**

* **Triagem por Múltiplas Entradas:** Aceita e-mails colados diretamente em texto ou via upload de arquivos **.txt** e **.pdf**.  
* **Classificação e Resposta com IA:** Utiliza um prompt único e otimizado para o **Google Gemini** que, em uma só chamada, classifica o e-mail e gera uma sugestão de resposta humanizada.  
* **Dashboard Gerencial:** Uma página de dashboard que lê o banco de dados e exibe métricas em tempo real sobre os e-mails processados, incluindo distribuição percentual e volume diário .  
* **Deploy Automatizado (CI/CD):** Cada git push para a branch main aciona automaticamente o **Google Cloud Build**, que "containeriza" a aplicação com **Docker** e a implanta no **Google Cloud Run** sem qualquer intervenção manual.  
* **Interface Robusta e Segura:**  
  * **Validação no Frontend:** Limita o tamanho de arquivos (10MB) e a contagem de caracteres (15.000).  
  * **Padrão Post/Redirect/Get (PRG):** Evita o reenvio de formulários ao recarregar a página.  
  * **Gestão de Segredos:** Todas as chaves (API, Banco de Dados, Flask) são gerenciadas de forma segura no **Google Secret Manager** e injetadas no ambiente de produção.  
* **Tema Escuro:** Possui um alternador de tema (claro/escuro) com persistência no localStorage do navegador.

## **Como Funciona**

1. **Entrada:** O usuário insere um texto ou faz upload de um arquivo no index.html.  
2. **Requisição:** O formulário é enviado via POST para o servidor **Flask**, que está rodando no Google Cloud Run.  
3. **Processamento:**  
   * O Flask (app.py) recebe os dados, lê o PDF (se houver) e chama a API do Google Gemini com um prompt otimizado.  
   * A API retorna uma string formatada (ex: PRODUTIVO---Prezado...).  
4. **Armazenamento:**  
   * O Flask divide a string. A categoria (PRODUTIVO) é enviada para o database.py.  
   * O database.py se conecta ao banco **PostgreSQL** (hospedado no Supabase) e insere o novo registro.  
   * O resultado completo (categoria \+ sugestão) é salvo na session do usuário.  
5. **Redirecionamento (PRG):** O servidor redireciona o usuário de volta para a página principal.  
6. **Exibição:** A página é recarregada via GET, o Flask lê o resultado da session e o injeta no HTML com o Jinja2.  
7. **Dashboard:**  
   * O database.py faz queries no **PostgreSQL** para agregar os dados.  
   * Os dados são passados para o dashboard.js, que desenha os gráficos com **Chart.js**.

## **Tech Stack**

| Categoria | Tecnologia | Propósito |
| :---- | :---- | :---- |
| **Backend** | **Python** | Linguagem principal da aplicação. |
|  | **Flask** | Micro-framework web para o servidor e rotas. |
|  | **Gunicorn** | Servidor WSGI de produção para o Flask. |
| **Frontend** | **HTML5 / CSS3 / JS (ES6+)** | Estrutura, estilo e interatividade da UI. |
| **IA** | **Google Gemini** | Modelo de IA Generativa para classificação e resposta. |
| **Banco de Dados** | **PostgreSQL (Supabase)** | Banco de dados relacional em nuvem, gratuito e persistente. |
|  | **psycopg2-binary** | Driver Python para conectar ao PostgreSQL. |
| **DevOps (GCP)** | **Google Cloud Run** | Plataforma serverless para hospedar o container. |
|  | **Google Cloud Build** | Serviço de CI/CD para automação do build e deploy. |
|  | **Google Secret Manager** | "Cofre" para armazenar as chaves de API e do banco de dados. |
|  | **Docker** | Tecnologia de containerização para empacotar o app. |
| **Outros** | **pypdf** | Biblioteca para extração de texto de arquivos .pdf. |
|  | **Chart.js** | Biblioteca para renderização dos gráficos do dashboard. |
|  | **chartjs-plugin-datalabels** | Plugin para exibir porcentagens e valores dentro dos gráficos. |

## **Rodando Localmente**

Estes passos são para rodar o projeto em seu ambiente local para desenvolvimento.

### **1\. Pré-requisitos**

* [Python 3.9+](https://www.python.org/downloads/)  
* [Git](https://www.google.com/search?q=https://git-scm.com/downloads)

### **2\. Clonar o Repositório**

```bash
   git clone https://github.com/pedrosmithhh/FinFlow.git
```
### **3\. Configurar Ambiente Virtual**

```bash 
   python -m venv venv
```

### **4\. Instalar Dependências**

Instale todas as bibliotecas Python necessárias.

```bash
   pip install -r requirements.txt
```
### **5\. Configurar Variáveis de Ambiente**

Crie um arquivo chamado .env dentro da pasta backend/. Este arquivo armazena seus segredos locais.

```env
# Obtenha sua chave de API no Google AI Studio  
API\_KEY=SUA\_CHAVE\_SECRETA\_DO\_GEMINI\_AQUI
```

```env
# Use qualquer string longa e aleatória  
FLASK\_SECRET\_KEY=SUA\_CHAVE\_SECRETA\_ALEATORIA\_DO\_FLASK
```
```env
# String de conexão URI do seu banco Supabase  
DATABASE\_URL=postgresql://postgres:\[SUA\_SENHA\]@db.\[SEU\_HOST\].supabase.co:5432/postgres
```

### **6\. Executar a Aplicação Localmente**

Antes de rodar, crie as tabelas no seu banco Supabase (veja a seção de Deploy).

```bash 
   python app.py
```

A aplicação estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

## **Deploy em Produção (GCP)**

Este projeto está configurado para deploy automático. Os passos de configuração inicial são:

1. **Configurar o Supabase:** Crie um projeto no Supabase (PostgreSQL) e obtenha sua DATABASE_URL.  
2. **Criar Tabelas:** Rode o SQL de init_db() uma vez no SQL Editor do Supabase para criar a tabela historico.  
3. **Configurar o GCP:**  
   * Crie um projeto no Google Cloud.  
   * Ative as APIs: Cloud Run, Cloud Build, Secret Manager, Artifact Registry.  
   * Crie um repositório no Artifact Registry (ex: finflow-repo).  
   * Salve suas três variáveis (API\_KEY, FLASK\_SECRET\_KEY, DATABASE\_URL) no Secret Manager (ex: FINFLOW\_API\_KEY, etc).  
4. **Configurar Permissões (IAM):** Dê ao Agente de Serviço do Cloud Build (...@cloudbuild.gserviceaccount.com) os papéis de Cloud Run Admin e Secret Manager Secret Accessor.  
5. **Criar o Gatilho (Trigger):** No Cloud Build, crie um gatilho que monitora a branch main e aponta para o arquivo cloudbuild.yaml.

Após esta configuração, **todo git push origin main** irá automaticamente construir o container, salvar no Artifact Registry e implantar a nova versão no Cloud Run.

Para acessar a aplicação, acesse este link: https://finflow-service-794146794944.us-central1.run.app/

