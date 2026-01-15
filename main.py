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

app = App(token=SLACK_BOT_TOKEN)
mistral = Mistral(api_key=MISTRAL_API_KEY)
conversations = {}

@app.event("message")
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
    text = event.get("text", "")    channel = event["channel"]
    # Remove bot mentions like <@U123456>
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
