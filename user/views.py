from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from .models import User
import instagram_web_api
import datetime
from django.utils import timezone
import json, requests
from client.forms import AddUserForm, AddUserStep2Form, AddUserStep3Form
from website.settings import SERVER_URL
from django.http import JsonResponse
from .functions import searchUser, searchLocation


def get_user(uid):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    return user


class DeleteUserView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)

        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        user.delete()
        return redirect('/client/dashboard/')


class UserSettingView(TemplateView):
    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return render(request, 'user/settingview.html', {'user': user})


def item_is_in_efficiency(text, key, json_items):
    index = 0
    if key == 'users':
        for value in json_items[key]:
            if value['pk'] == text:
                return index
            index += 1
        return False

    for value in json_items[key]:
        if value['text'] == text:
            return index
        index += 1
    return False


class UserSettingEditView(TemplateView):
    def get(self, request, uid):
        user = get_user(uid)

        if not (user and (request.user == user.cid or (request.user.is_staff or (request.user.marketer and request.user == user.cid.parent)))):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        get_insta_info2(uid) # to update username in case of change in username

        limit_list = list(range(0, 4200, 200))

        try:
            user.setting['follow']['limits'] *= 200
        except:
            pass

        return render(request, 'user/setting.html', {'instagramUser': user, 'range': limit_list})

    def post(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or (
                request.user.is_staff or (request.user.marketer and request.user == user.cid.parent)))):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        speedMode = int(request.POST.get('speed'))
        flwFlag = True if request.POST.get('flwFlag') else False
        unflwFlag = True if request.POST.get('unflwFlag') else False
        likeFlag = True if request.POST.get('likeFlag') else False
        commentFlag = True if request.POST.get('commentFlag') else False
        directFlag = True if request.POST.get('directFlag') else False
        commentsLikeFlag = True if request.POST.get('commentsLikeFlag') else False

        flwPerHour = int(request.POST.get('flwPerHour'))
        unflwPerHour = int(request.POST.get('unflwPerHour'))
        likePerHour = int(request.POST.get('likePerHour'))
        commentPerHour = int(request.POST.get('commentPerHour'))
        directPerHour = int(request.POST.get('directPerHour'))
        commentsLikePerHour = int(request.POST.get('commentsLikePerHour'))

        usernames = request.POST.getlist('usernames[]')
        userids = request.POST.getlist('userids[]')
        targets = []

        json_efficiency = {'tags': [], 'locations': [], 'users': []}
        i = 0
        for username in usernames:
            targets.append({'userId': int(userids[i]), 'userName': usernames[i]})

            user_item = {'pk': int(userids[i]), 'userName': usernames[i], 'count': 0, 'comment': 0, 'follow': 0, 'like': 0}
            user_item_index = item_is_in_efficiency(user_item['pk'], 'users', user.json_efficiency)
            if user_item_index is False:
                json_efficiency['users'].append(user_item)
            else:
                json_efficiency['users'].append(user.json_efficiency['users'][user_item_index])
            i += 1

        temp_tags = request.POST.getlist('tags[]')
        pktags = request.POST.getlist('pktags[]')
        tags = []
        i = 0
        for tag in temp_tags:
            tags.append({'text': temp_tags[i], 'pk': pktags[i], 'mode': 'tag'})

            tag_item = {'text': temp_tags[i], 'pk': pktags[i], 'count': 0, 'comment': 0, 'follow': 0, 'like': 0}
            tag_item_index = item_is_in_efficiency(tag_item['text'], 'tags', user.json_efficiency)
            if tag_item_index is False:
                json_efficiency['tags'].append(tag_item)
            else:
                json_efficiency['tags'].append(user.json_efficiency['tags'][tag_item_index])

            i += 1

        temp_locations = request.POST.getlist('locations[]')
        pklocations = request.POST.getlist('pklocations[]')
        i = 0
        for location in temp_locations:
            tags.append({'text': temp_locations[i], 'pk': int(pklocations[i]), 'mode': 'location'})

            location_item = {'text': temp_locations[i], 'pk': int(pklocations[i]), 'count': 0, 'comment': 0, 'follow': 0, 'like': 0}
            location_item_index = item_is_in_efficiency(location_item['text'], 'locations', user.json_efficiency)
            if location_item_index is False:
                json_efficiency['locations'].append(location_item)
            else:
                json_efficiency['locations'].append(user.json_efficiency['locations'][location_item_index])

            i += 1

        commentsLikeMode = int(request.POST.get('commentslikeMode'))
        commentsLike = {'mode': commentsLikeMode, 'dontTryAgain': False}

        followMode = int(request.POST.get('followMode'))
        flwers1 = int(request.POST.get('followFlwers1'))
        flwers2 = int(request.POST.get('followFlwers2'))
        flwing1 = int(request.POST.get('followFlwing1'))
        flwing2 = int(request.POST.get('followFlwing2'))
        posts1 = int(request.POST.get('followposts1'))
        posts2 = int(request.POST.get('followposts2'))
        gender = int(request.POST.get('followGender'))
        doseNotFlwBusiness = True if request.POST.get('doseNotFlwBusiness') else False
        flwPrivate = True if request.POST.get('followPrivate') else False
        flwPublic = True if request.POST.get('followPublic') else False
        flwHasPic = True if request.POST.get('followHasPic') else False
        dontTryAgain = True if request.POST.get('followDontTryAgain') else False
        limits = int(request.POST.get('followLimit', 0)) / 200
        follow = {'mode': followMode, 'flwers': [flwers1, flwers2], 'flwing': [flwing1, flwing2],
                  'posts': [posts1, posts2], 'hasPic': flwHasPic, 'gender': gender, 'doseNotFlwBusiness': doseNotFlwBusiness,
                  'flwPrivate': flwPrivate, 'flwPublic': flwPublic, 'dontTryAgain': dontTryAgain, 'limits': limits}

        likeMode = int(request.POST.get('likeMode'))
        likeLikeAfterFlw = True if request.POST.get('likeLikeAfterFlw') else False
        likeLikes1 = int(request.POST.get('likeLikes1'))
        likeLikes2 = int(request.POST.get('likeLikes2'))
        likecomments1 = int(request.POST.get('likecomments1'))
        likecomments2 = int(request.POST.get('likecomments2'))
        like = {'mode': likeMode, 'likeAfterFlw': likeLikeAfterFlw, 'likes': [likeLikes1, likeLikes2],
                'comments': [likecomments1, likecomments2], 'dontTryAgain': False}

        commentCommentAfterFlw = True if request.POST.get('commentCommentAfterFlw') else False
        commentDontTryAgain = True if request.POST.get('commentDontTryAgain') else False
        commentList = request.POST.getlist('comments[]')
        comment = {'mode': likeMode, 'commentAfterFlw': commentCommentAfterFlw,  'likes': like['likes'],
                   'comments': like['comments'], 'commentList': commentList, 'dontTryAgain': commentDontTryAgain,}

        unfollowStartFlwing = request.POST.get('unfollowStartFlwing')
        if (unfollowStartFlwing == ''):
            unfollowStartFlwing = 500
        else:
            unfollowStartFlwing = int(unfollowStartFlwing)

        unfollowMode = int(request.POST.get('unfollowMode'))
        unfollowTime = int(request.POST.get('unfollowTime'))

        whitelist_usernames = request.POST.getlist('whitelistUsername[]')
        whutelist_ids = request.POST.getlist('whitelistId[]')
        white_targets = []
        i = 0
        for username in whitelist_usernames:
            white_targets.append({'userId': int(whutelist_ids[i]), 'userName': whitelist_usernames[i]})
            i += 1
        unfollow = {'startFlwing': unfollowStartFlwing, 'mode': unfollowMode, 'time': unfollowTime, 'whiteList': white_targets}

        directs = request.POST.getlist('directs[]', [])
        sendDirectToAll = True if request.POST.get('directSendToAll') else False

        if sendDirectToAll:
            directPerHour = 60
            directFlag = True

        direct = {'messageList': directs, 'sendToAll': sendDirectToAll}

        copyPosts = True if request.POST.get('copyPosts') else False

        if copyPosts:
            copyCaption = True if request.POST.get('copyCaption') else False
        else:
            copyCaption = False

        if copyCaption:
            caption = ''
        else:
            caption = request.POST.get('caption', '')

        post = {'copyPosts': copyPosts, 'copyCaption': copyCaption, 'caption': caption}

        targetpost_ids = request.POST.getlist('userTargetid[]', [])
        targetpost_usernames = request.POST.getlist('userTargetname[]', [])
        targetposts = []
        i = 0
        for username in targetpost_usernames:
            targetposts.append({'userId': int(targetpost_ids[i]), 'userName': targetpost_usernames[i]})
            i += 1

        user_setting = {
            "flwFlag": flwFlag,
            "tags": tags,
            "unflwFlag": unflwFlag,
            "likeFlag": likeFlag,
            "commentFlag": commentFlag,
            "directFlag": directFlag,
            "commentsLikeFlag": commentsLikeFlag,
            "flwPerHour": flwPerHour,
            "unflwPerHour": unflwPerHour,
            "likePerHour": likePerHour,
            "commentPerHour": commentPerHour,
            "directPerHour": directPerHour,
            "commentsLikePerHour": commentsLikePerHour,
            "targets": targets,
            "commentsLike": commentsLike,
            "follow": follow,
            "like": like,
            "comment": comment,
            "unfollow": unfollow,
            "direct": direct,
            "speed": speedMode,
            "post": post,
            "targetPosts": targetposts,
        }

        user.json_efficiency = json_efficiency
        user.setting = user_setting
        user.save()

        limit_list = list(range(0, 4200, 200))

        try:
            user.setting['follow']['limits'] *= 200
        except:
            pass

        return render(request, 'user/setting.html', {'instagramUser': user, 'range': limit_list})


