from django.test import TestCase
from .forms import SignupForm, LoginForm
from .models import Client


class FormTest(TestCase):

    def test_signup_form(self):
        data = {}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': '', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user@user.com'}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': 'user1', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user@user'}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': 111, 'password1': 'password@123', 'password2': 'password@123', 'email': 'user@user.com'}
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())

        data = {'username': 'user1', 'password1': 'password@123', 'password2': 'password@12', 'email': 'user@user.com'}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': 'user1', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user@user.com'}
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        data = {'username': 'user1', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user@user.com'}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': 'user2', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user@user.com'}
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_login_form(self):
        data = {}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': 'user1', 'password': 'password@123'}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

        data = {'username': 1234, 'password': 'password@123'}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())


class ViewTest(TestCase):

    def test_signup_view(self):
        # test get method
        response = self.client.get('/client/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/signup.html')

        # test post method
        client_count = Client.objects.count()
        data = {'username': 'user1', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user1@user.com'}
        response = self.client.post('/client/signup/', data)
        self.assertEqual(client_count+1, Client.objects.count())

        # test get method after user is logged in
        self.client.login(username='user1', password='password@123')
        response = self.client.get('/client/signup/')
        self.assertTemplateNotUsed(response, 'client/signup.html')

        # test post method after user is logged in
        data = {'username': 'user2', 'password1': 'password@123', 'password2': 'password@123', 'email': 'user2@user.com'}
        response = self.client.post('/client/signup/', data)
        self.assertTemplateNotUsed(response, 'client/signup.html')

    def test_login_view(self):
        # test get method
        response = self.client.get('/client/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/login.html')

        # create a user
        client = Client.objects.create_user(username='user', password='password@123', email='user@user.com')

        # test post method
        data = {'username': 'user', 'password': 'password@123'}
        last_login = client.last_login
        response = self.client.post('/client/login/', data)
        client = Client.objects.get(pk=client.pk)
        self.assertTemplateNotUsed(response, 'client/login.html')
        self.assertNotEqual(last_login, client.last_login)

        # test get method after user is logged in
        response = self.client.get('/client/login/')
        self.assertTemplateNotUsed(response, 'client/login.html')

        # test post method after user is logged in
        data = {'username': 'user', 'password': 'password@123'}
        response = self.client.post('/client/login/', data)
        self.assertTemplateNotUsed(response, 'client/login.html')

    def test_logout_view(self):
        # create a user and login
        client = Client.objects.create_user(username='user', password='password@123', email='user@user.com')
        self.client.login(username='user', password='password@123')

        # check login
        response = self.client.get('/client/login/')
        self.assertTemplateNotUsed(response, 'client/login.html')

        # do logout
        response = self.client.get('/client/logout/')

        # check logout
        response = self.client.get('/client/login/')
        self.assertTemplateUsed(response, 'client/login.html')

    def test_detail_view(self):
        # create a user and login
        client = Client.objects.create_user(username='user', password='password@123', email='user@user.com')
        self.client.login(username='user', password='password@123')

        response = self.client.get('/client/1/')
        self.assertTemplateNotUsed(response, 'client/detail.html')


    def test_users_list_view(self):
        # create a user and login
        client = Client.objects.create_user(username='user', password='password@123', email='user@user.com')
        self.client.login(username='user', password='password@123')

        response = self.client.get('/client/1/list/')
        self.assertTemplateNotUsed(response, 'client/list.html')