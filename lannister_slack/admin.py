from django.contrib import admin
from lannister_slack.models import (
    BonusRequest,
    BonusRequestsHistory,
    BonusRequestStatus,
)

# Register your models here.
admin.site.register(BonusRequest)
admin.site.register(BonusRequestsHistory)
admin.site.register(BonusRequestStatus)
