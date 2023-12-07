from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, PostComment

#user registration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        #adding classes and placeholders
        def __init__(self, *args, **kwargs):
            super(UserRegistrationForm,self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update(
                {'class':'registername','paceholder':'Enter username...'}
            )
            self.fields['email'].widget.attrs.update(
                {'class':'registeremail','placeholder':'Enter email...'}
            )
            self.fields['password1'].widget.attr.update(
                {'class':'registerpassword1','placeholder':'Enter password...'}
            )
            self.fields['password2'].widget.attrs.update(
                {'class':'registerpassword2', 'placeholder':'Confirm password...'}
            )
        
#user login form       
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class':'loginusername','placeholder':'Enter username...'}
        )
        self.fields['password'].widget.attrs.update(
            {'class':'loginpassword','placeholder':'Enter password...'}
        )
    
#user updateform for uername and email
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
#user profile create form
class UserProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'location', 'profile_image']
        
        def __init__(self, *args, **kwargs):
            super(UserProfileCreateForm, self).__init__(*args, **kwargs)
            self.fields['nickname'].widget.attrs.update(
                {'class':'nickname','placeholder':'Enter nickname...'}
            )
            self.fields['location'].widgets.attrs.update(
                {'class':'location','placeholder':'Enter location...'}
            )
        
#user profile update
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'location']
        
        def __init__(self, *args, **kwargs):
            super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
            self.fields['nickname'].widget.attrs.update(
                {'class':'nickname','placeholder':'Enter nickname...'}
            )
            self.fields['location'].widgets.attrs.update(
                {'class':'location','placeholder':'Enter location...'}
            )
        
#Post upload form
class PostUploadFoam(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','post_image']
        
        def __init__(self, *args, **kwargs):
            super(PostUploadFoam, self).__init__(*args, **kwargs)
            self.fields['title'].widget.attrs.update(
                {'class':'title','placeholder':'Enter title...'}
            )
            self.fields['description'].widgets.attrs.update(
                {'class':'description','placeholder':'Enter description...'}
            )
            self.fields['post_image'].widget.attrs.update(
                {'class':'post_image'}
            )
        
        
#comment form
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = PostComment
        fields = ['comment', 'rate']
        
        
            