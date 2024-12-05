from langchain_core.messages import HumanMessage
from .agent import INPUT_MESSAGE, output
from .agent_chat import agent_chat
import json
import threading


def chat(bot_setting_file: str):
    history = []
    stop_event = threading.Event()

    def user_input_listener():
        while not stop_event.is_set():
            input_text = input()
            if input_text:
                stop_event.set()
                if not input_text.startswith(INPUT_MESSAGE):
                    raise ValueError("Invalid message")
                message = json.loads(input_text[len(INPUT_MESSAGE):])
                history.append(HumanMessage(message["content"]))
                # 中断当前的机器人输出
                print("User interrupted the bot.")
                # 重新开始对话
                chat(bot_setting_file)

    input_thread = threading.Thread(target=user_input_listener)
    input_thread.start()

    while not stop_event.is_set():
        result = agent_chat(bot_setting_file, history)
        history.append(output("assistant", result))
        print(result)  # 输出机器人回复

    input_thread.join()


def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    result = agent_chat(bot_setting_file, history)
    return result
