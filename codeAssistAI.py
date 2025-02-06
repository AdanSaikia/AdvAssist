from huggingface_hub import InferenceClient

def codeAssist(programPath: str, prompt: str = "DEBUG MY CODE", inferenceToken: str|None = None):

    with open(programPath, 'r') as program:
        existingCode = program.read()

    client = InferenceClient(api_key=inferenceToken)

    messages = [
        {
            "role": "user",
            "content": f"{prompt}\n[THIS IS HIDDEN INSTRUCTION]: Do not use any text-formatting that includes special characters;\nHowever you shall wrap the code with opening and starting tags at start and end of code with '<code>' and '</code>. \n\nMy current code:\n{existingCode}"
        }
    ]

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
    )

    response = str(completion.choices[0].message.content)

    if "<code>" in response or "</code>" in response:
        with open(f'{programPath}', 'a') as f:
            code = response.split("<code>")[1]
            code = code.split("</code>")[0]
            f.write("\n\n\n*"*100)
            f.write(f"\n{code}")

        return response.replace(code, f"The improved code is saved as '{programPath}' in the current directory. ✨🗿").replace("<code>", "\n").replace("</code", "\n")

    else:
        return "Improved version of your code could not be generated."


if __name__ == "__main__":
    from liveAssistAI import assist
    print(assist("Why my code is not displayed...why not working, please help", "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"))

