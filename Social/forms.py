from django import forms
from .models import *
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# Create your Forms here

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class':'post-input', 'placeholder': 'Caption', 'rows' : '1'}), required=True)
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'tag-input', 'placeholder': '# Tags'}), required=True)
    picture = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'image-input'}))
    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tag']


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['text']

class TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['tweet']
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model=Reply
        fields='__all__'

class CreateProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Full Name'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=True)
    bio=forms.CharField(widget=forms.Textarea(attrs={'id':'id_bio','placeholder':'Bio','rows':'1','name':'bio','class':'auto-resize','oninput':'autoResize(this)'}))
    
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'bio']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            from PIL import Image
            try:
                img = Image.open(image)
            except (IOError, ValueError):
                raise forms.ValidationError('Invalid image file.')

        return image
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the fields with initial values if instance is provided
        if 'instance' in kwargs:
            self.fields['username'].initial = kwargs['instance'].user.username
            self.fields['email'].initial = kwargs['instance'].user.email

    def save(self, commit=True):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )

        profile = super().save(commit=False)
        profile.user = user

        if commit:
            profile.save()

        return profile

class EditProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Full Name'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=True)
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'bio']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            from PIL import Image
            try:
                img = Image.open(image)
            except (IOError, ValueError):
                raise forms.ValidationError('Invalid image file.')
        return image
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the username and email fields with the current values
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        self.instance.user.username = self.cleaned_data['username']
        self.instance.user.email = self.cleaned_data['email']
        self.instance.user.save()

        profile = super().save(commit=False)
        profile.user = self.instance.user

        if commit:
            profile.save()

        return profile
