from chat.utils import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
    
)
import re
import json
from flask import abort,jsonify,make_response



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

def create_questions(obj_chat):
    

    raw_text = get_pdf_text(obj_chat["url_pdf"])
    print(obj_chat["url_pdf"])
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)
    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    questions = get_conversation_chain(vectorstore, "Crea preguntas y respuestas sobre el documento. Cada pregunta y respuesta será un objeto y estará en un array de objetos, se seguirá este formato: {[pregunta: 'ejemplo pregunta', respuesta: 'ejemplo respuesta']}. En caso no se pueda obtener preguntas, se devolverá un mensaje en formato json siguiendo este formato: {error: 'Error no se pudo generar preguntas'}")

    print(questions)
    try:
        questions = json.loads(questions)
        
    except:
        error_message = {"error": "Failed to generate questions"}
        response = make_response(jsonify(error_message), 400)
        response.headers["Content-Type"] = "application/json"
        abort(response)



    return questions
    