def get_insta_info(username):
    try:
        insta_info = instagram_web_api.Client()
        insta_info = insta_info.user_info2(username)
    except instagram_web_api.ClientError:
        insta_info = {}

    return insta_info


def update_user_username(uid, response):
    user = get_user(uid)
    if user and user.username != response['username']:
        user.username = response['username']
        user.save()


def update_user_username_by_username(uid, username):
    user = get_user(uid)
    if user and user.username != username:
        user.username = username
        user.save()


def get_insta_info2(uid):  # not working anymore
    try:
        response = requests.get('https://i.instagram.com/api/v1/users/{}/info/'.format(uid))
        response = json.loads(response.text)
        response = response['user']
        update_user_username(uid, response)
        return response
    except Exception:
        return {}


class UserDetailView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        insta_info = get_insta_info(user.username)
        return render(request, 'user/detail.html',  {'user': user, 'insta_info': insta_info})


class UserChartView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return render(request, 'user/chart.html', {'user': user})


def update_user_charge(user):
    user_start_time = user.start_time.timestamp()
    now = datetime.datetime.now().timestamp()

    d = now - user_start_time
    d = str(d).split('.')[0]
    d = int(d)

    user_charge = user.charge
    user_charge = user_charge - d

    if user_charge < 0:
        user.status = -300  # stop user
        user_charge = 0

    if user.charge > 0 and user.status == -300:
        user.status = 100

    user.start_time = timezone.now()
    user.charge = user_charge
    user.save()

    return user_charge


