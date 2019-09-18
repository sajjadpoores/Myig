from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client, Plan
from user.models import User
from PIL import Image
# from validate_email import validate_email
from email_validator import validate_email, EmailNotValidError

class SignupForm(UserCreationForm):
    class Meta:
        fields = ['username', 'email']
        model = Client

    error_messages = {
        'password_mismatch': ("کلمه عبور و تاییدیه یکسان نیستند."),
        'required': ('این فیلد ضروری است.'),
        'unique': ('این نام کاربری قبلا ثبت شده است'),
    }

    email_error_messages = {
        'required': ('این فیلد ضروری است.'),
        'unique': ('این ایمیل قبلا ثبت شده است'),
    }

    password1 = forms.CharField(
        label="کلمه عبور",
        strip=False,
        widget=forms.PasswordInput,
        error_messages=error_messages,
    )
    password2 = forms.CharField(
        label="تایید کلمه عبور",
        widget=forms.PasswordInput,
        strip=False,
        error_messages=error_messages,
    )

    username = forms.CharField(
        label='نام کاربری',
        max_length=150,
        strip=False,
        error_messages=error_messages,
    )

    email = forms.CharField(
        label='ایمیل',
        max_length=150,
        strip=False,
        error_messages=email_error_messages ,
    )

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            v = validate_email(data)  # validate and get info
            return data
        except EmailNotValidError as e:
            raise forms.ValidationError("ایمیل نا معتبر است")


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=30)
    password = forms.CharField(label='کلمه عبور', max_length=30, widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=30)
    password = forms.CharField(label='کلمه عبور', max_length=30, widget=forms.PasswordInput)


STEP2_CHOICES = (
    (0, 'موبایل'),
    (1, 'ایمیل'),
)


class AddUserStep2Form(forms.Form):
    choice = forms.ChoiceField(label='نحوه احراز هویت', choices=STEP2_CHOICES, widget=forms.RadioSelect(),
                                required=True)
    username = forms.CharField(label='username', max_length=30, widget=forms.HiddenInput, required=True)


class AddUserStep3Form(forms.Form):
    code = forms.CharField(label='کد فعالسازی', max_length=10, required=True)
    username = forms.CharField(label='username', max_length=30, widget=forms.HiddenInput, required=True)


class AddPlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'price', 'time', 'followers1', 'followers2', 'charge']


class PostForm(forms.Form):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    post_date = forms.CharField(label='ارسال در تاریخ')
    post_h = forms.CharField(label='ساعت ارسال')
    post_m = forms.CharField(label='دقیقه ارسال')
    caption = forms.Textarea()
    photo = forms.ImageField(label='انتخاب عکس')
    file = forms.FileField(label='انتخاب فایل')

    def save(self):
        photo = super(PostForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo


class TradeForm(forms.Form):
    from_user = forms.ChoiceField(label='از اکانت', choices=((x.uid, x.username) for x in User.objects.all()), widget=forms.Select(), required=True)
    to_user = forms.ChoiceField(label='به اکانت', choices=((x.uid, x.username) for x in User.objects.all()), widget=forms.Select(), required=True)
    days = forms.IntegerField(label='روز', min_value=0, required=True, initial=0)
    hours = forms.IntegerField(label='ساعت', min_value=0, required=True, initial=0)
    minutes = forms.IntegerField(label='دقیقه', min_value=0, required=True, initial=0)
