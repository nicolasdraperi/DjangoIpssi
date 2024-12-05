from django import forms


class BlogPostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.Form):
    author = forms.CharField(max_length=50)
    text = forms.CharField(widget=forms.Textarea)
