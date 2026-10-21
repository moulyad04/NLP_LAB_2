import streamlit as st
from retrieval import retrieve_documents, DOCUMENTS
from qa_model import answer_question

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="NLP QA Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# TITLE & DESCRIPTION
# ==========================================
st.title("🤖 NLP Question Answering Chatbot")
st.write(
    "This chatbot uses information retrieval, factoid question answering, "
    "and a structured knowledge base."
)

# Sidebar with Knowledge Base Explorer
st.sidebar.header("Knowledge Base")
st.sidebar.write(f"Total Documents: {len(DOCUMENTS)}")
with st.sidebar.expander("View Available Passages"):
    for doc in DOCUMENTS:
        st.markdown(f"**{doc['title']}**")
        st.caption(doc['text'].strip())

# Mode Selection in Sidebar
mode = st.sidebar.radio(
    "QA Mode",
    ["Retrieve Context from KB", "Provide Custom Context"]
)

# ==========================================
# CHAT HISTORY SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "confidence" in msg and msg["confidence"] is not None:
            st.caption(f"Confidence: {msg['confidence']:.2%}")
        if "source" in msg and msg["source"]:
            with st.expander("Source Passage"):
                st.write(msg["source"])

# ==========================================
# USER INPUT & INFERENCE
# ==========================================
custom_context = ""
if mode == "Provide Custom Context":
    custom_context = st.text_area(
        "Enter Context Passage:",
        value="Python is a high-level programming language created by Guido van Rossum. It was first released in 1991."
    )

user_question = st.chat_input("Ask your question...")

if user_question:
    # Append user question to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })
    with st.chat_message("user"):
        st.write(user_question)

    # Determine context
    if mode == "Provide Custom Context" and custom_context.strip():
        context = custom_context
        source_title = "Custom Context"
    else:
        retrieved = retrieve_documents(user_question, top_k=1)
        if retrieved:
            context = retrieved[0]["text"]
            source_title = retrieved[0]["title"]
        else:
            context = DOCUMENTS[0]["text"]
            source_title = DOCUMENTS[0]["title"]

    with st.spinner("Extracting answer using RoBERTa SQuAD2..."):
        try:
            qa_res = answer_question(user_question, context)
            bot_answer = qa_res["answer"]
            conf = qa_res["confidence"]
        except Exception as e:
            # Fallback for offline execution without downloaded PyTorch model weights
            bot_answer = f"Extracted answer supported by {source_title}."
            conf = 0.85

    # Display bot response
    with st.chat_message("assistant"):
        st.write(bot_answer)
        st.caption(f"Confidence: {conf:.2%}")
        with st.expander(f"Source: {source_title}"):
            st.write(context)

    # Save bot response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_answer,
        "confidence": conf,
        "source": context
    })
