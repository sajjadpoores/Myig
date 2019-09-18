from django import forms
from django.forms import MultipleChoiceField


class MyMultipleChoiceField(MultipleChoiceField):

    def validate(self, value):
        return True


class UserSettingForm(forms.Form):
    comment = forms.BooleanField(label='کامنت', required=False)
    like = forms.BooleanField(label='لایک', required=False)
    comentslike = forms.BooleanField(label='لایک کامنت', required=False)
    unfollow = forms.BooleanField(label='آنفالو', required=False)
    direct = forms.BooleanField(label='دایرکت', required=False)
    follow = forms.BooleanField(label='فالو', required=False)

    speed = forms.ChoiceField(label='سرعت فعالیت', choices=(
        (1, 'کم'),
        (2, 'متوسط'),
        (3, 'زیاد'),
        (4, 'دستی'),
    ))
    follow_per_hour = forms.IntegerField(label='فالو بر ساعت', min_value=0)
    following_range1 = forms.IntegerField(label='شروع حدود فالووینگ صفحات', min_value=0)
    following_range2 = forms.IntegerField(label='پایان حدود فالووینگ صفحات', min_value=0)

    follower_range1 = forms.IntegerField(label='شروع حدود فالوور صفحات', min_value=0)
    follower_range2 = forms.IntegerField(label='پایان حدود فالوور صفحات', min_value=0)

    post_range1 = forms.IntegerField(label='شروع حدود تعداد پست ها', min_value=0)
    post_range2 = forms.IntegerField(label='پایان حدود تعداد پست ها', min_value=0)

    follow_source = forms.ChoiceField(label='منبع فالو', choices=(
        (1, 'کاربران هدف'),
        (2, 'لایک کنندگان کاربران هدف'),
        (3, 'لایک کنندگان تگ ها'),
    ))
    follow_twice = forms.BooleanField(label='دوبار فالو نکن', required=False)

    business_follow = forms.BooleanField(label='صفحات بیزینس را فالو کن', required=False)
    non_avatar_follow = forms.BooleanField(label='صفحات بدون عکس را فالو نکن', required=False)
    public_follow = forms.BooleanField(label='صفحات پابلیک را فالو کن', required=False)
    private_follow = forms.BooleanField(label='صفحات پرایوت را فالو کن', required=False)

    target_list = MyMultipleChoiceField(label='لیست کاربران هدف', required=False)
