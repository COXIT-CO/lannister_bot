from django.db import models
from django.utils.translation import gettext_lazy as _
from lannister_auth.models import LannisterUser, Role

"""
NOTE: following models/managers are used for building out the skeleton
      and should be adjusted when LAN-52 (DB schema) is finalized and agreed upon
"""


class BonusRequest(models.Model):
    class BonusRequestStatus(models.TextChoices):
        CREATED = "Cr", _("Created")
        APPROVED = "Appr", _("Approved")
        REJECTED = "Rj", _("Rejected")
        DONE = "Done", _("Done")

    class BonusRequestType(models.TextChoices):
        REFERAL = "Ref", _("Referral")
        OVERTIME = "Ot", _("Overtime")

    creator = models.ForeignKey(LannisterUser, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=50,
        choices=BonusRequestStatus.choices,
        default=BonusRequestStatus.CREATED,
    )
    reviewer = models.ForeignKey(
        LannisterUser, related_name="reviewer", on_delete=models.SET_NULL, null=True
    )
    bonus_type = models.CharField(max_length=50, choices=BonusRequestType.choices)
    description = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        reviewer = LannisterUser.objects.get(username=self.reviewer.username)
        is_reviewer = Role.objects.get(id=2) in reviewer.roles.all()
        if not is_reviewer:
            raise ValueError(
                _(
                    "Selected user is not a reviewer. Select a valid user with reviewer role."
                )
            )
        self.reviewer = reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.creator}'s bonus request. Reviewer assigned - {self.reviewer}"


# TODO: implement history
