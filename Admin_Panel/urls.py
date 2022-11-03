from django.urls import path
from . import views
from Juno.settings import DEBUG, STATIC_URL, STATICFILES_DIRS, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signin, name = 'signin'),
    path('index/', views.index, name = 'index'),
    path('userlist/', views.userlist, name = 'userlist'),
    path('partnerlist/', views.partnerlist, name = 'partnerlist'),
    path('user_call_detail/', views.user_call_detail, name = 'user_call_detail'),
    path('partner_call_detail/', views.partner_call_detail, name = 'partner_call_detail'),
    path('logout/', views.logout, name = 'logout'),
    path('coupons/', views.coupons, name = 'coupons'),
    path('create_coupon/', views.create_coupon, name = 'create_coupon'),
    path('missed_call/', views.user_missed_call_report, name = 'missed_call'),
    path('user_inactive/', views.user_inactive, name = 'user_inactive'),
    path('partner_inactive/', views.partner_inactive, name = 'partner_inactive'),
    path('edit/', views.edit, name = 'edit'),
    path('user_wallet/', views.user_wallet, name = 'user_wallet'),
    path('partner_wallet/', views.partner_wallet, name = 'partner_wallet'),
    path('edit_detail/', views.edit_detail, name = 'edit_detail'),
    path('daily_report/', views.daily_report, name = 'daily_report'),
    path('monthly_report/', views.monthly_report, name = 'monthly_report'),
    path('call_modal/', views.call_modal, name = 'call_modal')
]

#DataFlair
if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATICFILES_DIRS)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)