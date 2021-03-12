from django import forms

class ArticleForm(forms.Form):
	title = forms.CharField(label="Article Title", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	content = forms.CharField(label="Page Content:", widget=forms.Textarea(attrs={'class': 'form-control'}))