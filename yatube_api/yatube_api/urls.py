from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from api.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

