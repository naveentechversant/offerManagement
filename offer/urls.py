from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from product.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'offer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', offer_page, name='offer_list'),
    url(r'^offer/create$', offer_create, name='offer_create'),
    url(r'^offer/edit/(?P<id>\d+)$', offer_edit, name='offer_edit'),
    url(r'^offer/delete$', offer_delete, name='offer_delete'),
    url(r'^check/price$', check_product_price, name='check_product_price'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


