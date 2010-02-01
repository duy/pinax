from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template

#from wiki import models as wiki_models

from django.contrib import admin
admin.autodiscover()

from account.openid_consumer import PinaxConsumer
# duy
from waitinglist.forms import WaitingListEntryForm


# @@@ turn into template tag
def homepage(request):
    if request.method == "POST":
        form = WaitingListEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("waitinglist_sucess"))
    else:
        form = WaitingListEntryForm()
    return direct_to_template(request, "homepage.html", {
        "form": form,
    })


if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = "account.views.signup"
else:
    signup_view = "signup_codes.views.signup"


urlpatterns = patterns('',
# duy
#    url(r'^$', direct_to_template, {
#        "template": "homepage.html",
#    }, name="home"),

    url(r'^$', homepage, name="home"),
    url(r'^success/$', direct_to_template, {"template": "waitinglist/success.html"}, name="waitinglist_sucess"),
    
    url(r'^admin/invite_user/$', 'signup_codes.views.admin_invite_user', name="admin_invite_user"),
    url(r'^account/signup/$', "signup_codes.views.signup", name="acct_signup"),
    
    (r'^account/', include('account.urls')),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^profiles/', include('basic_profiles.urls')),
#    (r'^profiles/', include('profiles.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^announcements/', include('announcements.urls')),
    (r'^tagging_utils/', include('tagging_utils.urls')),
    #(r'^attachments/', include('attachments.urls')),
    (r'^bookmarks/', include('bookmarks.urls')),
    #(r'^tasks/', include('tasks.urls')),
    #(r'^topics/', include('topics.urls')),
    #(r'^comments/', include('threadedcomments.urls')),
    #(r'^wiki/', include('wiki.urls')),
    
    #duy
    (r'^avatar/', include('avatar.urls')),
    (r'^invitations/', include('friends_app.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^tags/', include('tag_app.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^bookmarks/firefox/', include('firefox.urls')),
# duy

#    url(r'^feeds/(?P<feedtype>\w+)/bookmarks/$', 'bookmarks.views.bookmark_feed', name='bookmark_feed'),
#    url(r'^feeds/(?P<feedtype>\w+)/bookmarks/(?P<id_slug>\d+)/$', 'bookmarks.views.bookmark_feed', name='bookmark_feed'),

#    url(r'^api/(?P<format>\w+)/bookmarks/(?P<model_name>[\d\w]+)/$', 'bookmarks.serializers.bookmarks', name="bookmark_serializer"),
#    url(r'^api/(?P<format>\w+)/bookmarks/(?P<model_name>[\d\w]+)/(?P<object_id>\d+)/$', 'bookmarks.serializers.bookmarks', name="bookmark_serializer"),

#    url(r'^api/rest/(?P<format>\w+)/bookmarks/(?P<model_name>[\d\w]+)/$', 'bookmarks.rest.bookmarks', name="bookmark_rest"),
#    url(r'^api/rest/(?P<format>\w+)/bookmarks/(?P<model_name>[\d\w]+)/(?P<object_id>[\d]+)/$', 'bookmarks.rest.bookmarks', name="bookmark_rest"),

)

# duy
from bookmarks.models import Bookmark

friends_bookmarks_kwargs = {
    "template_name": "bookmarks/friends_bookmarks.html",
    "friends_objects_function": lambda users: Bookmark.objects.filter(saved_instances__user__in=users),
    "extra_context": {
        "user_bookmarks": lambda request: Bookmark.objects.filter(saved_instances__user=request.user),
    },
}

urlpatterns += patterns('',
    url('^bookmarks/friends_bookmarks/$', 'friends_app.views.friends_objects', kwargs=friends_bookmarks_kwargs, name="friends_bookmarks"),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
