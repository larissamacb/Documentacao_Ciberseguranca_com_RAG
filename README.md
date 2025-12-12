# 🏥 Hospital LISA - Dossiê de Documentos + RAG

> *Dossiê de Segurança da Informação potencializado por uma interface de IA Generativa (RAG).*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Status](https://img.shields.io/badge/Status-Concluído-success)

---

## 📋 Índice

* [🎯 Sobre o Projeto](#-sobre-o-projeto)
* [🏢 Cenário do Projeto: Hospital LISA](#-cenário-do-projeto-hospital-lisa)
* [🚀 Funcionalidades do Sistema (RAG)](#-funcionalidades-do-sistema-rag)
* [📂 Documentação](#-documentação)
* [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
* [⚙️ Como Executar](#️-como-executar)
* [🧠 Experiência e Aprendizados](#-experiência-e-aprendizados)
* [🤝 Créditos](#-créditos)

---

## 🎯 Sobre o Projeto

Este repositório é fruto de um **Projeto Integrador de Cibersegurança** da faculdade. O desafio acadêmico proposto foi desenvolver um **Dossiê Completo de Segurança da Informação** (políticas, normas e procedimentos) para uma empresa fictícia do setor de saúde, batizada de **Hospital LISA** (LISA = Larissa Igo Samuel Ageu, referenciando os integrantes do grupo).

Embora o escopo acadêmico exigisse apenas a elaboração dos documentos em PDF, tomei a iniciativa de desenvolver também uma aplicação simples para facilitar o acesso e a consulta à temas específicos dessas normas.

Entendendo que documentos de compliance costumam ser densos e de difícil consulta rápida, criei um **Chatbot RAG (Retrieval-Augmented Generation)**. Isso permite que qualquer colaborador fictício do hospital tire dúvidas sobre as políticas conversando em linguagem natural.

---

## 🏢 Cenário do Projeto: Hospital LISA

O ambiente hospitalar exige conformidade rigorosa (LGPD/HIPAA) e alta disponibilidade.
* **Ambiente:** Sistemas de prontuários eletrônicos, dados sensíveis de pacientes, dispositivos médicos conectados (IoMT).
* **Foco:** Confidencialidade, privacidade e controles de acesso.
* **Risco Crítico:** Vazamento de dados médicos.

---

## 🚀 Funcionalidades do Sistema (RAG)

O sistema atua como um **Analista de SOC Virtual**, facilitando a navegação pelo dossiê criado:

* **🧠 IA Generativa:** Interpreta perguntas técnicas e responde com base estritamente nos documentos do dossiê.
* **🔍 Rastreabilidade:** Cada resposta cita a Fonte (Nome da Política) e a Página exata onde a regra se encontra.
* **💡 Inferência Semântica:** O sistema correlaciona temas. Por exemplo, se o usuário pergunta sobre *"Vírus"*, a IA busca as normas de *"Resposta a Incidentes"* ou *"Uso Aceitável"*.
* **📖 Leitor Integrado:** Visualização dos PDFs originais dentro da própria ferramenta, sem necessidade de download externo.

---

## 📂 Documentação

A base de conhecimento do sistema é composta pelas seguintes normas desenvolvidas pela equipe:

1.  **PSI – Política de Segurança da Informação:** Diretrizes macro e responsabilidades.
2.  **Política de Uso Aceitável:** Regras para e-mail, internet e BYOD.
3.  **Política de Classificação da Informação:** Níveis de confidencialidade.
4.  **Política de Gestão de Acessos:** Controle de senhas, MFA e revogação.
5.  **Norma de Backup e Retenção:** Procedimentos de cópia, janelas de backup e restore.
6.  **PCN e DRP:** Plano de Continuidade e Recuperação de Desastres.
7.  **Plano de Resposta a Incidentes:** Fluxo de triagem, contenção e erradicação.
8.  **Segurança em IoMT:** Procedimento específico para Dispositivos Médicos Conectados.

Os documentos podem ser encontrados e lidos separadamente na pasta `docs_hospital`, que contém todos eles em PDF, ou pelo próprio visualizador de arquivos dentro da aplicação.

Todos estão reunidos como um dossiê no documento `Dossie_Hospital_LISA`, presente na raiz do repositório.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface:** Streamlit
* **IA & Orquestração:** LangChain
* **LLM:** Google Gemini 2.5 Flash (via API)
* **Vetorização:** FAISS & HuggingFace Embeddings (Processamento local dos vetores).

---

## ⚙️ Como Executar

### Pré-requisitos
* Python 3.9 ou superior.
* Uma chave de API do Google (Google AI Studio).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/larissamacb/Documentacao_Ciberseguranca_com_RAG.git
    cd documentacao_ciberseguranca_com_rag
    ```

2.  **Ambiente Virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate  # Windows
    ```

3.  **Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração:**
    Crie um arquivo `.env` na raiz e adicione:
    ```env
    GOOGLE_API_KEY="sua_chave_aqui"
    ```
    Você pode obter uma chave do Gemini [por este link](https://aistudio.google.com/api-keys)
    > Observação: atualmente (hoje é dia 12/12/2025), uma chave gratuita dessa versão (Gemini 2.5 Flash) permite 20 requisições diárias. Faça uma alteração manual no código caso queira utilizar outra versão ou API.

6.  **Execução:**
    ```bash
    streamlit run app.py
    ```

---

## 🧠 Experiência e Aprendizados 
#### (Este é um texto 100% autoral)

Apesar de ter sido um projeto, de certa forma, não prático (é claro que o desenvolvimento de documentos é prático, mas quero dizer que não é a experiência real de vivenciar as práticas neles citadas), o considerei como extremamente importante pelas pesquisas que tiveram de ser feitas e até mesmo as correções que o professor pedia, apontando coisas importantes que deveriam ser citadas e outros aspectos. 

Por exemplo, algo que muitas vezes esquecíamos e que ele sempre mencionava eram os indicadores de desempenho e métricas de conformidade. Quando percebi isso, me toquei do quanto essa parte era relevante. Não adianta que sejam cuspidas regras e procedimentos se não existe a previsão de medir o seu real cumprimento e avaliar os resultados obtidos com essas práticas. É por isso que são feitas auditorias, e para que elas sejam feitas, os indicadores e métricas não necessários. 

Como eu disse, não vivenciamos verdadeiramente o ambiente de um hospital que segue políticas de segurança, mas não deixou de ser uma imersão. Precisamos pensar sobre os procedimentos que deveriam ser seguidos, e o mais interessante, dentro do foco desse cenário, que é, aplicando a tríade CIA: 
* **Confidencialidade** de Dados Pessoais Sensíveis de pacientes
* **Integridade** desses dados para a aplicação correta de procedimentos médicos
* **Disponibilidade** de dados e dispositivos médicos para a não interrupção de atendimentos

Ao contextualizar esses conceitos em um ambiente real e tão crítico como um hospital, percebemos que não é apenas uma decoreba irrelevante de fundamentos de cibersegurança. São pilares que devem ser a todo momento relembrados e aplicados, e nesse estudo de caso, visando o **tratamento médico** de **vidas**, além da **integridade pessoal** de pacientes. A importância da rede, dos dados e sua segurança chegaram a esse nível! Por isso que o seu manipulamento não deve ser feito de qualquer jeito.

O último documento do projeto é um procimento específico que cada grupo deveria escolher de acordo com seu setor, e no caso do meu, foi o Procedimento de Gerenciamento de Segurança de Dispositivos Médicos Conectados (IoMT). A ideia veio de um exemplo interessante que encontrei fazendo pesquisas para uma apresentação de outra matéria, o de um caso em que foi descoberta uma vulnerabilidade nos marca-passos (dispositivo implantado no corpo para regular o ritmo cardíaco, emitindo impulsos elétricos) de um hospital que permitia que atacantes pudessem controlá-los de longe, literalmente com a capacidade de matar alguém. Felizmente, perceberam e corrigiram antes que acontecesse algo, mas esse caso toca em um tema importante e muitas vezes negligenciado: a segurança de dispositivos IoT (que foi, realmente, um dos temas dessa apresentação).

Não paramos pra pensar nisso, mas um hospital é um ambiente cheio desses dispositivos conectados à rede, porque são diversos os equipamentos para exames que capturam os dados em tempo real e os transmitem para computadores. Passei, então, a ver esse documento como obrigatório, e naturalmente foi o procedimento específico escolhido para finalizar o dossiê.

Para postar esses documentos aqui em um repositório, achei que a melhor forma seria desenvolvendo também um RAG com uma interface simples, pelos motivos já explicados em [Sobre o Projeto](#-sobre-o-projeto). Até em um ambiente corporativo real me parece uma boa solução para facilitar o acesso e a revisão dos documentos pelos colaboradores, sem a necessidade de ter que reler cada um dos vários documentos em busca de sanar uma dúvida específica. A leitura inteira ainda pode ser feita conforme o que foi dito em [Documentação](#-documentação).

---

## 🤝 Créditos

* **O Dossiê do Hospital LISA foi desenvolvido em grupo por:**
[L](https://github.com/larissamacb)arissa, 
[I](https://github.com/igocecilio)go, 
[S](https://github.com/SamuelGdA)amuel e 
[A](https://github.com/Ageubr)geu

---
