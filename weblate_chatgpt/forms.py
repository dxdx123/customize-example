from django import forms
from weblate.machinery.forms import BaseMachineryForm

class ChatGPTSettingsForm(BaseMachineryForm):
    openai_api_key = forms.CharField(
        label=_("OpenAI API Key"),
        max_length=200,
        required=True,
        help_text=_("Your OpenAI API Key."),
    )

    temperature = forms.FloatField(
        label=_("Temperature"),
        min_value=0.0,
        max_value=1.0,
        initial=0.8,
        help_text=_("Temperature setting for the ChatGPT."),
    )
