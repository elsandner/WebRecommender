from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

# TODO: I have no idea what this code is used for?!   - Seems like it can be deleted
