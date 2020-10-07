from tweets.models import Tweet
from django import forms
from .models import Tweet



MAX_TWEET_LENGTH = 250

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is tooo long")
        return content