def show_user_charge(user):  # show current user charge (updates the charge if necessary).
    if not user:
        return HttpResponse("user not found!")

    if user.status == 0:
        update_user_charge(user)

    return user.charge


class UserUpdateChargeView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)
        if not user:
            return HttpResponse("user not found!")

        if user.status == 0:
            update_user_charge(user)

        return HttpResponse(user.charge)


def start_user(user):
    if user.charge > 0:
        user.status = 1
        user.start_time = timezone.now()
        user.save()
        return True
    user.status = -300
    user.save()
    return False


class UserStartView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        status = user.status

        if status == 100:
            if start_user(user):
                return HttpResponse('user started!')
            else:
                return HttpResponse('user is out of charge!')
        elif status == 1 or status == 0:
            return HttpResponse("user is already started!")
        elif status == -100:
            return HttpResponse("redirect to user relogin page")
        elif status == -300:
            if user.charge > 0 and start_user(user):
                return HttpResponse('user started!')
            return HttpResponse('user is out of charge!')
        else:
            return HttpResponse("error non valid status!")

        return HttpResponse("cant reach here!")


def stop_user(user):
    user.status = 100
    user.start_time = timezone.now()
    user.save()
    return True


class UserStopView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)

        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        status = user.status

        if status == 100:
            return HttpResponse('user is already stopped!')
        elif status == 1 or status == 0:
            stop_user(user)
            return HttpResponse("user stopped!")
        elif status == -100:
            return HttpResponse('user is already stopped (user is logged out).')
        elif status == -300:
            return HttpResponse('user is already stopped (user is out of charge).')
        else:
            return HttpResponse("error non valid status!")

        return HttpResponse("cant reach here!")


def login_user(response, uid):
    cookie = response.get('cookie', '')
    phone_info = response.get('phone_info', '')
    user = get_user(uid)
    if user:
        user.cookie = cookie
        user.phone_info = phone_info
        user.status = 100
        user.save()
        return user
    return None


