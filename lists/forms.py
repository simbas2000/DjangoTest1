from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


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

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)
