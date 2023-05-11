from django.conf import settings
from requests.exceptions import RequestException

from openai import api

from .forms import ChatGPTSettingsForm
from weblate.machinery.base import MachineTranslation, MachineTranslationError


class ChatGPTTranslation(MachineTranslation):
    name = "ChatGPT"
    max_score = 90
    settings_form = ChatGPTSettingsForm

    @staticmethod
    def migrate_settings():
        return {
            "api_key": settings.MT_CHATGPT_API_KEY,
            "temperature": settings.MT_CHATGPT_TEMPERATURE,
        }

    def download_translations(self, source, language, text, unit, user, threshold=75):
        try:
            api_key = self.settings["api_key"]
            temperature = float(self.settings["temperature"])
        except (KeyError, ValueError):
            raise MachineTranslationError("Invalid API Key or temperature value")

        api.set_api_key(api_key)

        try:
            response = api.Completion.create(
                engine="text-davinci-002",
                prompt=text,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=temperature,
                top_p=1,
            )
        except Exception as e:
            raise MachineTranslationError(str(e))

        if not response.choices:
            raise MachineTranslationError("No response from the ChatGPT API")

        translation = response.choices[0].text.strip()

        yield {
            "text": translation,
            "quality": self.max_score,
            "service": self.name,
            "source": text,
        }

    def get_error_message(self, exc):
        if isinstance(exc, RequestException) and exc.response is not None:
            data = exc.response.json()
            try:
                return data["error"]["message"]
            except KeyError:
                pass

        return super().get_error_message(exc)
