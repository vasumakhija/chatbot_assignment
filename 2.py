# hiring_assistant.py

import streamlit as st
from typing import List
import requests
import time
import os
import json
from fpdf import FPDF

# === CONFIG ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"
SAVE_FILE = "candidates.json"

# === Prompt Templates ===
GREETING = """
You are TalentBot, a friendly and professional hiring assistant chatbot for TalentScout.
Greet the candidate and explain that you'll collect their basic info and ask relevant technical questions based on their tech stack.
"""

QUESTION_GENERATION_TEMPLATE = """
Generate exactly 5 technical interview questions based on this tech stack: {tech_stack}.
Include a mix of theoretical and practical questions.
Format the questions as a numbered list.
"""

END_PROMPT = """
The candidate said a conversation-ending word. Politely thank them and let them know the next steps. End the conversation.
"""

# === Groq Chat Function ===
def query_groq(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Exception: {e}"

# === Tech Stack Validation ===
def is_valid_tech_stack(stack: str) -> bool:
    validation_prompt = f"Is '{stack}' a valid tech stack (combination of programming languages, frameworks, or tools)? Just reply Yes or No."
    reply = query_groq(validation_prompt).lower()
    return "yes" in reply

# === Save Data ===
def save_candidate_info(info: dict):
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(info)
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# === PDF Export ===
def export_pdf(candidate_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Candidate Interview Summary", ln=True, align='C')
    pdf.ln(10)

    for key, value in candidate_info.items():
        if isinstance(value, list):
            pdf.multi_cell(0, 10, txt=f"{key}:\n" + "\n".join(value))
        else:
            pdf.multi_cell(0, 10, txt=f"{key}: {value}")
        pdf.ln(5)

    pdf.output("candidate_summary.pdf")

# === Streamlit Frontend ===
st.set_page_config(page_title="TalentScout Hiring Assistant")
st.title("TalentScout - Hiring Assistant")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'form_step' not in st.session_state:
    st.session_state.form_step = 0
    st.session_state.candidate_info = {
        "Full Name": "",
        "Email Address": "",
        "Phone Number": "",
        "Years of Experience": "",
        "Desired Position(s)": "",
        "Current Location": "",
        "Tech Stack": ""
    }

if 'conversation_ended' not in st.session_state:
    st.session_state.conversation_ended = False

if 'question_step' not in st.session_state:
    st.session_state.question_step = 0

info_fields = list(st.session_state.candidate_info.keys())

# Input area
if not st.session_state.conversation_ended:
    user_input = st.chat_input("Say something to the assistant...")
else:
    user_input = None

if user_input:
    if any(kw in user_input.lower() for kw in ["bye", "exit", "quit", "thank you", "byy"]):
        bot_reply = query_groq(END_PROMPT)
        st.session_state.chat_history.append((user_input, bot_reply))
        st.session_state.conversation_ended = True

    else:
        step = st.session_state.form_step

        if step == 0:
            greeting = query_groq(GREETING)
            st.session_state.chat_history.append((user_input, greeting))
            st.session_state.form_step += 1
            next_field = info_fields[0]
            bot_reply = f"Can you please tell me your {next_field}?"
            st.session_state.chat_history.append(("", bot_reply))

        elif step <= len(info_fields):
            field = info_fields[step - 1]
            st.session_state.candidate_info[field] = user_input
            st.session_state.chat_history.append((user_input, f"Thanks for your {field}!"))

            if step < len(info_fields):
                next_field = info_fields[step]
                bot_reply = f"Can you please tell me your {next_field}?"
                st.session_state.chat_history.append(("", bot_reply))
                st.session_state.form_step += 1
            else:
                tech_stack = st.session_state.candidate_info["Tech Stack"]
                if not is_valid_tech_stack(tech_stack):
                    st.session_state.chat_history.append(("", f"❌ '{tech_stack}' is not a valid tech stack. Please try again with something like Python + Django, Java + Spring, etc.\n\nCan you please re-enter your Tech Stack?"))
                    st.session_state.form_step -= 1
                else:
                    question_prompt = QUESTION_GENERATION_TEMPLATE.format(tech_stack=tech_stack)
                    questions = query_groq(question_prompt)
                    question_lines = [q.strip() for q in questions.split('\n') if q.strip() and q.strip()[0].isdigit()]
                    st.session_state.generated_questions = question_lines[:5]
                    st.session_state.answers = []
                    st.session_state.question_step = 0
                    bot_reply = f"✅ Thanks! Based on your tech stack, here are your questions:\n\n{chr(10).join(st.session_state.generated_questions)}\n\nPlease answer question 1:"
                    st.session_state.chat_history.append(("", bot_reply))
                    st.session_state.form_step += 1

        elif 'generated_questions' in st.session_state and st.session_state.question_step < len(st.session_state.generated_questions):
            if len(user_input.strip()) < 10:
                bot_reply = f"❌ Your answer seems too short. Please provide a more detailed answer to question {st.session_state.question_step + 1}."
                st.session_state.chat_history.append((user_input, bot_reply))
            else:
                st.session_state.answers.append(user_input)
                st.session_state.chat_history.append((user_input, f"Answer saved for question {st.session_state.question_step + 1}."))

                st.session_state.question_step += 1
                if st.session_state.question_step < len(st.session_state.generated_questions):
                    bot_reply = f"Please answer question {st.session_state.question_step + 1}:"
                    st.session_state.chat_history.append(("", bot_reply))
                else:
                    bot_reply = "Thanks! All your answers have been recorded. Our team will get back to you soon. 😊"
                    st.session_state.chat_history.append(("", bot_reply))
                    st.session_state.conversation_ended = True

                    st.session_state.candidate_info["Technical Answers"] = st.session_state.answers
                    save_candidate_info(st.session_state.candidate_info)
                    export_pdf(st.session_state.candidate_info)

                    with open("candidate_summary.pdf", "rb") as f:
                        st.download_button("📄 Download Your Interview Summary", f, file_name="candidate_summary.pdf", mime="application/pdf")

# Chat display
for user_msg, bot_msg in st.session_state.chat_history:
    if user_msg:
        st.chat_message("user").write(user_msg)
    if bot_msg:
        st.chat_message("assistant").write(bot_msg)

if st.session_state.conversation_ended:
    st.info("Conversation ended. Refresh the page to restart.")