class UserLoginView(TemplateView):
    def get(self, request, uid):
        user = get_user(uid)
        get_insta_info2(uid) # to update username
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserForm()
        return render(request, 'user/login.html', {'form': form, 'instagramUser': user})

    def post(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username != user.username:
                return render(request, 'user/login.html', {'form': form, 'error':
                                                    'نام کاربری با شناسه یوزر همخوانی ندارد.', 'instagramUser': user})

            try:
                response = requests.post(SERVER_URL,
                                         {'data': "{},{},{}".format(1, username, password)}, timeout=30)
            except Exception:
                return render(request, 'user/login.html', {'form': form, 'error': 'اشکال در اتصال به سرور',
                                                           'instagramUser': user})

            try:
                response = json.loads(response.text)
            except ValueError:
                return render(request, 'user/login.html', {'form': form, 'error': 'اشکال در سرور',
                                                           'instagramUser': user})

            status = response.get('status', None)

            if status == 'ok':
                user = login_user(response, uid)
                if user:
                    return redirect('/client/dashboard/')
                else:
                    return render(request, 'user/login.html', {'form': form, 'error': 'اشکال در ذخیره سازی یوزر',
                                                               'instagramUser': user})
            elif status == 'fail':
                error = response.get('message', '')
                if "The password you entered is incorrect" in error:
                    error = "پسورد وارد شده صحیح نیست."

                return render(request, 'user/login.html', {'form': form, 'error': error,
                                                           'instagramUser': user})
            elif status == 'challenge':
                choices = response.get('choices', [])
                form2 = AddUserStep2Form(initial={'username': username})
                return render(request, 'user/login2.html', {'form': form2, 'choices': choices, 'instagramUser': user})

            return JsonResponse(response)
        return render(request, 'user/login.html', {'form': form, 'error': ''})


class UserLogin2View(TemplateView):
    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        return redirect('/user/{}/login/'.format(uid))

    def post(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        form = AddUserStep2Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            choice = form.cleaned_data['choice']

            if username != user.username:
                return render(request, 'user/login.html', {'form': form, 'error':
                                                    'نام کاربری با شناسه یوزر همخوانی ندارد.', 'instagramUser': user})

            response = requests.post(SERVER_URL,
                                     {'data': "{},{},{}".format(2, username, choice)}, timeout=30)

            try:
                response = json.loads(response.text)
            except ValueError:
                return render(request, 'user/login.html', {'form': form, 'error': "اشکال در سرور",
                                                              'instagramUser': user})

            status = response.get('status', None)

            if status == 'ok':
                form2 = AddUserStep3Form(initial={'username': username})
                return render(request, 'user/login3.html', {'form': form2, 'instagramUser': user})
            else:
                return redirect('/user/{}/login/'.format(uid))

            return JsonResponse(response)
        return HttpResponse("QWE")  # TODO: handle this


class UserLogin3View(TemplateView):
    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        return redirect('/user/{}/login/'.format(uid))

    def post(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page
        form = AddUserStep3Form(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            code = form.cleaned_data['code']

            if username != user.username:
                return render(request, 'user/login.html', {'form': form, 'error':
                                                    'نام کاربری با شناسه یوزر همخوانی ندارد.', 'instagramUser': user})

            response = requests.post(SERVER_URL,
                                     {'data': "{},{},{}".format(3, username, code)}, timeout=30)

            try:
                response = json.loads(response.text)
            except ValueError:
                return render(request, 'user/login.html', {'form': form, 'error': "اشکال در سرور",
                                                              'instagramUser': user})

            status = response.get('status', None)
            error = response.get('msg', '')

            if status == 'ok':
                user = login_user(response, uid)
                return redirect('/client/dashboard/')
            elif status == 'fail':
                form2 = AddUserStep3Form(initial={'username': username})
                return render(request, 'user/login3.html', {'form': form2, 'instagramUser': user, 'error': error})
            else:
                return redirect('/user/{}/login/'.format(uid))

        return HttpResponse("مشکل نا مشخص")


class UserActivityView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        return render(request, 'user/activity.html', {'instagramUser': user})


class UserSearchUsersView(TemplateView):

    def get(self, request, uid, search_string):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        try:
            result = searchUser(user.cookie, user.setting, search_string)
        except Exception as e:
            return HttpResponse(str(e))
        if type(result) != type([]) and result.get("error", None) == "نیاز به لاگین مجدد":
            user.status = -100
            user.save()
        return JsonResponse(result, safe=False)


class UserSearchLocationsView(TemplateView):

    def get(self, request, uid, search_string):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        try:
            result = searchLocation(user.cookie, user.setting, search_string)
        except Exception as e:
            return HttpResponse(str(e))

        if type(result) != type([]) and result.get("error", None) == "نیاز به لاگین مجدد":
            user.status = -100
            user.save()
        return JsonResponse(result, safe=False)


class UserEfficiencyView(TemplateView):

    def get(self, request, uid):
        user = get_user(uid)
        if not (user and (request.user == user.cid or request.user.is_staff)):
            return HttpResponse("دسترسی مجاز نیست")  # TODO: redirect to error page

        for key in user.json_efficiency:
            for item in user.json_efficiency[key]:
                try:
                    actions = 0.6 * item['follow'] + 0.6 * item['like'] + 0.6 * item['comment']
                    if actions == 0:
                        item['total'] = 0
                    else:
                        item['total'] = item['count'] * 100 / actions
                        item['total'] = round(item['total'], 2)
                        if item['total'] > 100:
                            item['total'] = 100
                except KeyError:
                    item['total'] = 0

                if item['total'] < 5:
                    item['quality'] = 'بد'
                elif 5 <= item['total'] < 20:
                    item['quality'] = 'خوب'
                else:
                    item['quality'] = 'عالی'

        return render(request, 'user/efficiency.html', {'instagramUser': user})