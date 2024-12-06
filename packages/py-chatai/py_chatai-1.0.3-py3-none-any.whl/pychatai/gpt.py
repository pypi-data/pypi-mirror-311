import openai

class GPT:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def ask_from_input(self, prompt_message: str = "Ask your question: ", model: str = "gpt-3.5-turbo"):
        try:
            question = input(prompt_message)
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": question}],
            )
            return response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            return f"An error occurred: {e}"
            