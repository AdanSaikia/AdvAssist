import os
import base64
from PIL import Image
from huggingface_hub import InferenceClient


def imgVQA(imgPath: str, query: str, inferenceToken: str = os.getenv('HUGGINGFACE_IMG_TOKEN')) -> str:
    """
    Args:
        imgPath (str): The path of the local image.
        query (str): Your visual question for the given image.
        inferenceToken (str): The Hugging Face inference token. Pass it directly or use an environment variable.

    Returns:
        str: The answer to the visual question.

    Raises:
        ValueError: If the inferenceToken is None or empty.
        RuntimeError: If the API call fails.
    """

    # Validate the inference token
    if not inferenceToken:
        raise ValueError(
            "Invalid token: The 'inferenceToken' is None or empty. "
            "Ensure the token is passed as an argument or set as an environment variable."
        )

    # Get the filename without extension for better context
    filename = os.path.basename(imgPath)
    filename_without_extension = os.path.splitext(filename)[0]

    # Resize the image to 1024p (if necessary) and save it as tmp_vqa_img in the cache folder
    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)
    resized_image_path = os.path.join(cache_dir, "tmp_vqa_img.jpg")

    with Image.open(imgPath) as img:
        width, height = img.size
        if width > 1024 or height > 1024:
            aspect_ratio = width / height
            if aspect_ratio > 1:  # Landscape
                new_width = 1024
                new_height = int(new_width / aspect_ratio)
            else:  # Portrait or square
                new_height = 1024
                new_width = int(new_height * aspect_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img.save(resized_image_path)
        else:
            img.save(resized_image_path)

    # Perform the VQA using Hugging Face Inference API
    client = InferenceClient(model="meta-llama/Llama-3.2-11B-Vision-Instruct", token=inferenceToken)

    with open(resized_image_path, "rb") as f:
        image = base64.b64encode(f.read()).decode("utf-8")

    image = f"data:image/jpeg;base64,{image}"

    # Add the filename to the query for better context
    prompt = f"[{filename_without_extension}] ![]({image}){query}\n\n"

    # Collect output tokens and remove '|eot_id|' token
    answer = ""
    for token in client.text_generation(prompt, stream=True):
        answer += token

    # Remove the eot_id token
    answer = answer.replace("<|eot_id|>", "").strip()

    # Delete the temporary resized image
    os.remove(resized_image_path)

    return answer


if __name__ == "__main__":
    print(imgVQA("levi-ackerman.jpg", "What is in the image?", "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"))
