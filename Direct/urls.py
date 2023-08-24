from Direct.views import inbox, Directs, SendDirect, UserSearch, NewConversation
from django.urls import path

urlpatterns = [
    path("inbox/", inbox, name="message"),
    path("direct/<username>", Directs, name="directs"),
    path("send/", SendDirect, name="send-directs"),
    path("search/", UserSearch, name="search-users"),
    path("new/<username>", NewConversation, name="conversation"),
]
