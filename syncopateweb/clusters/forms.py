from django import forms

class NewClusterForm(forms.Form):
    name = forms.CharField(label='',max_length=100)

    def __init__(self, *args, **kwargs):
        super(NewClusterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Cluster Name'})