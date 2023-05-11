import requests
from django.conf import settings
from .forms import ChatGPTSettingsForm
from weblate.machinery.base import MachineTranslation, MachineTranslationError

class ChatGPTTranslation(MachineTranslation):
    name = "ChatGPT"
    max_score = 90
    settings_form = ChatGPTSettingsForm

    def download_languages(self):
        # 返回支持的语言代码列表
        return settings.LANGUAGES.keys()

    def download_translations(
        self,
        source,
        language,
        text: str,
        unit,
        user,
        threshold: int = 75,
    ):
        # 从ChatGPT API获取翻译
        headers = {
            "Authorization": f"Bearer {self.settings['openai_api_key']}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "text-davinci-002",
            "prompt": f"Translate the following English text to {language}:\n{text}",
            "temperature": self.settings["temperature"],
            "max_tokens": 200,
            "n": 1,
        }
        response = requests.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers=headers,
            json=data,
        )

        if response.status_code != 200:
            raise MachineTranslationError(response.json()["error"]["message"])

        result = response.json()["choices"][0]["text"].strip()
        yield {
            "text": result,
            "quality": self.max_score,
            "service": self.name,
            "source": text,
        }

    def get_error_message(self, exc):
        if isinstance(exc, requests.exceptions.RequestException) and exc.response is not None:
            data = exc.response.json()
            try:
                return data["error"]["message"]
            except KeyError:
                pass

        return super().get_error_message(exc)
