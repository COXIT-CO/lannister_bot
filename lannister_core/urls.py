from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path(
        "api/",
        include(
            [	path("admin/", admin.site.urls),
                path("auth/", include("lannister_auth.urls")),
                path("workers/", include("api_workers.urls")),
                path("requests/", include("lannister_requests.urls")),
                path("roles/", include("lannister_roles.urls")),
                path(
                    "schema",
                    get_schema_view(
                        title="lannister",
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
