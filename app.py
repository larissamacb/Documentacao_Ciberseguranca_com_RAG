import streamlit as st
import os
import base64
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="RAG - Hospital LISA", layout="wide")
load_dotenv()

DOCS_FOLDER = "docs_hospital"
INDEX_FOLDER = "faiss_index" 

NOME_DOS_ARQUIVOS = {
    "PSI_Politica_de_Segurança_da_Informacao.pdf": "Política de Segurança da Informação",
    "PUA_Politica_de_Uso_Aceitavel.pdf": "Política de Uso Aceitável",
    "PCI_Politica_de_Classificacao_da_Informacao.pdf": "Política de Classificação da Informação",
    "PGA_Politica_de_Gestao_de_Acessos.pdf": "Política de Gestão de Acessos",
    "Norma_de_Backup_e_Retencao_de_Dados.pdf": "Norma de Backup e Retenção de Dados",
    "PCN_DRP_Plano_de_Continuidade_de_Negocios_e_Recuperacao_de_Desastres.pdf": "Plano de Continuidade de Negócios e Recuperação de Desastres",
    "Plano_de_Resposta_a_Incidentes.pdf": "Plano de Resposta a Incidentes",
    "Procedimento_de_Gerenciamento_de_Seguranca_de_Dispositivos_Medicos_Conectados_IoMT.pdf": "Segurança de Dispositivos Médicos (IoMT)"
}

# Configuração da API key (no caso, sendo utilizada a do Gemini)
def get_api_key():
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        try:
            return st.secrets["GOOGLE_API_KEY"]
        except:
            return None
    return key

api_key = get_api_key()
if not api_key:
    st.error("❌ Configure a GOOGLE_API_KEY no .env")
    st.stop()
os.environ["GOOGLE_API_KEY"] = api_key


def process_pdfs_with_metadata():
    """Lê os PDFs e cria chunks preservando a origem (Fonte e Página)."""
    texts = []
    metadatas = []
    
    if not os.path.exists(DOCS_FOLDER):
        os.makedirs(DOCS_FOLDER)
        return [], []

    files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith('.pdf')]
    if not files: return [], []

    progress_bar = st.progress(0, text="Indexando documentos com referências...")
    total = len(files)
    
    for i, filename in enumerate(files):
        nome_bonito = NOME_DOS_ARQUIVOS.get(filename, filename)
        
        try:
            pdf_path = os.path.join(DOCS_FOLDER, filename)
            pdf_reader = PdfReader(pdf_path)
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                
                if page_text:
                    chunk_size = 1000
                    page_chunks = [page_text[j:j+chunk_size] for j in range(0, len(page_text), chunk_size)]
                    
                    for chunk in page_chunks:
                        texts.append(chunk)
                        metadatas.append({
                            "source": nome_bonito,
                            "page": page_num 
                        })
        except Exception as e:
            st.warning(f"Erro ao ler {filename}: {e}")
            
        progress_bar.progress((i + 1) / total, text=f"Lendo: {filename}")
    
    progress_bar.empty()
    return texts, metadatas


def create_vector_store():
    texts, metadatas = process_pdfs_with_metadata()
    if not texts: return False, []
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    vector_store.save_local(INDEX_FOLDER)
    unique_files = list(set([m["source"] for m in metadatas]))
    return True, unique_files


