from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ModernRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'peer w-full bg-transparent border-b-2 border-white/20 px-0 py-3 text-white focus:border-[#d4af37] focus:outline-none transition-colors placeholder-transparent',
                'placeholder': ' ' # Required for Tailwind's peer-placeholder-shown to work
            })