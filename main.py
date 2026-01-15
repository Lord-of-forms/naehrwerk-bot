#!/usr/bin/env python3
"""
NährWerk Bot - Ernährungsassistent mit Mistral AI & Slack
"""
import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from mistralai import Mistral
import re
import requests
import base64
from supabase import create_client, Client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment Variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = App(token=SLACK_BOT_TOKEN)
mistral = Mistral(api_key=MISTRAL_API_KEY)
conversations = {}

# Database Helper Functions
def create_or_get_user(slack_user_id: str):
    """Create or get user from database"""
    try:
        result = supabase.table('users').select('*').eq('slack_user_id', slack_user_id).execute()
        if result.data:
            return result.data[0]
        else:
            new_user = supabase.table('users').insert({'slack_user_id': slack_user_id}).execute()
            return new_user.data[0]
    except Exception as e:
        logger.error(f"Error creating/getting user: {e}")
        return None

def save_meal(user_id: int, meal_type: str, description: str, calories: int = None):
    """Save a meal to the database"""
    try:
        meal_data = {
            'user_id': user_id,
            'meal_type': meal_type,
            'description': description
        }
        if calories:
            meal_data['calories'] = calories
        result = supabase.table('meals').insert(meal_data).execute()
        logger.info(f"✅ Meal saved for user {user_id}")
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error saving meal: {e}")
        return None


           @app.event("file_shared")
def handle_file_upload(event, say, client):
    """Handle file uploads for image recognition"""
    file_id = event["file_id"]
    user_id = event["user_id"]
    channel_id = event.get("channel_id")
    
    logger.info(f"📷 File upload from {user_id}: {file_id}")
    
    try:
        # Get file info from Slack
        file_info = client.files_info(file=file_id)["file"]
        file_url = file_info.get("url_private")
        mimetype = file_info.get("mimetype", "")
        
        # Only process images
        if not mimetype.startswith("image/"):
            return
        
        # Download image
        import headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
        response = requests.get(file_url, headers=headers)
        image_data = response.content
        
        # Encode image to base64 for Mistral
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        # Send to Mistral with image
        if user_id not in conversations:
            conversations[user_id] = []
        
        # Add image message
        conversations[user_id].append({
            "role": "user",
            "content": [
                {"type": "text", "text": "Analysiere dieses Bild und identifiziere die Lebensmittel."},
                {"type": "image_url", "image_url": f"data:{mimetype};base64,{image_base64}"}
            ]
        })
        
        # Get response from Mistral
        response = mistral.agents.complete(
            agent_id=AGENT_ID,
            messages=conversations[user_id]
        )
        
        answer = response.choices[0].message.content
        conversations[user_id].append({"role": "assistant", "content": answer})
        
        # Send response
        if channel_id:
            say(text=answer, channel=channel_id)
        else:
            # Send DM if no channel
            client.chat_postMessage(channel=user_id, text=answer)
        
        logger.info("✅ Image analysis sent")
        
    except Exception as e:
        logger.error(f"❌ Error processing image: {e}")
        error_msg = f"⚠️ Fehler beim Analysieren des Bildes: {e}"
        if channel_id:
            say(text=error_msg, channel=channel_id)
        else:
            client.chat_postMessage(channel=user_id, text=error_msg)")
def handle_message(event, say, client):
    if event.get("bot_id") or event.get("subtype"):
        return
    
    user_id = event["user"]
    text = event.get("text", "")
    channel = event["channel"]
    thread_ts = event["ts"]
    
    logger.info(f"📩 Message from {user_id}: {text}")
    
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({"role": "user", "content": text})
    
    try:
        response = mistral.agents.complete(
            agent_id=AGENT_ID,
            messages=conversations[user_id]
        )
        
        answer = response.choices[0].message.content
        conversations[user_id].append({"role": "assistant", "content": answer})
        
        say(text=answer, channel=channel, thread_ts=thread_ts)
        logger.info("✅ Response sent")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        say(text=f"⚠️ Fehler: {e}", channel=channel, thread_ts=thread_ts)

@app.event("app_mention")
def handle_mention(event, say, client):
    user_id = event["user"]
    text = event.get("text", "")    # Remove bot mentions like <@U123456>
    channel = event["channel"]
    text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    thread_ts = event["ts"]
    
    logger.info(f"👋 Mention from {user_id}: {text}")
    
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({"role": "user", "content": text})
    
    try:
        response = mistral.agents.complete(
            agent_id=AGENT_ID,
            messages=conversations[user_id]
        )
        
        answer = response.choices[0].message.content
        conversations[user_id].append({"role": "assistant", "content": answer})
        
        say(text=answer, channel=channel, thread_ts=thread_ts)
        logger.info("✅ Response sent")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        say(text=f"⚠️ Fehler: {e}", channel=channel, thread_ts=thread_ts)
def main():
    logger.info("🍏 NährWerk Bot starting...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    logger.info("✅ Bot running!")
    handler.start()

if __name__ == "__main__":
    main()
