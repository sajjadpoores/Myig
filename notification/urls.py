from django.urls import path
from .views import GetFollowBacksView, AddFollowBackView, DeleteFollowBackView, AddBlockNotificationView,\
    GetBlockNotificationView, SeenBlockNotificationView, GetTicketNotificationView, GetTicketAndBlockNotificationView


urlpatterns = [
    path('followback/<int:cid>/', GetFollowBacksView.as_view()),
    path('followback/<int:cid>/<int:nid>/delete/', DeleteFollowBackView.as_view()),
    path('followback/<int:fuid>/<int:tuid>/', AddFollowBackView.as_view()),

    path('block/<int:uid>/<int:type>/', AddBlockNotificationView.as_view()),
    path('block/<int:cid>/', GetBlockNotificationView.as_view()),
    path('block/<int:cid>/<int:nid>/seen/', SeenBlockNotificationView.as_view()),

    path('ticket/<int:cid>/', GetTicketNotificationView.as_view()),
    path('block_ticket/<int:cid>/', GetTicketAndBlockNotificationView.as_view()),
]
