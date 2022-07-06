from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

"""
NOTE: following urls are used for building out the skeleton
      and should be adjusted when LAN-53 (API endpoints) is finalized and agreed upon
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("auth/", include("lannister_auth.urls")),
                path("slack/", include("lannister_slack.urls")),
                path(
                    "schema",
                    get_schema_view(
                        title="el-shopperinjoAPI",
                        description="api schema",
                        version="1.0.0",
                    ),
                    name="openapi_schema",
                ),
                path("docs/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "docs/swagger-ui/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
            ]
        ),
    ),
]
