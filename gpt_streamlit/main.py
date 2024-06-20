from openai import OpenAI
from time import sleep
import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

from assistant_message import AssistantMessage

title = 'DC Healthy Homes Survey'
assistant_id = 'asst_3voxEjRL0twsoN72h41xxueJ'

client = OpenAI(
    organization=st.secrets["openai"]["org"],
    api_key=st.secrets["openai"]["api_key"]
)

def get_thread_id():
    if 'thread_id' not in st.session_state:
        print('Creating a new thread.')
        thread = client.beta.threads.create()
        st.session_state['thread_id'] = thread.id
    return st.session_state['thread_id']

def add_user_message(msg):
    thread_id = get_thread_id()
    print(f'Adding user message to thread: {thread_id}')
    user_msg = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=msg
    )
    run_assistant()

def run_assistant():
    thread_id = get_thread_id()
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    check_assistant_response(run)

def check_assistant_response(run):
    thread_id = get_thread_id()
    while run.status in ['queued', 'in_progress']:
        updated_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        print(f'Run status: {updated_run.status}')
        if updated_run.status == 'completed':
            handle_new_assistant_messages()
            break
        elif updated_run.status in ['queued', 'in_progress']:
            sleep(0.5)
            pass
        else:
            print(f'Run ended with status: {updated_run.status}')
            break

def handle_new_assistant_messages():
    thread_id = get_thread_id()
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    assistant_messages = []

    count = 0

    for msg in messages:
        count += 1
        message_content = msg.content[0].text
        annotations = message_content.annotations

        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, '')

        assistant_messages.append(AssistantMessage(msg.id, msg.role, message_content.value))

    for msg in reversed(assistant_messages):
        if msg.role == 'user':
            message(msg.text, is_user=True, avatar_style="adventurer", key=msg.message_id + '_user')
        else:
            message(msg.text, key=msg.message_id)

    st.session_state.message_count = count

def user_prompt_submit():
    user_input = st.session_state.input
    st.session_state.prompt = user_input
    st.session_state['input'] = ''

st.set_page_config(page_title=f"{title} ChatBot", page_icon="🤖", layout="wide")

if 'prompt' not in st.session_state:
    st.session_state.prompt = ''

if 'message_count' not in st.session_state:
    st.session_state.message_count = 1

html(f"""
<script>
    function scroll(index){{
        setTimeout(() => {{
            const container = parent.document.querySelector('.block-container');
            if (!container) return false;
            container.scrollTop = container.scrollHeight;
            if (index > -1) {{
                scroll(-1);
            }}
        }}, "3000");
    }}
    scroll({st.session_state.message_count});
</script>
""")

intro_text = '''Thank you for participating in our survey. Your input is invaluable to our research at Howard University, School of Social Work, where we are investigating the impact and effectiveness of the DC Healthy Homes Program. This program aims to improve the health and well-being of residents by addressing housing-related health issues.

Please be assured that all information you provide will be kept strictly confidential. Your responses will be used solely for research purposes and will not be shared with anyone outside of our research team. We are committed to protecting your privacy and ensuring the anonymity of your responses.

To begin, we kindly ask you to provide your name and age.
'''

message(intro_text, key='-1')

if st.session_state.prompt:
    add_user_message(st.session_state.prompt)

st.text_input(key='input',
              on_change=user_prompt_submit,
              label='Type in your question here',
              label_visibility='hidden',
              placeholder='Type in your question here')

styl = f"""
<style>
    .stTextInput {{
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        width: 96vw;
        margin: auto;
    }}    

    .block-container {{
        position: fixed !important;
        bottom: 1rem !important;
        padding: 0 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        max-height: 90vh !important;
        width: 96vw !important;
    }}

    #MainMenu {{
        display: none;
    }}

    footer {{
        display: none;
    }}
    
    iframe[title="st.iframe"] {{
        height: 0px;
        overflow: hidden;
        display: block;
    }}

</style>
"""
st.markdown(styl, unsafe_allow_html=True)
