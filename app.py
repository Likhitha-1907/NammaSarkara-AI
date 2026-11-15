
import streamlit as st

st.set_page_config(
    page_title="NammaSarkara AI",
    page_icon="🇮🇳",
    layout="centered"
)

st.title("🇮🇳 NammaSarkara AI")

st.subheader("Your guide to government schemes")

st.write(
    "Discover government schemes, understand eligibility "
    "and learn how to apply."
)

st.info(
    "Our mission is to make government scheme information "
    "simple and accessible to every citizen."
)

st.divider()

st.subheader("How can we help you?")

language = st.selectbox(
    "Choose your preferred language",
    ["English", "Hindi"]
)

question = st.text_input(
    "Ask your question",
    placeholder="Example: Are there scholarships for students?"
)

if st.button("Submit"):
    if question.strip():
        st.success("Thank you! Your question has been received.")
        st.write("Selected language:", language)
        st.info("Scheme search and AI assistance will be added in the next development stages.")
    else:
        st.warning("Please enter your question first.")
