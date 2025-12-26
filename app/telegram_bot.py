import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send(text: str) -> bool:
    """
    Send a message to the admin via Telegram bot
    
    Args:
        text (str): Message text to send
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        bot_token = os.getenv('bot_token')
        admin_id = os.getenv('admin_id')
        
        if not bot_token or not admin_id:
            print("Error: bot_token or admin_id is not set in .env file")
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            'chat_id': admin_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("Message sent successfully!")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending message: {e}")
        return False


# Тестирование (опционально)
if __name__ == "__main__":
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('bot_token=your_bot_token_here\n')
            f.write('admin_id=your_admin_id_here\n')
        print("Please update the .env file with your bot token and admin ID")
    else:
        # Тест отправки
        result = send("🚀 Тестовое сообщение от Flask бота!")
        print(f"Test result: {result}")