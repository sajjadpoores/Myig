from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from .forms import SignupForm, LoginForm, AddUserForm, AddUserStep2Form, AddUserStep3Form, AddPlanForm, PostForm, TradeForm
from .models import Client, Activity, Plan, Payment
from django.contrib.auth import authenticate, login, logout
import instagram_web_api
from user.models import User, UserHistory, Post
import requests
import json
import datetime, jdatetime
from website.settings import SERVER_URL
from user.views import update_user_charge
import os
from django.utils.crypto import get_random_string
import hashlib
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q


def redirect_to_dashboard(request, addMessage=None, tradeMessage=None):
    if request.user.is_authenticated:
        if request.user.is_staff:
            users = User.objects.all()
        elif request.user.marketer:
            users = User.objects.filter(Q(cid=request.user) | Q(cid__parent=request.user))
        else:
            users = User.objects.filter(cid=request.user)

        on = 0
        off = 0
        for user in users:
            # insta_info = get_insta_info2(user.uid)
            # user.insta_info = insta_info

            if user.status == 0:
                update_user_charge(user)

            if user.status == 0 or user.status == 1:
                on += 1
            else:
                off += 1

        return render(request, 'client/dashboard.html', {'users': users, 'message': addMessage, 'on': on, 'off': off,
                                                         'tradeMessage': tradeMessage})
    return redirect('/client/login/')  # TODO: redirect to error page


class ClientDashboardView(TemplateView):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect_to_dashboard(request, None)
        return redirect('/client/login/')


def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


class SignupView(TemplateView):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/client/dashboard/')

        form = SignupForm()
        return render(request, 'client/signup.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/client/dashboard/')

        form = SignupForm(request.POST)
        if form.is_valid():
            client = form.save()
            client.is_active = False
            client.code = generate_activation_key(client.username)

            html_content = render_to_string('client/send_activation_code.html', {'client': client})
            text_content = strip_tags(html_content)
            from website.settings import EMAIL_HOST_USER
            send_mail('کد فعالسازی حساب شما', text_content, EMAIL_HOST_USER, [client.email], html_message=html_content)

            client.save()
            return HttpResponse("نام کاربری شما ثبت شد. لینک فعالسازی به ایمیلتان فرستاده شد.")

        return render(request, 'client/signup.html', {'form': form})


class RecommendView(TemplateView):

    def get(self, request, cid):
        if request.user.is_authenticated:
            return redirect('/client/dashboard/')

        parent = get_client(cid)
        if not parent:
            return HttpResponse('کاربری با این شماره وجود ندارد.')

        form = SignupForm()
        return render(request, 'client/signup.html', {'form': form})

    def post(self, request, cid):
        if request.user.is_authenticated:
            return redirect('/client/dashboard/')

        parent = get_client(cid)
        if not parent:
            return HttpResponse('کاربری با این شماره وجود ندارد.')

        form = SignupForm(request.POST)
        if form.is_valid():
            client = form.save()
            client.is_active = False
            client.code = generate_activation_key(client.username)
            client.parent = parent
            html_content = render_to_string('client/send_activation_code.html', {'client': client})
            text_content = strip_tags(html_content)
            from website.settings import EMAIL_HOST_USER
            send_mail('کد فعالسازی حساب شما', text_content, EMAIL_HOST_USER, [client.email], html_message=html_content)

            client.save()
            return HttpResponse("نام کاربری شما ثبت شد. لینک فعالسازی به ایمیلتان فرستاده شد.")

        return render(request, 'client/signup.html', {'form': form})


class ActivateView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not client or request.user.is_active or client.is_active:
            return redirect_to_dashboard(request)

        return render(request, 'client/activate.html')

    def post(self, request, cid):
        client = get_client(cid)
        if not client or request.user.is_active or client.is_active:
            return redirect_to_dashboard(request)

        code = request.POST.get('code', None)
        if code and client.code == code and client.code != '':
            client.is_active = True
            client.code = ''
            client.save()
            login(request, client)
            return redirect('/client/login/')

        error = 'کد فعالسازی نامعتبر است'
        return render(request, 'client/activate.html', {'error': error})


class ActivateWithLinkView(TemplateView):
    def get(self, request, cid, code):
        client = get_client(cid)
        if not client or request.user.is_active or client.is_active:
            return redirect_to_dashboard(request)

        if code and client.code == code and client.code != '':
            client.is_active = True
            client.code = ''
            client.save()
            login(request, client)
            return redirect('/client/login/')

        error = 'کد فعالسازی نامعتبر است'
        return render(request, 'client/activate.html', {'error': error})


