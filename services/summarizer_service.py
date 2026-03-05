from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="lcw99/t5-base-korean-text-summary"
)

def summarize_text(text: str):

    if len(text) < 50:
        return text

    result = summarizer(
        text,
        max_length=120,
        min_length=40,
        do_sample=False
    )

    return result[0]["summary_text"]