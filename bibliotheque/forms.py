from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ModernRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On applique le style "Gold" à tous les champs d'un coup
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-white/5 border border-gold/10 rounded-xl px-4 py-3 text-sm text-white focus:border-gold outline-none transition-all',
                'placeholder': field.label
            })