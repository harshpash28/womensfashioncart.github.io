# from django.contrib import admin
from django.urls import path
from fashioncartapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home',views.home),
    path('about',views.about),
    path('contact',views.contact),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('register',views.register),
    path('shopmore',views.shopmore),
    path('hot',views.hot),
    path('newarrivals',views.newarrivals),
    path('accessories',views.accessories),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('pdetails/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)