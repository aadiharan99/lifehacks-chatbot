# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import langchain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
import random
import time

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",

    )
    st.title("LifeHacker: The Lifehacks chatbot")
    st.divider()
    st.subheader("A conversational AI chatbot to generate life hacks for different situations in life, from travelling to kitchen to cleaning your apartment")
    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
      with st.chat_message("user"):
          st.markdown(prompt)
      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": prompt})
    
    ## need to have the bot say a default hello first
      with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        template = """You are a life guru who makes people's lives easier by giving life hacks to different situations. Given the text of question, it is your job to write a answer that question with example.
        {chat_history}
        Human: {question}
        AI:
        """
        prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
        memory = ConversationBufferMemory(memory_key="chat_history")

        llm_chain = LLMChain(
            llm=OpenAI(temperature=0.7, openai_api_key="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"),
            prompt=prompt_template,
            verbose=True,
            memory=memory,
        )

        result = llm_chain.predict(question=prompt)

        # assistant_response = random.choice(
        #     [
        #         "Hello there! How can I assist you today?",
        #         "Hi, human! Is there anything I can help you with?"
        #     ]
        # )
        # Simulate stream of response with milliseconds delay
        for chunk in result.split():
            full_response += chunk + " "
            time.sleep(0.15)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": full_response})




if __name__ == "__main__":
    run()
