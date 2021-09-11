from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/item/', include('item.urls')),

    path('api/user/', include('user.urls')),
    path('api/', include('api.urls')),
    path('api/map/', include('map.urls')),
    path('api/skill/', include('skill.urls')),
    path('api/post/', include('post.urls')),
    path('api/guild/', include('guild.urls')),
    path('api/guide/', include('guide.urls')),
    path('api/craft/', include('craft.urls')),
    # path('api/dkp/', include('dkp.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
