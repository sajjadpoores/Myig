from instagram_private_api import Client, ClientConnectionError, ClientCookieExpiredError
import base64 , json


def decodeCookie(cookie):
    data = cookie.encode("utf-8")
    data = base64.b64decode(data)
    return data


def isLogin(cookie, setting):
    cookie = decodeCookie(cookie)
    setting = json.loads(setting)
    user = Client("none", "none", cookie=cookie, setting=setting)
    for i in range(3):
        try:
            user.current_user()
            return True
        except ClientConnectionError:
            continue
        except:
            return False
    return False


def searchUser(cookie, setting, userName):
    cookie = decodeCookie(cookie)
    # setting = json.loads(setting)
    try:
        user = Client("none", "none", cookie=cookie, setting=setting)
        for i in range(3):
            try:
                out = user.search_users(userName, rank_token=user.generate_uuid())
                out = list(map(lambda x: {"userId": x["pk"], "username": x["username"],"pic_url": x["profile_pic_url"],
                                          'followers': x["follower_count"]}, out["users"]))
                return out
            except ClientCookieExpiredError:
                return {"error": "نیاز به لاگین مجدد"}
    except ClientCookieExpiredError:
        return {"error": "نیاز به لاگین مجدد"}

    return []


def searchLocation(cookie, setting, location):
    try:
        cookie = decodeCookie(cookie)
        # setting = json.loads(setting)
        user = Client("none", "none", cookie=cookie, setting=setting)
        for i in range(3):
            try:
                out = user.location_fb_search(location, rank_token=user.generate_uuid())
                out = list(map(lambda x: {"locationId":x["location"]["pk"],"name":x["location"]["name"]},out["items"]))
                return out
            except ClientCookieExpiredError:
                return {"error": "نیاز به لاگین مجدد"}
    except ClientCookieExpiredError:
        return {"error": "نیاز به لاگین مجدد"}
    return []