import streamlit as st
import requests

st.title("🤝 Your Personal Assistant")

st.subheader("What can your personal assistant do?")

st.markdown("""
1. Answer questions on various topics.
2. Arrange Calendar events and meetings.
3. Read your emails and send replies, can even summarize them for you.
4. Manage your tasks and to-do lists.
5. Take quick notes for you.
6. Track your expenses and budgeting.
""")

st.subheader("💬 Chat with your assistant")

webhook_url = "--Your webhook url"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input()

if user_message:

    with st.chat_message("user"):
        st.markdown(user_message)

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    webhook_url,
                    json={"message": user_message},
                    timeout=60
                )

                if response.status_code == 429:
                    ai_response = "⚠️ You've reached your AI usage limit. Please try again later."

                elif response.status_code >= 500:
                    ai_response = "⚠️ Our AI assistant is temporarily unavailable due to a technical issue. Please try again later."

                elif response.status_code != 200:
                    ai_response = "⚠️ Something went wrong while processing your request. Please try again."

                else:
                    data = response.json()

                    if isinstance(data, list) and len(data) > 0:
                        ai_response = data[0].get(
                            "output",
                            "⚠️ No response received from the AI assistant."
                        )

                    elif isinstance(data, dict):
                        ai_response = data.get(
                            "output",
                            "⚠️ No response received from the AI assistant."
                        )

                    else:
                        ai_response = "⚠️ The AI assistant returned an empty response."

            except requests.exceptions.Timeout:
                ai_response = "⏳ The AI assistant is taking too long to respond. Please try again."

            except requests.exceptions.ConnectionError:
                ai_response = "🔌 Unable to connect to the AI server. Please check whether n8n is running."

            except requests.exceptions.RequestException:
                ai_response = "⚠️ Unable to communicate with the AI server. Please try again later."

            except Exception:
                ai_response = "⚠️ Something unexpected happened. Please try again later."

        st.markdown(ai_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })
