import requests

def get():
    target = "https://www.google.com/"
    response = requests.get(target)
    print(response.text)

if __name__ == "__main__":
    get()
    