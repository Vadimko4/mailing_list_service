from django.forms import BooleanField, ModelForm

from mailer.models import Letter, Recipient


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class LetterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Letter
        exclude = ('created_at', 'updated_at', 'owner',)


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        exclude = ('owner',)
