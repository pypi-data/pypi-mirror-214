import requests

class ChatAPI:
    def __init__(self, api_key):
        self.url = "https://openai80.p.rapidapi.com/chat/completions"
        self.headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "openai80.p.rapidapi.com"
        }

    def send_message(self, user_input):
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }

        response = requests.post(self.url, json=payload, headers=self.headers)
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return content


# Example usage
api_key = "d9050d5653msh75d645c395b0db8p19a102jsn44253b504e66"
chat_api = ChatAPI(api_key)
user_input = input("User: ")
response = chat_api.send_message(user_input)
print("Assistant:", response)
