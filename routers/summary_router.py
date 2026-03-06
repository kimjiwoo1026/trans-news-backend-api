from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os


class SummarizerService:

    def __init__(self):

        model_dir = "lcw99/t5-base-korean-text-summary"

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    def summarize(self, text, model="t5"):

        if model == "openai":

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "뉴스 기사를 간단히 요약해라"},
                    {"role": "user", "content": text}
                ]
            )

            return response.choices[0].message.content.strip()


        elif model == "t5":

            inputs = self.tokenizer(
                [text],
                max_length=2048,
                truncation=True,
                return_tensors="pt",
                padding=True
            )

            output = self.model.generate(
                **inputs,
                num_beams=16,
                max_length=128
            )

            decoded = self.tokenizer.batch_decode(
                output,
                skip_special_tokens=True
            )[0]

            return decoded.strip()