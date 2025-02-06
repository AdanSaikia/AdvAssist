import pyautogui
from imgCaption import captionImg
from imgQA import imgVQA
from ocr import ocr
import google.generativeai as genai

def assist(prompt:str, inferenceToken:str):
    pyautogui.screenshot(r"cache\temp.png")

    caption = captionImg(r"cache\temp.png", inferenceToken)
    imgTxt = ocr(r"cache\temp.png")
    imgDesc = imgVQA(r"cache\temp.png", "Describe the image", inferenceToken)


    genai.configure(api_key="AIzaSyCuiNF8S4HbWKV60namJumCUJLaTI6e3mA")
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    # response =
    response = model.generate_content(f"{prompt}\nCaption: {caption}\nImage description:{imgDesc}\nOCR Text: {imgTxt}\n[Do not rely on the ocr content if it contains unrecognised words]")
    if response and hasattr(response, 'text') and response.text:
        response = response.text.replace("**", "").strip()

    return response




