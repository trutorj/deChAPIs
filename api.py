from src.config import PORT
from src.app import app
import src.controllers.create_user
import src.controllers.create_chat
import src.controllers.add_user_chat
import src.controllers.create_message
import src.controllers.extract_messages
import src.controllers.sentiment_analysis
import src.controllers.recomendator
import src.controllers.recomend_user
import src.controllers.inicio

app.run("0.0.0.0", PORT, debug=True)