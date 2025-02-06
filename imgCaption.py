import os
import requests

def captionImg(imgPath: str, inferenceToken: str = os.getenv('HUGGINGFACE_IMG_TOKEN')):

    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": f"Bearer {inferenceToken}"}

    with open(imgPath, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)

    result = response.json()
    caption_text = result[0]['generated_text'] if result else "No caption generated"
    return caption_text

if __name__ == "__main__":
    print(captionImg("levi-ackerman.jpg", "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"))