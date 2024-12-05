from langchain_core.messages import HumanMessage, AIMessage
from .agent import INPUT_MESSAGE, output, CHAT_DATA, clear_chat_data
from .agent_chat import agent_chat
import json
import threading


def chat(bot_setting_file: str):
    history = []
    while True:
        input_text = input()
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(input_text[len(INPUT_MESSAGE) :])
        history.append(HumanMessage(message["content"]))
        clear_chat_data()
        agent_chat_thread = threading.Thread(target=agent_chat, args=(bot_setting_file, history))
        agent_chat_thread.start()
        agent_chat_thread.join()
        history.append(AIMessage(content=CHAT_DATA["output"]))


def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    clear_chat_data()
    agent_chat(bot_setting_file, history)
    return CHAT_DATA["output"]
