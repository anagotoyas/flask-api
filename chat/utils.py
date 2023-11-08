from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
import requests
from io import BytesIO
from transformers import pipeline
import PyPDF2

# this is dark magic, don't touch unless you are a dark wizard


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(
    vectorstore,
    question,
):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )

    answer = conversation_chain.run({"question": question})
    return answer


def get_pdf_text(url):
    text = ""

    # Descarga el archivo PDF
    response = requests.get(url)

    # Comprueba que la solicitud fue exitosa
    if response.status_code == 200:
        # Crea un objeto BytesIO a partir del contenido del PDF
        pdf_file = BytesIO(response.content)

        # Crea un objeto PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Obtiene el número de páginas
        for page in pdf_reader.pages:
            partText = page.extract_text()
            text += partText
    else:
        print("No se pudo descargar el archivo.")

    return text


def summarize(chunks):
    summarizer = pipeline("summarization")
    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
    return " ".join([summ["summary_text"] for summ in res])
