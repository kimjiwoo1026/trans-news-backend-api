import os
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class SummarizerService:

    def __init__(self):

        self.model_type = os.getenv("SUMMARY_MODEL", "t5")

        if self.model_type == "openai":

            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        else:

            model_dir = "lcw99/t5-base-korean-text-summary"

            self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

            self.max_input_length = 2048


    def summarize(self, text, max_length=128):

        if self.model_type == "openai":

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "다음 뉴스 기사를 간결하게 요약하라."},
                    {"role": "user", "content": text}
                ]
            )

            return response.choices[0].message.content.strip()

        else:

            inputs = self.tokenizer(
                [text],
                max_length=self.max_input_length,
                truncation=True,
                return_tensors="pt",
                padding=True
            )

            output = self.model.generate(
                **inputs,
                num_beams=16,
                do_sample=False,
                min_length=1,
                max_length=max_length
            )

            decoded = self.tokenizer.batch_decode(
                output,
                skip_special_tokens=True
            )[0]

            return decoded.strip()