def manual_rag_response(user_question):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        new_db = FAISS.load_local(INDEX_FOLDER, embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question, k=4)
        
        context_parts = []
        for doc in docs:
            source = doc.metadata.get("source", "Fonte Desconhecida")
            page = doc.metadata.get("page", "-")
            content = doc.page_content
            formatted_chunk = f"---\nFonte: {source}\nPágina: {page}\nConteúdo: {content}\n---"
            context_parts.append(formatted_chunk)
            
        context_text = "\n".join(context_parts)
        
        prompt_template = """
        Você é um assistente sênior de cibersegurança (SOC).
        Analise o contexto abaixo para responder à pergunta do usuário.

        CONTEXTO:
        {context}

        PERGUNTA:
        {question}

        ---
        INSTRUÇÕES DE RACIOCÍNIO (LEIA COM ATENÇÃO):

        1. **ASSOCIAÇÃO TÉCNICA (Permitido):**
           - Se o usuário perguntar sobre um termo específico (ex: "Ransomware", "Worm", "Trojan") e essa palavra NÃO estiver no texto, você DEVE buscar por procedimentos genéricos que se aplicam (ex: "Resposta a Incidentes", "Malware", "Código Malicioso", "Recuperação de Desastres").
           - Nesses casos, responda explicando a conexão, como no exemplo: "Embora o termo exato 'Ransomware' não seja citado, o [Nome do Documento] define procedimentos para incidentes de código malicioso/malware que se aplicam..."

        2. **PERGUNTAS FORA DO TEMA (Proibido):**
           - Se a pergunta for totalmente irrelevante para segurança/TI (ex: cor de objetos, receitas, futebol), diga APENAS: "A informação solicitada não consta nas políticas internas carregadas." e pare.

        3. **FORMATAÇÃO (Se houver resposta):**
           - Responda tecnicamente.
           - Pule duas linhas no final.
           - Escreva "📚 Referências Consultadas".
           - Liste: * Nome do Documento (Página X).
        """
        
        model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        final_prompt = prompt.format(context=context_text, question=user_question)
        
        response_text = model.invoke(final_prompt).content
        clean_text = response_text.replace("<br>", "\n").replace("<br/>", "\n")
        
        if "📚 Referências Consultadas" in clean_text:
            disclaimer = "\n\n> ℹ️ **Nota de Navegação:** A paginação citada acima segue a numeração interna do arquivo. Ao buscar no visualizador, adicione 1 ao número da página."
            return clean_text + disclaimer
        else:
            return clean_text
        
    except RuntimeError:
        return "⚠️ Índice desatualizado. Apague a pasta 'faiss_index' para recriar."
    except Exception as e:
        return f"Erro: {str(e)}"


def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page=1" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# --- Interface ---
def main():
    st.header("🏥 RAG - Hospital LISA")
    
    if "selected_pdf" not in st.session_state:
        st.session_state.selected_pdf = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not os.path.exists(INDEX_FOLDER):
        with st.status("⚙️ Atualizando sistema...", expanded=True) as status:
            st.write("Reindexando documentos...")
            success, files = create_vector_store()
            if success:
                status.update(label="Pronto!", state="complete", expanded=False)
                st.rerun()
            else:
                st.error("Pasta vazia.")
                st.stop()

    # Sidebar
    with st.sidebar:
        if st.button("🗑️ Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.title("📂 Documentação")
        
        if os.path.exists(DOCS_FOLDER):
            files = sorted([f for f in os.listdir(DOCS_FOLDER) if f.endswith('.pdf')])
            if files:
                for f in files:
                    nome_botao = NOME_DOS_ARQUIVOS.get(f, f.replace(".pdf", "").replace("_", " ").title())
                    if st.button(f"📄 {nome_botao}", key=f, use_container_width=True):
                        st.session_state.selected_pdf = f
                        st.rerun()
            else:
                st.warning("Nenhum PDF encontrado.")

    # Modo Leitura
    if st.session_state.selected_pdf:
        nome_arquivo = st.session_state.selected_pdf
        titulo_bonito = NOME_DOS_ARQUIVOS.get(nome_arquivo, nome_arquivo)
        pdf_path = os.path.join(DOCS_FOLDER, nome_arquivo)
        
        st.info(f"📖 Modo Leitura: **{titulo_bonito}**")
        
        if st.button("⬅️ Fechar Documento e Voltar ao Chat", type="primary", use_container_width=True):
            st.session_state.selected_pdf = None
            st.rerun()
        
        display_pdf(pdf_path)

    # Modo Chat
    else:
        st.divider()
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_question = st.chat_input("Ex: Qual o plano de resposta a incidentes?")

        if user_question:
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)
            
            with st.spinner("Analisando documentos..."):
                response = manual_rag_response(user_question)
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()