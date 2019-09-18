from django.urls import path
from .views import TicketAddView, TicketListView, TicketReplyView, TicketDetailView, TicketUnrepliedListView, \
    TicketUnseenListView

urlpatterns = [
    path('<int:cid>/', TicketAddView.as_view()),
    path('<int:cid>/<int:tid>/', TicketDetailView.as_view()),
    path('<int:cid>/list/', TicketListView.as_view()),

    path('<int:tid>/reply/', TicketReplyView.as_view()),
    path('unseen/', TicketUnseenListView.as_view()),
    path('unreplied/', TicketUnrepliedListView.as_view()),
]
