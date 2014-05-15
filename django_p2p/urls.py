from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django_p2p.views',
    # Examples:
    # url(r'^$', 'django_p2p.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "cart", name="cart"),
    url(r'^checkout/$', "checkout", name="checkout"),
    url(r'^checkout/callback-receiver/$', "p2p_callback", name="p2p_callback"),
    url(r'^checkout/thank-you/$', "thankyou", name="thankyou"),
)
