from django.urls import path
from .views import DeleteUserView, UserSettingEditView, UserSettingView, UserDetailView, UserChartView, \
    UserUpdateChargeView, UserStartView, UserStopView, UserLoginView, UserLogin2View, UserLogin3View, UserActivityView, \
    UserSearchUsersView, UserSearchLocationsView, UserEfficiencyView

urlpatterns = [
    path('<int:uid>/', UserDetailView.as_view()),
    path('<int:uid>/delete/', DeleteUserView.as_view()),

    path('<int:uid>/setting/edit/', UserSettingEditView.as_view()),
    path('<int:uid>/setting/', UserSettingView.as_view()),

    path('<int:uid>/update/', UserUpdateChargeView.as_view()),
    path('<int:uid>/start/', UserStartView.as_view()),
    path('<int:uid>/stop/', UserStopView.as_view()),

    path('<int:uid>/login/', UserLoginView.as_view()),
    path('<int:uid>/login2/', UserLogin2View.as_view()),
    path('<int:uid>/login3/', UserLogin3View.as_view()),

    path('<int:uid>/chart/', UserChartView.as_view()),
    path('<int:uid>/activity/', UserActivityView.as_view()),

    path('<int:uid>/finduser/<str:search_string>/', UserSearchUsersView.as_view()),
    path('<int:uid>/findlocation/<str:search_string>/', UserSearchLocationsView.as_view()),

    path('<int:uid>/efficiency/', UserEfficiencyView.as_view()),

]
