from huggingface_hub import InferenceClient
import os
import re

def generateImg(prompt: str, location: str = "AiGenImgs", inferenceToken: str = os.getenv('HUGGINGFACE_IMG_TOKEN')):
    """
    Generate an image from a text prompt and save it to a specified directory with the prompt as the image name.

    Args:
        prompt (str): The prompt text to generate the image.
        location (str): The location (directory) where you wish your images to be saved. Default is 'AiGenImgs'.
        inferenceToken (str): The Hugging Face inference token. Pass it directly or use an environment variable.

    Raises:
        ValueError: If the inferenceToken is None or empty.
    """
    # Validate the inference token
    if not inferenceToken:
        raise ValueError(
            "Invalid token: The 'inferenceToken' is None or empty. "
            "Issue 'might' even persist if token is stored as an environment variable (returns None). "
        )

    # Ensure the output directory exists
    os.makedirs(location, exist_ok=True)

    # Initialize the Hugging Face inference client
    client = InferenceClient("black-forest-labs/FLUX.1-schnell", token=inferenceToken)

    # Generate the image using the given prompt
    try:
        image = client.text_to_image(prompt)
    except Exception as e:
        raise RuntimeError(f"Error generating image: {e}")

    # Sanitize the prompt to create a valid filename
    sanitized_prompt = re.sub(r'[^\w\s-]', '_', prompt).strip().replace(" ", "_")
    output_filename = f"{sanitized_prompt}.jpeg"
    output_path = os.path.join(location, output_filename)

    # Save the image to the specified directory
    try:
        image.save(output_path)
    except Exception as e:
        raise RuntimeError(f"Error saving image to '{output_path}': {e}")

    print(f"Image successfully saved to: {output_path}")

if __name__ == "__main__":
    generateImg(input("Image prompt: "), inferenceToken="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")