class ResetPassword(TemplateView):

    def get(self, request):
        return render(request, 'client/forgetPassword.html')

    def post(self, request):
        email = request.POST.get('email', None)

        if not email:
            error = 'لطفا ایمیل خود را وارد کنید.'
            return render(request, 'client/forgetPassword.html', {'error': error})

        client = Client.objects.filter(email=email)
        if len(client) == 0:
            error = 'ایمیل وارد شده معتبر نیست.'
            return render(request, 'client/forgetPassword.html', {'error': error})

        client = client[0]
        client.code = generate_activation_key(client.username)

        html_content = render_to_string('client/send_reset_code.html', {'client': client})
        text_content = strip_tags(html_content)
        from website.settings import EMAIL_HOST_USER
        send_mail('کد تغییر کلمه عبور', text_content, EMAIL_HOST_USER, [client.email], html_message=html_content)

        client.save()

        return HttpResponse('لینک تغییر پسورد برای شما فرستاده شد.')


class ChangePassword(TemplateView):

        def get(self, request, cid, code):
            client = get_client(cid)
            if not (client and client.code != ''):
                return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

            errors = []
            if client.code != code:
                errors.append('کد نا معتبر است.')

            return render(request, 'client/changePassword.html', {'errors': errors})

        def post(self, request, cid, code):
            client = get_client(cid)
            if not (client and client.code != ''):
                return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

            errors = []
            if client.code != code:
                errors.append('کد نا معتبر است.')

            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)

            if password1 != password2:
                errors.append('کلمه عبور و تاییدیه آن برابر نیستند.')

            if len(errors) > 0:
                return render(request, 'client/changePassword.html', {'errors': errors})

            client.set_password(password1)
            client.code = ''
            client.is_active = True
            client.save()

            return redirect('/client/login/')


class ClientChangeEmailView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        errors = []
        return render(request, 'client/email.html', {'client': client, 'errors': errors})

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        errors = []
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if not email:
            errors.append('لطفا ایمیل خود را وارد کنید.')
        elif email == client.email:
            errors.append('لطفا ایمیلی غیر از ایمیل فعلی ثبت شده وارد نمایید.')

        check_email = Client.objects.filter(email=email)
        if len(check_email) > 0:
            errors.append('این ایمیل قبلا ثبت شده است.')

        if not password:
            errors.append('لطفا پسورد خود را وارد کنید.')

        if not client.check_password(password):
            errors.append('پسورد وارد شده صحیح نیست.')

        if len(errors) > 0:
            return render(request, 'client/email.html', {'client': client, 'errors': errors})

        client.email = email
        client.is_active = False
        client.code = generate_activation_key(client.username)

        html_content = render_to_string('client/send_activation_code.html', {'client': client})
        text_content = strip_tags(html_content)
        from website.settings import EMAIL_HOST_USER
        send_mail('کد فعالسازی ایمیل شما', text_content, EMAIL_HOST_USER, [client.email], html_message=html_content)
        client.save()

        logout(request)
        return HttpResponse("کد فعالسازی به ایمیلتان فرستاده شد.")  # TODO: show success msg on main page


class LoginView(TemplateView):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/client/dashboard/')

        form = LoginForm()
        return render(request, 'client/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/client/dashboard/')

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            client = authenticate(username=username, password=password)

            if client is not None:
                login(request, client)
                return redirect('/client/dashboard/')
        return render(request, 'client/login.html', {'form': form})


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)

        return redirect('/client/login/')


def get_client(cid):
    try:
        client = Client.objects.get(pk=cid)
    except Client.DoesNotExist:
        client = None
    return client


def get_uid(username):
    instagram = instagram_web_api.Client()

    try:
        insta_user_info = instagram.user_info2(username)
    except instagram_web_api.ClientError:
        insta_user_info = {}

    insta_user_id = insta_user_info.get('id', None)

    return insta_user_id


def get_user_history(uid):
    try:
        user_history = UserHistory.objects.get(pk=uid)
    except UserHistory.DoesNotExist:
        user_history = None
    return user_history


