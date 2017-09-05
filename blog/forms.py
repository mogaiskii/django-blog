from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
    def __init__(self, *args, **kwargs):
    	super(PostForm,self).__init__(*args,**kwargs)
    	self.fields['title'].widget=forms.TextInput(attrs={'autocomplite':'off','class':'form-control'})
    	self.fields['text'].widget=forms.Textarea(attrs={'autocomplite':'off','class':'form-control','rows':'14'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'author')
