from chat.utils import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
)


def create_chat(obj_chat):
    # result = db.session.query(Class).filter_by(id=obj_chat["class_id"]).first()
    # get pdf text
    print(obj_chat)
    raw_text = get_pdf_text(obj_chat["url_pdf"])
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)
    # create vector store
    vectorstore = get_vectorstore(text_chunks)
    # Generating an answer
    answer = get_conversation_chain(vectorstore, obj_chat["question"])

    # Return the new chat as json
    return answer


def create_resume(obj_chat):
    print(obj_chat)
    question = "Dame un resumen de 1 hoja, resaltando puntos y detalles importantes, separalo por parrafos"
    raw_text = get_pdf_text(obj_chat["url_pdf"])
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)
    # create vector store
    vectorstore = get_vectorstore(text_chunks)
    # Generating an answer
    answer = get_conversation_chain(vectorstore, question)
    return answer