def save_user(response, client, username, insta_user_id):
    cookie = response.get('cookie', '')
    phone_info = response.get('phone_info', '')

    user_history = get_user_history(insta_user_id)

    if not (client.used_free or user_history):
        charge = 3 * 24 * 3600
        client.used_free = True
        client.save()

        UserHistory.objects.create(uid=insta_user_id)
    else:
        charge = 0

    json_chart = {
        "chart": [],
        "all":
            {
                "follow": 0,
                "like": 0,
                "comment": 0,
                "commentsLike": 0,
                "unfollow": 0,
                "newFollower": 0,
                "direct": 0
            }
    }
    for i in range(30):
        start_date = datetime.date.today() + datetime.timedelta(i)
        json_chart['chart'].append({
            "follow": 0,
            "like": 0,
            "comment": 0,
            "commentsLike": 0,
            "unfollow": 0,
            "direct": 0,
            "newFollower": 0,
            "date": str(start_date)
        })

    json_chart = json.dumps(json_chart)
    json_chart = json.loads(json_chart)

    first_time = False
    if not user_history:
        first_time = True

    user = User.objects.create(uid=insta_user_id, username=username, cookie=cookie, phone_info=phone_info,
                               status=100, cid=client, charge=charge, json_chart=json_chart, first_time=first_time)

    return user


class AddUserView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserForm()
        return render(request, 'client/add.html', {'form': form})

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            insta_user_id = get_uid(username)

            if insta_user_id:
                # check user existence in DB
                user = User.objects.filter(pk=insta_user_id).first()

                if not user: # if user does not exist in DB

                    try:
                        response = requests.post(SERVER_URL,
                                                 {'data': "{},{},{}".format(1, username, password)}, timeout=30)
                    except Exception:
                        return redirect_to_dashboard(request, 'اشکال در اتصال به سرور')

                    try:
                        response = json.loads(response.text)
                    except ValueError:
                        return redirect_to_dashboard(request, 'اشکال در سرور')

                    status = response.get('status', None)

                    if status == 'ok':
                        user = save_user(response, client, username, insta_user_id)
                        if user:
                            return redirect('/client/dashboard/')
                        else:
                            return redirect_to_dashboard(request, 'اشکال در ذخیره سازی یوزر')
                    elif status == 'fail':
                        return redirect_to_dashboard(request, response.get('message', ''))
                    elif status == 'challenge':
                        choices = response.get('choices', [])
                        form2 = AddUserStep2Form(initial={'username': username})
                        return render(request, 'client/add2.html', {'form': form2, 'choices': choices, 'cid': cid})

                    return JsonResponse(response)
                return redirect_to_dashboard(request, 'این یوزر قبلا در سایت ثبت شده است.')
            return redirect_to_dashboard(request, 'اشکال در اتصال به اینستاگرام')
        return redirect_to_dashboard(request, None)


