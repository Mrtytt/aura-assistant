from memory import memory

def get_response(input_text):
    input_text = input_text.strip().lower()
    if input_text in memory:
        return memory[input_text]
    return "Bilmiyorum. Lütfen öğret."

def teach(input_text, response_text):
    input_text = input_text.strip().lower()
    memory[input_text] = response_text.strip()
