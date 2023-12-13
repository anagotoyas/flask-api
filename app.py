from chat.routes import chat_bp
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask
from waitress import serve

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["https://voist.me","http://localhost:5173"])


app.register_blueprint(chat_bp)

if __name__ == '__main__':
    # serve(self.app, port=self.port)
    app.run(host='0.0.0.0', port=5002,threaded=True, debug=True, **{"timeout": 180})