class AddUserStep2View(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        return redirect_to_dashboard(request, None)

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserStep2Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            choice = form.cleaned_data['choice']

            response = requests.post(SERVER_URL,
                                     {'data': "{},{},{}".format(2, username, choice)}, timeout=30)

            try:
                response = json.loads(response.text)
            except ValueError:
                return render(request, 'client/add2.html', {'form': form, 'error': "اشکال در سرور"})

            status = response.get('status', None)

            if status == 'ok':
                form2 = AddUserStep3Form(initial={'username': username})
                return render(request, 'client/add3.html', {'form': form2, 'cid': cid})
            else:
                return redirect_to_dashboard(request, None)

            return JsonResponse(response)
        return HttpResponse("QWE")  # TODO: handle this


class AddUserStep3View(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        return redirect_to_dashboard(request, None)

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserStep3Form(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            code = form.cleaned_data['code']

            response = requests.post(SERVER_URL,
                                     {'data': "{},{},{}".format(3, username, code)}, timeout=30)

            try:
                response = json.loads(response.text)
            except ValueError:
                return redirect('/client/{}/add/'.format(cid))

            status = response.get('status', None)
            error = response.get('msg', '')

            if status == 'ok':
                user = save_user(response, client, username, get_uid(username))
                return redirect('/client/dashboard/')
            elif status == 'fail':
                form2 = AddUserStep3Form(initial={'username': username})
                return render(request, 'client/add3.html', {'form': form2, 'cid': cid, 'error': error})
            else:
                return redirect_to_dashboard(request, None)

        return HttpResponse("مشکل نا مشخص")


class ClientUserDeleteView(TemplateView):
    def get(self, request, cid, uid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        import user
        user = user.views.get_user(uid)
        if not (user and (user.cid == request.user or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        user.delete()

        return redirect('/client/dashboard/')


class ClientDetailView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return render(request, 'client/detail.html', {'client': client})


class ClientUserListView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff )):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        users = User.objects.filter(cid=client)
        return render(request, 'client/list.html', {'users': users})


class ClientUserListOfAllView(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        users = User.objects.all()
        return render(request, 'client/list.html', {'users': users})


class ClientSelectUserView(TemplateView):

    def get(self, request, cid, pid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff )):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        plan = get_plan(pid)
        if not plan:
            return HttpResponse("selected plan does not exist")  # TODO: redirect to error page

        if request.user.is_staff:
            users = User.objects.all()
        else:
            users = User.objects.filter(cid=request.user)

        # from user.views import get_insta_info2
        for user in users:
        #     insta_info = get_insta_info2(user.uid)
        #     user.insta_info = insta_info
            if user.status == 0:
                update_user_charge(user)

        return render(request, 'plan/selectuser.html', {'users': users, 'plan': plan, 'client': client})


class ClientPrePaymentView(TemplateView):
    def get(self, request, cid, pid):
        return HttpResponse("this page does not support get request")

    def post(self, request, cid, pid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        plan = get_plan(pid)
        if not plan:
            return HttpResponse("selected plan does not exist")  # TODO: redirect to error page

        selected_users = request.POST.getlist('users[]')

        if len(selected_users) == 0: # if no user is selected
            if request.user.is_staff:
                users = User.objects.all()
            else:
                users = User.objects.filter(cid=request.user)

            from user.views import get_insta_info2
            for user in users:
                # insta_info = get_insta_info2(user.uid)
                # user.insta_info = insta_info

                if user.status == 0:
                    update_user_charge(user)

                return render(request, 'plan/selectuser.html', {'users': users, 'plan': plan, 'client': client})

        users = []
        from user.views import get_user
        for selected_user in selected_users:
            user = get_user(int(selected_user))
            if user:
                users.append(user)

        total = len(users) * plan.price
        return render(request, 'plan/prepay.html', {'users': users, 'plan': plan, 'total': total, 'client': client})


# for client
class ClientPlanListView(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/client/login/')
        plans = Plan.objects.all()
        return render(request, 'plan/list.html', {'plans': plans})


# for admin
class ClientPlansView(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        plans = Plan.objects.all()
        return render(request, 'plan/planlist.html', {'plans': plans})


class ClientAddPlan(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddPlanForm()
        return render(request, 'plan/create.html', {'form': form})

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/client/plan/plans/')
        return render(request, 'plan/create.html', {'form': form})


def get_plan(pid):
    try:
        plan = Plan.objects.get(pk=pid)
    except Plan.DoesNotExist:
        plan = None
    return plan


class ClientPlanDetail(TemplateView):

    def get(self, request, pid):
        plan = get_plan(pid)
        if not (request.user.is_staff and plan):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return render(request, 'plan/detail.html', {'plan': plan})


class ClientDeletePlanView(TemplateView):

    def get(self, request, pid):
        plan = get_plan(pid)
        if not (request.user.is_staff and plan):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        plan.delete()
        return redirect('/client/plan/plans/')


class ClientEditPlan(TemplateView):

    def get(self, request, pid):
        plan = get_plan(pid)

        if not (request.user.is_staff and plan):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddPlanForm(instance=plan)
        return render(request, 'plan/edit.html', {'form': form, 'plan': plan})

    def post(self, request, pid):
        plan = get_plan(pid)

        if not (request.user.is_staff and plan):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('/client/plan/plans/')
        return render(request, 'plan/edit.html', {'form': form, 'plan': plan})


import zeep
MERCHANT = 'e7ff5cc6-7b1c-11e8-8400-005056a205be'
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional


class ClientPayView(TemplateView):

    def post(self, request, cid, pid):
        client_user = get_client(cid)
        plan = get_plan(pid)

        if not (client_user and request.user == client_user and plan):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        users = request.POST.getlist('users[]')

        if len(users) == 0:  # if no user is selected
            if request.user.is_staff:
                users = User.objects.all()
            else:
                users = User.objects.filter(cid=request.user)

            from user.views import get_insta_info2
            for user in users:
                insta_info = get_insta_info2(user.uid)
                user.insta_info = insta_info

                if user.status == 0:
                    update_user_charge(user)

                return render(request, 'plan/selectuser.html', {'users': users, 'plan': plan, 'client': client_user})

        client = zeep.Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        amount = len(users) * plan.price  # Toman

        items = {'list': []}
        for user in users:
            x = {'uid': int(user), 'pid': pid}
            items['list'].append(x)
        payment = Payment(cid=client_user, pid=plan, amount=amount, done=False, items=items)
        payment.save()

        description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید."  # Required
        CallbackURL = 'https://myig.ir/client/{}/plan/{}/pay/{}/verify/'.format(client_user.id, plan.id, payment.id)  # edit for realy server.
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)

        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            payment.delete()
            return HttpResponse("خطا در اتصال به درگاه")  # TODO: redirect to error page


def get_payment(payid):
    try:
        payment = Payment.objects.get(pk=payid)
    except Plan.DoesNotExist:
        payment = None
    return payment


def add_charge_payment_done(plan, payment):
    payment.done = True
    payment.save()

    from user.views import get_user
    payment_items = payment.items.get('list', [])
    for item in payment_items:
        user = get_user(item['uid'])
        user.charge += plan.charge
        if user.status == -300:
            user.status = 100
        user.save()


def add_income_to_parent(payment):
    client = payment.cid
    if client.parent and client.parent.marketer:
        income = payment.amount * client.parent.participation / 100
        client.parent.income += income
        client.parent.save()


class ClientVerifyView(TemplateView):

    def get(self, request, cid, pid, payid):
        client_user = get_client(cid)
        plan = get_plan(pid)
        payment = get_payment(payid)
        if not (client_user and request.user == client_user and plan and payment):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        client = zeep.Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

        if request.GET.get('Status') == 'OK':
            price = len(payment.items['list']) * plan.price
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], price)

            if result.Status == 100:
                add_charge_payment_done(plan, payment)
                add_income_to_parent(payment)
                return redirect('/client/dashboard/')  # TODO: redirect to history of paymentsreturn HttpResponse('Done')
            elif result.Status == 101:
                return HttpResponse('پرداخت شما ثبت شد.')
            else:
                return HttpResponse('پرداخت صورت نگرفت.')
        else:
            return HttpResponse('پرداخت صورت نگرفت.')


class ClientStartAllUsersView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if client.is_staff or request.user.is_staff:
            users = User.objects.all()
        else:
            users = User.objects.filter(cid=client)

        from user.views import start_user

        for user in users:
            status = user.status

            if status == 100:
                start_user(user)

        return HttpResponse("done!")


class ClientStopAllUsersView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if client.is_staff or request.user.is_staff:
            users = User.objects.all()
        else:
            users = User.objects.filter(cid=client)

        from user.views import stop_user

        for user in users:
            status = user.status

            if status == 1 or status == 0:
                stop_user(user)

        return HttpResponse("done!")


class ClientChartsView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if client.is_staff or request.user.is_staff:
            users = User.objects.all()
        else:
            users = User.objects.filter(cid=client)

        # from user.views import get_insta_info2
        # for user in users:
        #     insta_info = get_insta_info2(user.uid)
        #     user.insta_info = insta_info

        return render(request, 'client/charts.html', {'client': client, 'users': users})


class ClientScheduledPostView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = PostForm()

        if client.is_staff or request.user.is_staff:
            users = User.objects.all()
        else:
            users = User.objects.filter(cid=client)

        # from user.views import get_insta_info2
        # for user in users:
        #     insta_info = get_insta_info2(user.uid)
        #     user.insta_info = insta_info

        return render(request, 'post/request.html', {'form': form, 'users': users})

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = PostForm(request.POST)
        mode = form.data.get('mode', None)
        caption = form.data.get('caption', '')
        users = request.POST.getlist('users[]', None)
        if users:
            users = list(map(int, users))
        post_date = form.data.get('post_date', None)
        post_h = form.data.get('post_h', None)
        post_m = form.data.get('post_m', None)

        if post_date:
            post_date = post_date.split('/')
            post_date = jdatetime.datetime(int(post_date[0]), int(post_date[1]), int(post_date[2]), int(post_h),
                                           int(post_m)).togregorian()
        else:
            post_date = datetime.datetime.now()

        photo = request.FILES.get('photo', None)
        video = request.FILES.get('video', None)

        errors = []

        if len(users) == 0:
            errors.append('باید حداقل یک یوزر را انتخاب کنید.')
        if not(photo or video):
            errors.append('هیچ فایلی فرستاده نشده است.')
        elif photo and video:
            errors.append('نمی توانید همزمان هم فیلم و هم عکس بفرستید.')
        elif video:
            valid_formats = ['avi', 'mp4', '3gp', 'flv', 'wmv', 'mov']
            if not video.name.split('.')[-1] in valid_formats:
                errors.push('فایل انتخاب شده مورد قبول نیست.')

        if not mode:
            errors.append('استوری نمیتواند متن داشته باشد.')
        if mode == 1 and len(caption) > 0:
            errors.append('استوری نمیتواند متن داشته باشد.')

        if len(errors) > 0:
            if client.is_staff or request.user.is_staff:
                users = User.objects.all()
            else:
                users = User.objects.filter(cid=client)

            from user.views import get_insta_info2
            for user in users:
                insta_info = get_insta_info2(user.uid)
                user.insta_info = insta_info
            return render(request, 'post/request.html', {'form': form, 'users': users, 'errors': errors})

        # if form is valid
        for user in users:
            from user.views import get_user
            user_boject = get_user(user)
            if photo:
                x = float(form.data.get('x'))
                y = float(form.data.get('y'))
                w = float(form.data.get('width'))
                h = float(form.data.get('height'))

                import math

                __device_ratios = [(3, 4), (2, 3), (5, 8), (3, 5), (9, 16), (10, 16), (40, 71)]
                __aspect_ratios = [1.0 * x[0] / x[1] for x in __device_ratios]

                if mode == 0:
                    min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
                else:
                    min_ratio, max_ratio =  min(__aspect_ratios), max(__aspect_ratios)

                while 1.0 * math.ceil(w) / math.ceil(h) <= min_ratio:
                    w += 1

                while 1.0 * math.ceil(w) / math.ceil(h) >= max_ratio:
                    w -= 1

                post = Post(user=user_boject, mode=mode, photo=photo, post_at= post_date, caption=caption)
                post.save()

                from PIL import Image
                try:
                    image = Image.open(post.photo.file)
                    cropped_image = image.crop((x, y, w + x, h + y))

                    if w < 320:
                        w1 = 320
                        h1 = w1 * h / w

                        while 1.0 * math.ceil(w) / math.ceil(h) <= min_ratio:
                            w += 1

                        while 1.0 * math.ceil(w) / math.ceil(h) >= max_ratio:
                            w -= 1

                        cropped_image = cropped_image.resize((w1, int(h1)), Image.ANTIALIAS)
                    elif w > 1080:
                        w1 = 1080
                        h1 = w1 * h / w

                        while 1.0 * math.ceil(w) / math.ceil(h) <= min_ratio:
                            w += 1

                        while 1.0 * math.ceil(w) / math.ceil(h) >= max_ratio:
                            w -= 1

                        cropped_image = cropped_image.resize((w1, int(h1)), Image.ANTIALIAS)

                    cropped_image.save(post.photo.file.name)
                except Exception:
                    return redirect('/client/{}/post/'.format(cid))
            elif video:
                # fs = FileSystemStorage()
                # filename = fs.save(video.name, video)
                post = Post(user=user_boject, mode=mode, video=video, post_at=post_date, caption=caption)
                post.save()

        return redirect('/client/{}/post/list/'.format(cid))


def get_post(pid):
    try:
        post = Post.objects.get(pk=pid)
    except Post.DoesNotExist:
        post = None
    return post


class ClientScheduledPostListView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if request.user.is_staff:
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(user__cid=client)

        return render(request, 'post/list.html', {'posts': posts})


class ClientScheduledPostDeleteView(TemplateView):

    def get(self, request, cid, pid):
        client = get_client(cid)
        post = get_post(pid)

        if not (post and client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if post.photo:
            if os.path.isfile(post.photo.path):
                os.remove(post.photo.path)
        if post.video:
            if os.path.isfile(post.video.path):
                os.remove(post.video.path)

        post.delete()
        return redirect('/client/{}/post/list/'.format(cid))


class ClientPaymentHistory(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if request.user.is_staff:
            payments = Payment.objects.all()
        else:
            payments = Payment.objects.filter(cid=client)

        from user.views import get_user
        for payment in payments:
            payment_items = payment.items.get('list', [])
            for item in payment_items:
                user = get_user(item['uid'])
                item['user'] = user

        return render(request, 'client/paymentHistory.html', {'payments': payments})


def switch_client(client):
    if client.marketer:
        client.marketer = False
    else:
        client.marketer = True
    client.save()
    return client


class ClientSwitchUsageView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        switch_client(client)
        return HttpResponse('done')


class ListOFClientsView(TemplateView):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        clients = Client.objects.all()

        return render(request, 'marketer/list.html', {'clients': clients})

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        cids = request.POST.getlist('clients[]', None)

        errors = []
        if not cids:
            errors.append('کاربری انتخاب نشده است')

        for cid in cids:
            client = get_client(int(cid))
            if client:
                switch_client(client)
            else:
                errors.append('کاربر با شناسه {} وجود ندارد.'.format(cid))

        clients = Client.objects.all()

        return render(request, 'marketer/list.html', {'clients': clients, 'errors': errors})


class MarketerDetailView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if not client.marketer:
            return HttpResponse('اکانت شما از نوع بازاریاب نیست')

        return render(request, 'marketer/detail.html', {'client': client})


class MarketersManagementView(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        marketers = Client.objects.filter(marketer=True)

        return render(request, 'marketer/manage.html', {'marketers': marketers})

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        errors = []

        mid = request.POST.get('id', None)
        if not mid:
            errors.append('شناسه بازاریاب وارد نشده است.')
        else:
            mid = int(mid)

        profit = request.POST.get('profit', None)
        if not profit:
            errors.append('درصد سود بازاریاب وارد نشده است.')
        else:
            profit = int(profit)

        if profit > 100 or profit < 0:
            errors.append('درصد سود بازاریاب وارد شده صحیح نیست.')

        income = request.POST.get('income', None)
        if not income:
            errors.append('میزان درآمد بازاریاب وارد نشده است.')
        else:
            income = int(income)

        if len(errors) == 0:
            marketer = get_client(mid)
            if not marketer:
                errors.append('شناسه بازاریاب اشتباه است.')
            else:
                marketer.income = income
                marketer.participation = profit
                marketer.save()

        marketers = Client.objects.filter(marketer=True)

        return render(request, 'marketer/manage.html', {'marketers': marketers, 'errors': errors})


class ClientTradeChargeView(TemplateView):

    def get(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return redirect_to_dashboard(request, tradeMessage=[''])

    def post(self, request, cid):
        client = get_client(cid)
        if not (client and (request.user == client or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        if client.is_staff or request.user.is_staff:
            users = User.objects.all()
        else:
            users = User.objects.filter(cid=client)

        form = TradeForm(request.POST)
        if form.is_valid():
            from user.views import get_user, show_user_charge

            from_user = form.cleaned_data['from_user']
            from_user = get_user(int(from_user))
            to_user = form.cleaned_data['to_user']
            to_user = get_user(int(to_user))
            days = form.cleaned_data['days']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            errors = []
            if from_user == to_user:
                errors.append('مبدا و مقصد نمی تواند شبیه به هم باشد.')

            seconds = days*24*3600 + hours*3600 + minutes*60

            if seconds == 0:
                errors.append('مدت زمان انتقالی نمیتواند صفر باشد.')

            if seconds > show_user_charge(from_user):
                errors.append('شارژ اکانت مبدا کافی نیست.')

            if len(errors) == 0:
                from_user.charge -= seconds
                to_user.charge += seconds
                from_user.save()
                to_user.save()
                return redirect('/client/dashboard/')

            return redirect_to_dashboard(request, tradeMessage=errors)
        return redirect_to_dashboard(request, tradeMessage=[form.errors])


class ClientManageUsersChargesView(TemplateView):

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        users = User.objects.all()

        return render(request, 'client/manageUserCharges.html', {'instagramUsers': users})

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        uid = request.POST.get('id', None)
        charge = request.POST.get('charge', None)

        errors = []

        if not uid:
            errors.append('لطفا یک یوزر انتخاب کنید.')
        elif not charge:
            errors.append('لطفا شارژ موردنظرتان را وارد کنید.')

        from user.views import get_user
        user = get_user(uid)

        if not user:
            errors.append('یوزر انتخاب شده معتبر نیست.')

        if len(errors) == 0:

            user.charge = charge

            if user.status == -300:
                user.status = 100

            user.save()

        users = User.objects.all()

        return render(request, 'client/manageUserCharges.html', {'instagramUsers': users, 'errors': errors})
