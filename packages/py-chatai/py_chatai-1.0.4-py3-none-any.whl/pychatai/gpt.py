import openai

class GPT:
    def __init__(self, api_key: str):
        """
        Initializes the GPT class with an OpenAI API key.
        """
        self.api_key = api_key
        openai.api_key = api_key

    def ask_from_input(self, prompt_message: str = "Ask a question to the AI: ", model: str = "gpt-3.5-turbo"):
        """
        Prompts the user for a question, sends it to the OpenAI API, and returns the response.

        Parameters:
        - prompt_message (str): The message to display when asking for input.
        - model (str): The OpenAI model to use (default: gpt-3.5-turbo).

        Returns:
        - str: The AI's response or an error message.
        """
        try:
            question = input(prompt_message)
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": question}],
            )
            return response['choices'][0]['message']['content']
        except openai.error.AuthenticationError:
            return "Authentication error: Please check your API key."
        except openai.error.RateLimitError:
            return "Rate limit exceeded: You have made too many requests. Please try again later."
        except openai.error.APIConnectionError:
            return "Connection error: Failed to connect to the OpenAI API."
        except openai.error.OpenAIError as e:
            return f"An error occurred: {e}"

# Main script
if __name__ == "__main__":
    # Replace with your OpenAI API key
    api_key = "your_openai_api_key"
    
    if not api_key:
        print("Error: Please provide a valid OpenAI API key in the script.")
    else:
        gpt = GPT(api_key)
        response = gpt.ask_from_input()
        print("AI Response:", response)
        