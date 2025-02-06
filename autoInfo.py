
def info(query: str, lines: int) -> str:
    """"
    Args:
        query (str): The specific topic you want to retrieve information about
        lines (int): The length of the result obtained. (The number of lines)
    """
    import wikipedia

    try:
        data: str = wikipedia.summary(query, sentences=lines).replace("No.", "No")
        extraLn: int = 1
        while not data.endswith("."):
            data: str = wikipedia.summary(query, sentences=lines+extraLn).replace("No.", "No")
            extraLn += 1

        return data.replace(".", ".\n")

    except:
        return ''


if __name__ == "__main__":
    print(info("Elon Musk", 2))