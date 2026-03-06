from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import openai
import google.generativeai as genai
import os


class SummarizerService:

    def __init__(self):

        model_dir = "lcw99/t5-base-korean-text-summary"

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

        openai.api_key = os.getenv("OPENAI_API_KEY")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.gemini_model = genai.GenerativeModel("gemini-pro")

    def summarize(self, text: str, model: str = "t5"):

        if model == "t5":

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
                do_sample=False,
                min_length=1,
                max_length=128
            )

            decoded = self.tokenizer.batch_decode(
                output,
                skip_special_tokens=True
            )[0]

            return decoded.strip()

        elif model == "openai":

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "다음 뉴스를 3줄로 요약해라"},
                    {"role": "user", "content": text}
                ]
            )

            return response.choices[0].message.content

        elif model == "gemini":

            response = self.gemini_model.generate_content(
                f"다음 뉴스를 3줄로 요약해라:\n{text}"
            )

            return response.text