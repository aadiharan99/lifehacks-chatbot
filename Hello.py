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
import google.generativeai as palm
import time

LOGGER = get_logger(__name__)



def run():
   
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if prompt := st.chat_input("Ask away!"):
    # Display user message in chat message container
      with st.chat_message("user"):
          st.markdown(prompt)
      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": prompt})
    
    ## need to have the bot say a default hello first
      with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        palm.configure(api_key= st.secrets["PALM-AI-API-KEY"])

        defaults = {
          'model': 'models/chat-bison-001',
          'temperature': 0.25,
          'candidate_count': 1,
          'top_k': 40,
          'top_p': 0.95,
        }
        context = "You are a life-guru with the solution to most if not all the problems in the world. You need to give a crisp and concise solution to problems posed to you. List all possible solutions and life hacks for the problem posed as a numbered list, along with examples if applicable. Your core domains of expertise are travel, cooking, kitchen and home and life. Introduce to the user that you can offer solutions to most problems in your core domain."
        examples = [
            [
              "Hi",
              "Hello there. How are you doing today?"
            ],
            [
              "I am doing good.",
              "Great! Is there anything I can help you with?"
            ],
            [
              "What can you help me with?",
              "I can provide solutions to most problems in the domain of travel, cooking, kitchen, home and life. Feel free to try me out."
            ]
          ]
        messages = []
        messages.append(prompt)
        response = palm.chat(
          **defaults,
          context=context,
          examples=examples,
          messages=messages
        )
        result = response.last # Response of the AI to your most recent request

        for chunk in result.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": full_response})




if __name__ == "__main__":
    st.set_page_config(
        page_title="LifeBot",
        layout="wide",

    )
    st.session_state.intro = False
    st.title("LifeBot: The Lifehacks chatbot")
    st.divider()      
    run()
    st.session_state.intro = True
