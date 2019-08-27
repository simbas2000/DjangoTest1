from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={'placeholder': 'Enter a to-do item', 'class': 'form-control'})
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }

    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid:
            self.fields['text'].widget = forms.fields.TextInput(
                attrs={'placeholder': 'Enter a to-do item', 'class': 'form-control is-valid'})
        else:
            self.fields['text'].widget = forms.fields.TextInput(
                attrs={'placeholder': 'Enter a to-do item', 'class': 'form-control is-invalid'})
        return is_valid
