from django.urls import path

from translate.service.views import (
    LivelinessCheckView,
    ReadinessCheckView,
    TranslationsAPIView,
    TranslationsAPIViewV2,
)

urlpatterns = [
    path("v1/translations/<language>/", TranslationsAPIView.as_view(), name="api_translations"),
    path("v2/translations/<language>/", TranslationsAPIViewV2.as_view(), name="api_translations_v2"),
    path("status/liveliness", LivelinessCheckView.as_view(), name="status_liveliness"),
    path("status/readiness", ReadinessCheckView.as_view(), name="status_readiness"),
]
