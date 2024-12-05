from langchain_core.messages import HumanMessage
from .agent import INPUT_MESSAGE, output
from .agent_chat import agent_chat
import json
import queue
import threading


def chat(bot_setting_file: str):
    history = []
    while True:
        input_text = input()
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(input_text[len(INPUT_MESSAGE) :])
        history.append(HumanMessage(message["content"]))
        result_queue = queue.Queue()
        agent_chat_thread = threading.Thread(target=agent_chat, args=(bot_setting_file, history, result_queue))
        agent_chat_thread.start()
        agent_chat_thread.join()
        result = result_queue.get()
        history.append(output("assistant", result))



def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    result_queue = queue.Queue()
    result = agent_chat(bot_setting_file, history, result_queue)
    return result
