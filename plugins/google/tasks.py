import webbrowser

def open(url: str):
    webbrowser.open(url)

def search(query: str):
    webbrowser.open(f"https://www.google.com/search?q={query}")