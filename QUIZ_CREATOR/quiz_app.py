import streamlit as st
import ollama
from PyPDF2 import PdfReader

# =========================
# Custom Dark + Neon CSS
# =========================
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    .main {
        background-color: #0f0f0f;
    }
    h1, h2, h3 {
        color: #00FFAA !important;
    }
    .stMarkdown p {
        color: #f0f0f0 !important;
        font-size: 18px;
    }
    /* Radio button labels */
    div[data-baseweb="radio"] label {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    /* Selected option */
    div[data-baseweb="radio"] input:checked + div > div {
        color: #00FFAA !important;
        font-weight: 700 !important;
    }
    /* Buttons */
    button[kind="primary"] {
        background-color: #00FFAA !important;
        color: black !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)


# =========================
# Helper Functions
# =========================
def extract_text_from_pdf(pdf_file):
    """Extract all text from uploaded PDF"""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def generate_quiz_from_text(text, num_questions=5):
    """Generate quiz questions using Ollama"""
    prompt = f"""
    Please generate {num_questions} multiple-choice questions from the following text.
    For each question, give 4 options (A, B, C, D) and mark the correct option with "(Correct)".
    
    Text:
    {text}
    """
    response = ollama.chat(
        model="llama3",  # make sure you've pulled this model: ollama pull llama3
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']


# =========================
# Streamlit UI
# =========================
st.title("Hackathon Quiz Generator")
st.write("Upload a PDF and get auto-generated MCQs with a sleek UI.")

# File uploader
uploaded_file = st.file_uploader(" Upload your PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Generating quiz questions..."):
        quiz_text = generate_quiz_from_text(pdf_text)

    # Display quiz
    st.header(" Quiz Time")
    questions = quiz_text.split("\n\n")

    for i, q in enumerate(questions):
        if not q.strip():
            continue
        st.markdown(f"**Q{i+1}. {q.splitlines()[0]}**")

        # Extract options
        options = [line for line in q.splitlines()[1:] if line.strip()]
        clean_options = [opt.replace("(Correct)", "").strip() for opt in options]

        # Show as radio button
        user_choice = st.radio(
            f"Choose your answer for Q{i+1}",
            clean_options,
            key=f"q{i}"
        )

        # Reveal correct answer
        correct_option = [opt for opt in options if "(Correct)" in opt]
        if correct_option:
            if st.button(f"Check Answer Q{i+1}", key=f"check{i}"):
                if user_choice.strip() in correct_option[0]:
                    st.success(" Correct!")
                else:
                    st.error(f"Wrong. Correct answer: {correct_option[0].replace('(Correct)','').strip()}")
