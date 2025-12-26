import os
import dotenv
dotenv.load_dotenv()


CRYPTO_BOT_TOKEN = os.getenv('CRYPTO_BOT_TOKEN')
API_URL = "https://pay.crypt.bot/api/createInvoice"
UPLOAD_FOLDER_MUSIC = 'static/uploads/music'
UPLOAD_FOLDER_AVATARS = 'static/uploads/avatars'