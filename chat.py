import os
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

llm_name = "nsdr_generator"
human_name = "nsdr_practitioner"

system_prompt = """
    Generate a guided Non-Sleep Deep Rest (NSDR) session. This session should provide listeners with a deep sense of relaxation without inducing sleep. Begin with a gentle introduction, then guide the listener through deep breathing exercises, body awareness, and visualization techniques. The language used should be soothing and positive. Ensure the session remains engaging and does not encourage drowsiness. Conclude with a gentle return to awareness and a sense of rejuvenation.

    Do not respond with anything other than the script. The script should not contain any /n characters. The script should utilize semicolons(;) to represent 500ms pauses in audio. Semicolons can also be chained together to create longer pauses. Pauses should be used generously, especially during breathing excersizes or when doing body awarness and visualization.
"""

def get_chat(temperature=1.2, model='gpt-3.5-turbo'):
    openai_api_key = os.environ["OPENAI_API_KEY"]
    chat = ChatOpenAI(openai_api_key=openai_api_key,
                      temperature=temperature, model=model, client=None)  # temp 1.0 is default
    return chat

def build_chat_prompt(prompt_message):
    return [SystemMessage(content=system_prompt, additional_kwargs={"name": llm_name}), HumanMessage(content=prompt_message, additional_kwargs={"name": human_name})]
