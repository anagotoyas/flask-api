# from flask_jwt_extended import jwt_required, get_jwt_identity
from decora.validator import request_validator
from flask import Blueprint, request, jsonify
from chat.services import create_chat, create_resume, extract_flashcards, create_questions
from chat.schemas import CreateChat, CreateResume, CreateFlashcards

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "¡Bienvenidos al API!"})

# CREATE CHAT
@chat_bp.route("/chat", methods=["POST"])
# @jwt_required(locations="headers")
@request_validator(request, CreateChat)
def create():
    # Jwt User

    # Generating a new answer and question
    answer = create_chat(request.json)
    print(answer)
    # Response
    return (
        jsonify({"answer": answer}),
        200,
    )


@chat_bp.route("/resume", methods=["POST"])
# @jwt_required(locations="headers")
@request_validator(request, CreateResume)
def resume():
    # Generating a new answer and question
    answer = create_resume(request.json)
    print(answer)
    return (
        jsonify({"answer": answer}),
        200,
    )

@chat_bp.route("/flashcards", methods=["POST"])
# @jwt_required(locations="headers")
@request_validator(request, CreateFlashcards)
def flashcards():
    # Generating flashcards
    flashcards = extract_flashcards(request.json)
    # print(flashcards)
    # Response
    return (
        jsonify(flashcards),
        200,
    )