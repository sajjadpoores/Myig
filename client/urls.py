from django.urls import path
from .views import SignupView, LoginView, LogoutView, AddUserView, AddUserStep2View, AddUserStep3View, ClientDetailView,\
    ClientUserListView, ClientPayView, ClientVerifyView, ClientUserListOfAllView, ClientPlanListView, ClientPlansView, \
    ClientAddPlan, ClientEditPlan, ClientPlanDetail, ClientDashboardView, ClientDeletePlanView, ClientUserDeleteView, \
    ClientSelectUserView, ClientPrePaymentView, ClientStartAllUsersView, ClientStopAllUsersView, ClientChartsView, \
    ClientScheduledPostView, ClientScheduledPostListView, ClientScheduledPostDeleteView, ClientPaymentHistory, \
    ActivateView, ResetPassword, ChangePassword, ClientSwitchUsageView, ListOFClientsView, MarketerDetailView, \
    MarketersManagementView, RecommendView, ActivateWithLinkView, ClientTradeChargeView, ClientChangeEmailView, \
    ClientManageUsersChargesView


urlpatterns = [
    path('dashboard/', ClientDashboardView.as_view()),
    path('signup/', SignupView.as_view()),
    path('<int:cid>/signup/', RecommendView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('list/', ClientUserListOfAllView.as_view()),

    path('reset/', ResetPassword.as_view()),
    path('<int:cid>/reset/<slug:code>/', ChangePassword.as_view()),
    path('<int:cid>/activate/', ActivateView.as_view()),
    path('<int:cid>/activate/<slug:code>/', ActivateWithLinkView.as_view()),
    path('<int:cid>/email/', ClientChangeEmailView.as_view()),

    path('<int:cid>/add/', AddUserView.as_view()),
    path('<int:cid>/add2/', AddUserStep2View.as_view()),
    path('<int:cid>/add3/', AddUserStep3View.as_view()),

    path('<int:cid>/history/', ClientPaymentHistory.as_view()),

    path('<int:cid>/startall/', ClientStartAllUsersView.as_view()),
    path('<int:cid>/stopall/', ClientStopAllUsersView.as_view()),

    path('<int:cid>/', ClientDetailView.as_view()),
    path('<int:cid>/list/', ClientUserListView.as_view()),

    path('<int:cid>/charts/', ClientChartsView.as_view()),
    path('<int:cid>/<int:uid>/delete/', ClientUserDeleteView.as_view()),

    path('plan/list/', ClientPlanListView.as_view()),   # for client
    path('plan/plans/', ClientPlansView.as_view()),   # for admin
    path('plan/', ClientAddPlan.as_view()),
    path('plan/<int:pid>/', ClientPlanDetail.as_view()),
    path('plan/<int:pid>/edit/', ClientEditPlan.as_view()),
    path('plan/<int:pid>/delete/', ClientDeletePlanView.as_view()),

    path('<int:cid>/plan/<int:pid>/select/', ClientSelectUserView.as_view()),
    path('<int:cid>/plan/<int:pid>/prepay/', ClientPrePaymentView.as_view()),
    path('<int:cid>/plan/<int:pid>/pay/', ClientPayView.as_view()),
    path('<int:cid>/plan/<int:pid>/pay/<int:payid>/verify/', ClientVerifyView.as_view()),

    path('<int:cid>/post/', ClientScheduledPostView.as_view()),
    path('<int:cid>/post/list/', ClientScheduledPostListView.as_view()),
    path('<int:cid>/post/<int:pid>/delete/', ClientScheduledPostDeleteView.as_view()),

    path('<int:cid>/switch/', ClientSwitchUsageView.as_view()),

    path('all/', ListOFClientsView.as_view()),
    path('marketers/', MarketersManagementView.as_view()),
    path('<int:cid>/marketer/', MarketerDetailView.as_view()),

    path('<int:cid>/trade/', ClientTradeChargeView.as_view()),

    path('usercharges/', ClientManageUsersChargesView.as_view()),

]
