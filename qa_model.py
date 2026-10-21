# ============================================================
# Transformer-Based Extractive Question Answering Module
# Model: deepset/roberta-base-squad2
# ============================================================

import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

MODEL_NAME = "deepset/roberta-base-squad2"

_tokenizer = None
_model = None

def load_qa_model():
    """Load pretrained RoBERTa SQuAD2 model and tokenizer."""
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        print(f"Loading QA model: {MODEL_NAME}...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForQuestionAnswering.from_pretrained(MODEL_NAME)
        print("QA model loaded successfully!")
    return _tokenizer, _model


def answer_question(question, context):
    """
    Extract relevant answer span from context using RoBERTa SQuAD2 model.
    Returns: dict with 'answer' and 'confidence' score.
    """
    tokenizer, model = load_qa_model()

    inputs = tokenizer(
        question,
        context,
        return_tensors="pt",
        truncation=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    start_index = torch.argmax(start_scores).item()
    end_index = torch.argmax(end_scores).item()

    # Calculate confidence score via softmax probabilities
    start_probs = torch.softmax(start_scores, dim=1)[0]
    end_probs = torch.softmax(end_scores, dim=1)[0]
    confidence = float(start_probs[start_index] * end_probs[end_index])

    if end_index < start_index:
        end_index = start_index

    answer_tokens = inputs["input_ids"][0][start_index:end_index + 1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True).strip()

    if not answer:
        answer = "I could not find an answer in the provided context."
        confidence = 0.0

    return {
        "question": question,
        "context": context,
        "answer": answer,
        "confidence": round(confidence, 4)
    }


if __name__ == "__main__":
    context = (
        "Python is a high-level programming language created by Guido van Rossum. "
        "It was first released in 1991."
    )
    q1 = "Who created Python?"
    res1 = answer_question(q1, context)
    print("Question:", q1)
    print("Answer:", res1["answer"])
    print("Confidence:", res1["confidence"])
    print("-" * 40)

    q2 = "When was Python first released?"
    res2 = answer_question(q2, context)
    print("Question:", q2)
    print("Answer:", res2["answer"])
    print("Confidence:", res2["confidence"])
