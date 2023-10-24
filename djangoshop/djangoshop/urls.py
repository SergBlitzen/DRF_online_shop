from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls.shop_urls')),
    path('api-token-auth/', views.obtain_auth_token),
]
