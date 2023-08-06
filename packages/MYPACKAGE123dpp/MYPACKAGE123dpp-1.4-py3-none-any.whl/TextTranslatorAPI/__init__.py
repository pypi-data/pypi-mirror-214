import requests

class TextTranslatorAPI:
    def __init__(self, api_key):
        self.url = "https://text-translator2.p.rapidapi.com/translate"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }

    def translate_text(self, source_language, target_language, text):
        payload = {
            "source_language": source_language,
            "target_language": target_language,
            "text": text
        }

        response = requests.post(self.url, data=payload, headers=self.headers)
        return response.json()



api_key = "d9050d5653msh75d645c395b0db8p19a102jsn44253b504e66"

