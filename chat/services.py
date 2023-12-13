from chat.utils import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
)
import re
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
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)
    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    questions = get_conversation_chain(vectorstore, "Dame preguntas sobre la información más importante")

    

    elementos_separados = questions.split("\n")

# Almacenar los elementos en un array
    array_elementos = []
    for elemento in elementos_separados:
        array_elementos.append(elemento)

    # Imprimir el array resultante

    filtered_list = list(filter(bool, array_elementos))

    print(filtered_list)

    return filtered_list
        
        


def extract_flashcards(obj_chat):
    # Call create_questions to generate questions dynamically
    preguntas = create_questions(obj_chat)
    raw_text = get_pdf_text(obj_chat["url_pdf"])
    # get the text chunks
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)

    if len(preguntas) == 1:
        error_message = {"error": "No se encontraron preguntas en el documento."}
        response = make_response(jsonify(error_message), 400)
        response.headers["Content-Type"] = "application/json"
        abort(response)



    preguntas_respuestas = []

    for pregunta in preguntas:
    # Obtener la respuesta del sistema para cada pregunta
        respuesta = get_conversation_chain(vectorstore, pregunta)
       
    
        # Crear objeto con pregunta y respuesta
        objeto_pregunta_respuesta = {
            "pregunta": pregunta,
            "respuesta": respuesta
        }
    
        # Agregar objeto al array
        preguntas_respuestas.append(objeto_pregunta_respuesta)


    print(preguntas_respuestas)


    return preguntas_respuestas