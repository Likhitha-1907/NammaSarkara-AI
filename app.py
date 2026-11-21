
import streamlit as st

from agent.scheme_agent import ask_agent
from src.eligibility_checker import check_pm_kisan_eligibility
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
    ["English", "Hindi", "Kannada"]
)
# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input(
    "Ask about government schemes..."
)

if question:

    # Display user's question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("NammaSarkara AI is thinking..."):

            try:
                answer = ask_agent(
                    question,
                    language
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(
                    "Something went wrong. Please try again."
                )
                print("Agent error:", error)
            st.divider()

st.subheader("🌾 PM-KISAN Eligibility Checker")

st.write(
    "Answer a few questions to get a preliminary "
    "assessment of your PM-KISAN eligibility."
)

if st.button("Check PM-KISAN Eligibility"):

    st.session_state.show_eligibility = True

if st.session_state.get("show_eligibility", False):

    st.info(
        "This is a preliminary assessment. "
        "Final eligibility is decided by government authorities."
    )

    profile = {}

    profile["has_cultivable_land"] = st.selectbox(
        "Does your farmer family have cultivable land recorded in its name?",
        ["Not sure", "Yes", "No"]
    )

    questions = {
        "institutional_landholder": "Is the land held by an institution?",
        "constitutional_post": "Does a family member fall under an excluded constitutional post category?",
        "political_position": "Does a family member fall under an excluded political category?",
        "government_employee": "Does a family member belong to an excluded government employment category?",
        "pension_10000_or_more": "Does a family member receive an excluded government pension of ₹10,000 or more per month?",
        "income_tax_payer": "Did a family member pay income tax in the last assessment year?",
        "practising_professional": "Is a family member an excluded practising registered professional?",
        "nri_family": "Does the farmer family fall under the NRI exclusion?",
        "land_acquired_after_cutoff": "Was ownership of the agricultural land transferred after 1 February 2019?"
    }

    for field, question_text in questions.items():
        profile[field] = st.selectbox(
            question_text,
            ["Not sure", "Yes", "No"],
            key=field
        )

    if profile["land_acquired_after_cutoff"] == "Yes":
        profile["land_transfer_due_to_death"] = st.selectbox(
            "Was the land transferred because the previous landowner passed away?",
            ["Not sure", "Yes", "No"],
            key="land_transfer_due_to_death"
        )
    else:
        profile["land_transfer_due_to_death"] = False

    if st.button("Submit Eligibility Assessment"):

        converted_profile = {
            key: (
                None if value == "Not sure"
                else True if value == "Yes"
                else False if value == "No"
                else value
            )
            for key, value in profile.items()
        }

        result = check_pm_kisan_eligibility(converted_profile)

        st.subheader("Your Assessment Result")

        if result["status"] == "POTENTIALLY ELIGIBLE":
            st.success(result["status"])

        elif result["status"] == "NOT ELIGIBLE":
            st.error(result["status"])

        else:
            st.warning(result["status"])

        st.write(result["reason"])

        if "missing_fields" in result:
            st.write("Missing information:", result["missing_fields"])
