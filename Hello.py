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
        context = "Be a life guru that provides tips for different real-life problems and situations, from travelling to kitchen hacks to creatively sprucing up your apartment. \nGive the response as a numbered list with concise information, each point being separated by a new line"
        examples = []
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
    # intro_placeholder = st.empty()
    # intro = ""
    # intro_text = "Travelling hacks, Life hacks, Kitchen problems, Trouble in Paradise? We have you covered. Ask Away!"
    # if not st.session_state.intro:
    #   for intro_chunk in intro_text.split():
    #         intro += intro_chunk + " "
    #         time.sleep(0.5)
    #         # Add a blinking cursor to simulate typing
    #         intro_placeholder.subheader(intro + "▌")
      

      # sample_prompts = ["What is the best time to book airplane tickets?", "How to optimize living space?", "How to do well in Life?"]


      # st.subheader("A conversational AI chatbot to generate life hacks for different situations in life, from travelling to kitchen to cleaning your apartment")
      # st.divider()
      
    run()
    st.session_state.intro = True
