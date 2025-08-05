from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    #
    # path("accounts/", include("users.urls", namespace="users")),
    path("", include("cinema.urls", namespace="cinema")),
    # path("promotion/", include("promotion.urls", namespace="promotion")),
    path("", include("booking.urls", namespace="booking")),
    # path("seo/", include("seo.urls", namespace="seo")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
