from typing import List, Optional
import nltk
import logging
import warnings
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
# Suppress NLTK logs and warnings
logging.getLogger('nltk').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="nltk")

from nltk.tokenize import word_tokenize
from nltk import pos_tag

class GoogleGenAI:
    """
    A customizable class to interact with Gemini AI for conversational and generative tasks.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-1.5-flash",
        ai_tag: str = "AI: ",
        hidden_instructions: Optional[List[str]] = None,
        verbose: bool = False
    ):
        """
        Initializes the GenAI instance.

        Args:
            api_key (str): API key for Gemini AI.
            model_name (str): AI model name. Defaults to "gemini-1.5-flash".
            ai_tag (str): Tag to prefix AI responses with. Defaults to "AI: ".
            hidden_instructions (Optional[List[str]]): Predefined instructions for the AI.
            verbose (bool): If True, logs additional debug information. Defaults to False.
        """
        import google.generativeai as genai

        if hidden_instructions is None:
            hidden_instructions = [
                "Role: Chatbot",
                "Response: Concise and helpful. No emojis, no text formatting.",
                "[\u2714] = Do not answer; [?] = Answer only when prompted."
            ]

        self.api_key = api_key
        self.model_name = model_name
        self.ai_tag = ai_tag
        self.history_file = 'conversation_history.txt'
        self.user_info_file = 'master-info.txt'
        self.hidden_instructions = hidden_instructions
        self.verbose = verbose

        # Configure AI model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)

        # Initialize conversation history file
        with open(self.history_file, 'w', encoding='utf-8') as file:
            file.write("\n".join(self.hidden_instructions) + "\n")

        with open(self.user_info_file, 'w', encoding='utf-8') as file:
            file.write("MASTER-INFO: ")


    def log(self, message: str) -> None:
        """Logs messages if verbosity is enabled."""
        if self.verbose:
            print(f"[DEBUG] {message}")

    def enterTempChat(self) -> str:
        """
        Starts an interactive chat session with the AI, maintaining context within the function.

        Returns:
            str: Final conversation history as a string.
        """
        conversation_history = self.hidden_instructions[:]
        conversation_transcript = []

        while True:
            user_input = input("You: ")

            if user_input.strip().lower() == "exit":
                break

            conversation_history.append(f"User: {user_input}[?]")
            prompt = "\n".join(conversation_history)

            try:
                response = self.model.generate_content(prompt)
                if response and hasattr(response, 'text') and response.text:
                    ai_response = response.text.replace("**", "").strip()
                    conversation_history.append(f"{self.ai_tag}{ai_response}")
                    conversation_transcript.append(f"You: {user_input}\n{self.ai_tag}{ai_response}")
                else:
                    conversation_transcript.append(f"You: {user_input}\n{self.ai_tag}I'm sorry, I couldn't generate a response.")
            except Exception as e:
                error_message = f"An error occurred: {e}"
                self.log(error_message)
                conversation_transcript.append(f"You: {user_input}\n{self.ai_tag}{error_message}")

        return "\n".join(conversation_transcript)

    def addInteractPermChat(self, user_input: str) -> str:
        """
        Processes a single chat interaction while maintaining conversational context externally.

        Args:
            user_input (str): The user's input message.

        Returns:
            str: The AI's response.
        """

        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

        tokens = word_tokenize(user_input)
        tagged_tokens = pos_tag(tokens)
        subject = ""

        for word, tag in tagged_tokens:
            if tag in ["NN", "NNS", "NNP", "NNPS"]:  # Noun or Proper Noun
                subject = word
                break

        try:
            # Record user input in the history file with [?], indicating it's pending an answer
            with open(self.history_file, 'a+', encoding='utf-8') as file:
                file.write(f"\nMaster: {user_input}[?]")

            # Read the entire conversation history to maintain context
            with open(self.history_file, 'r', encoding='utf-8') as file:
                conversation_history = file.readlines()

            # Generate a response using the model (just for processing context)
            response = self.model.generate_content(f"\n{conversation_history}")
            if response and hasattr(response, 'text') and response.text:
                ai_response = response.text.replace("**", "").strip()

                # Update history: Mark the last question (ending with [?]) as answered [\u2714]
                with open(self.history_file, 'r+', encoding='utf-8') as file:
                    lines = file.readlines()
                    for i in range(len(lines) - 1, -1, -1):
                        if lines[i].startswith("Master:") and "[?]" in lines[i]:
                            lines[i] = lines[i].replace("[?]", "[\u2714]")  # Only mark the most recent question
                            break  # Exit loop after updating the most recent question
                    # Write the updated lines back to the file
                    file.seek(0)
                    file.writelines(lines)
                    file.write(f"\n{self.ai_tag} {ai_response}")

                # Return the AI's response
                return ai_response

            else:
                return "I'm sorry, I couldn't generate a response."

        except Exception as e:
            error_message = f"Error in addInteractPermChat: {e}"
            self.log(error_message)
            return "An error occurred while generating a response."

    # The rest of the class remains unchanged


    def imgPrompt(self, imagePath, prompt, img_format="JPEG", quality=75):
        """
        Resizes the image, compresses it to reduce size, encodes it to base64, and sends it with a text prompt to the Gemini model.

        Args:
            imagePath: The path to the image file.
            prompt: The text prompt to use for generating text.
            img_format: The image format to use for saving (JPEG or PNG). Default is JPEG.
            quality: The compression quality for JPEG (1 to 100). Default is 75.

        Returns:
            The generated text response from the Gemini model.
        """
        import base64
        from PIL import Image
        import io

        try:
            # Resize the image and save it to a byte array with compression
            with Image.open(imagePath) as img:
                img.thumbnail((1024, 1024))  # Resize while maintaining aspect ratio
                byte_io = io.BytesIO()

                if img_format == "JPEG":
                    # Save as JPEG with specified quality to reduce size
                    img.save(byte_io, format='JPEG', quality=quality)
                elif img_format == "PNG":
                    # Save as PNG (lossless compression, may be better for images with transparency)
                    img.save(byte_io, format='PNG')
                else:
                    raise ValueError("Unsupported image format. Use 'JPEG' or 'PNG'.")

                image_data = byte_io.getvalue()

            # Encode the image to base64
            imageData = base64.b64encode(image_data).decode("utf-8")
            print(imageData)

            # Create and send the prompt with the image data
            full_prompt = f"[Image]\n{imageData}\n[/Image]\n{prompt}"

            # Generate response from the model
            response = self.model.generate_content(full_prompt)

            # Extract and clean response content
            if response and hasattr(response, 'candidates') and response.candidates:
                response_text = response.candidates[0].content.parts[0].text.strip()  # Get the generated text
                return response_text
            else:
                return "No valid response generated."

        except (FileNotFoundError, IOError) as e:
            print(f"Error opening image file: {e}")
            return "Error with the image file."

        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred during processing."

    def generate(self, prompt: str) -> str:
        """
        Generates a single AI response for a given prompt.

        Args:
            prompt (str): The input prompt for the AI.

        Returns:
            str: The generated response from the AI.
        """
        try:
            response = self.model.generate_content(prompt)  # Replace with actual method
            if response and hasattr(response, 'text') and response.text:
                # Clean and format the text
                formatted_response = response.text.strip().replace("**", "").replace(". ", ".\n")
                return formatted_response
            else:
                return "I'm sorry, I couldn't generate a response."
        except Exception as e:
            # Log the error for debugging
            error_message = f"Error in generate_response: {e}"
            self.log(error_message)
            return "An error occurred while generating a response."

# Example usage
if __name__ == "__main__":
    bot = GoogleGenAI(
        api_key="AIzaSyCuiNF8S4HbWKV60namJumCUJLaTI6e3mA",
        model_name="gemini-1.5-flash",
        ai_tag="GenAI: ",
        verbose=True
    )
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print(bot.addInteractPermChat(user_input))
    # image_path = "example.png"  # Replace with your image file path
    # prompt = "Describe the content of this image."
    #
    # # Call the image_and_prompt method and print the response
    # response = bot.imgPrompt(image_path, prompt, img_format="PNG")
    # print(response)
