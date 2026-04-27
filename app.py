import streamlit as st
import time
import random
from questions import QUESTIONS

st.set_page_config(page_title="Apple Dev Academy Prep", page_icon="🍎")

@st.cache_data
def get_random_questions(all_questions):
    selected_questions = {}
    quota = {
        "Section 1: Logic": 25,
        "Section 2: Programming (Swift Focus)": 15,
        "Section 3: OOP": 10,
        "Section 4: Bonus Question": 2
    }
    
    for section, limit in quota.items():
        if section in all_questions:
            sample_size = min(len(all_questions[section]), limit)
            selected_questions[section] = random.sample(all_questions[section], sample_size)
            
    return selected_questions

if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = get_random_questions(QUESTIONS)
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

st.title("🍎 Apple Developer Academy - Simulation Test")
st.markdown("---")

duration = 60 * 45 
elapsed = time.time() - st.session_state.start_time
remaining = max(0, int(duration - elapsed))

st.sidebar.header("⏱️ Timer")
st.sidebar.subheader(f"{remaining // 60} menit {remaining % 60} detik")

if remaining <= 0:
    st.error("Waktu Habis! Silakan tekan tombol submit.")

with st.form("exam_form"):
    for section, q_list in st.session_state.selected_questions.items():
        st.header(section)
        for i, q_item in enumerate(q_list):
            q_key = f"{section}_{i}"
            st.write(f"**{i+1}. {q_item['q']}**")
            
            user_choice = st.radio(
                "Pilih jawaban:", 
                q_item['options'], 
                key=q_key,
                index=None
            )
            st.session_state.answers[q_key] = user_choice
            st.write("")

    submitted = st.form_submit_button("Submit Jawaban")

if submitted:
    correct_count = 0
    total_questions = sum(len(v) for v in st.session_state.selected_questions.values())
    st.divider()
    st.header("📊 Hasil Tes Anda")
    
    for section, q_list in st.session_state.selected_questions.items():
        for i, q_item in enumerate(q_list):
            q_key = f"{section}_{i}"
            user_answer = st.session_state.answers.get(q_key)
            
            if user_answer == q_item['answer']:
                correct_count += 1
            else:
                with st.expander(f"Cek pembahasan {section} No {i+1}"):
                    st.write(f"Jawabanmu: {user_answer}")
                    st.write(f"Jawaban benar: :green[{q_item['answer']}]")

    score_final = (correct_count / total_questions) * 100
    
    col1, col2 = st.columns(2)
    col1.metric("Skor Akhir", f"{score_final:.2f}%")
    col2.metric("Benar", f"{correct_count} / {total_questions}")

    if score_final >= 75:
        st.balloons()
        st.success("Luar biasa! Peluang kamu lolos sangat besar.")
    else:
        st.warning("Terus latihan ya, fokus pada bagian yang salah.")