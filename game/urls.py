from django.contrib import admin
from django.urls import path, include
from home.views import home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),  # Página inicial do jogo
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
