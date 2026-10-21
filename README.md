# Department of AIML — Advance NLP (AML23702)
## Lab Exercise 2: Question Answering Chatbot Using Transformer-Based QA Model

**Student Name:** MOULYA D  
**USN:** 1GA23AI026  
**Repository:** [moulyad04/NLP_LAB_2](https://github.com/moulyad04/NLP_LAB_2)

---

### Project Overview
This project designs and implements an interactive transformer-based Question Answering (QA) chatbot. The system accepts a natural-language query and a knowledge-base context, retrieves relevant passages, extracts the most relevant answer span using the pretrained `deepset/roberta-base-squad2` model, calculates a confidence score, and presents the response through a Streamlit web interface.

### Key Features
- **Extractive QA Inference:** Tokenizes question-context pairs and predicts start/end token logits via `AutoModelForQuestionAnswering`.
- **Confidence Estimation:** Computes prediction probabilities via softmax over logits.
- **Information Retrieval:** Lexical scoring over a multi-document factual knowledge base.
- **Interactive UI:** Streamlit chatbot frontend with message history, confidence indicators, and expandable source passages.
- **Public Tunneling:** Compatible with `ngrok` / `localtunnel` for remote demonstration.

---

### System Architecture
```
+-----------------------+
|  Streamlit Frontend   |
|     User Question     |
+-----------+-----------+
            |
            v
+-----------+-----------+
|  Question + Context   |
+-----------+-----------+
            |
            v
+-----------+-----------+
| RoBERTa SQuAD2 Model  |
| Answer Span Prediction|
+-----------+-----------+
            |
            v
+-----------+-----------+
|  Answer + Confidence  |
+-----------+-----------+
            |
            v
+-----------+-----------+
| Streamlit Answer View |
+-----------------------+
```

---

### Installation & Execution

#### 1. Setup Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 2. Run Retrieval Test
```bash
python retrieval.py
```

#### 3. Run QA Model Test
```bash
python qa_model.py
```

#### 4. Launch Streamlit Chatbot
```bash
streamlit run app.py
```

---

### Repository Structure
- `app.py`: Streamlit interactive chatbot application.
- `qa_model.py`: RoBERTa SQuAD2 extractive question-answering logic and confidence scoring.
- `retrieval.py`: Information retrieval system over knowledge base documents.
- `NLP_2.ipynb`: Executed Jupyter/Colab notebook for demonstration and grading.
- `screenshots/`: Interface screenshots and terminal output.
- `requirements.txt`: Python dependencies.
