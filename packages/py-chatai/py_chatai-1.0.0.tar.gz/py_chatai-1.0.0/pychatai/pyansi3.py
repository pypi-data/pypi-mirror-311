import openai

class GPT:
    def __init__(self, api_key: str):
        """
        Initializes the GPT class with an OpenAI API key.
        """
        self.api_key = api_key
        openai.api_key = api_key

    def ask_from_input(self, prompt_message: str = "Ask your question: ", model: str = "gpt-3.5-turbo"):
        """
        Prompts the user for a question, sends it to the OpenAI API, and returns the response.

        Parameters:
        - prompt_message (str): The message to display when asking for input.
        - model (str): The OpenAI model to use (default: gpt-3.5-turbo).

        Returns:
        - str: The AI's response.
        """
        try:
            question = input(prompt_message)
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": question}],
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"An error occurred: {e}"
            