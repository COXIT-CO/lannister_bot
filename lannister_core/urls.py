"""lannister_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

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
                path("workers/", include("api_workers.urls")),
                path("requests/", include("lannister_requests.urls")),
                path("roles/", include("lannister_roles.urls")),
            ]
        ),
    ),
]
