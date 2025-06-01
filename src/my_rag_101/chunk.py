# chunk.py
# Implements document chunking for RAG pipeline

def read_data() -> str:
    with open('data.md', 'r', encoding='utf-8') as f:
        return f.read()

def get_chunks() -> list[str]:
    content: str = read_data()
    chunks: list[str] = content.split('\n\n')

    result: list[Any] = []
    header: Literal[''] = ''

    for c in chunks:
        if c.startswith("#"):
            header += f"{c}\n"
        else:
            result.append(f"{header}{c}")
            header: Literal[''] = ""

    return result

# def chunk_text(text, chunk_size=500):
#     """
#     Splits the input text into chunks of specified size.
#     """
#     return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


if __name__ == "__main__":
    chunks: list[str] = get_chunks()
    for c in chunks:
        print(c)
        print("-----------------")
