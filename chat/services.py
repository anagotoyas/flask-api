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
    question = "Dame un resumen de una hoja o menos, resaltando puntos y detalles importantes, separalo por parrafos en caso si se pudiese, de caso contrario solo dame una idea general"
    raw_text = get_pdf_text(obj_chat["url_pdf"])
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    print(text_chunks, "texto")
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

    print(text_chunks, "texto")

    questions = get_conversation_chain(vectorstore, "Crea preguntas y respuestas, al menos una, respecto al contenido que te estoy pasando, como para evaluar si entendió lo que dice el contenido. Cada pregunta y respuesta será un objeto y estará en un array de objetos, se seguirá este formato: {['pregunta': 'ejemplo pregunta', 'respuesta': 'ejemplo respuesta']}. Trata por favor, de al menos generar una pregunta con su respectiva respuesta y como máximo cinco, tu decide la cantidad en base a la información proporcionada, ten en cuenta que aunque sea una sola pregunta y respuesta, debe devolverla en un array del objeto previamente mencionado")

    try:
        if isinstance(questions, str):  
            questions = eval(str(questions))
        else:
            questions = questions
        
        
    except:
        error_message = {"error": "Failed to generate questions"}
        response = make_response(jsonify(error_message), 400)
        response.headers["Content-Type"] = "application/json"
        abort(response)



    return questions
    
