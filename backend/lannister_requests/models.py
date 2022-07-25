from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from lannister_auth.models import LannisterUser, Role


class BonusRequestStatus(models.Model):
    status_name = models.CharField(max_length=45, unique=True, null=False)

    def __str__(self):
        return self.status_name

    class Meta:
        db_table = "bonus_requests_status"
        verbose_name = "Bonus status"
        verbose_name_plural = "Bonus statuses"


def set_request_status():
    """create new statuses. Get default status"""
    BonusRequestStatus.objects.get_or_create(status_name="Created")
    BonusRequestStatus.objects.get_or_create(status_name="Approved")
    BonusRequestStatus.objects.get_or_create(status_name="Rejected")
    BonusRequestStatus.objects.get_or_create(status_name="Done")
    default = BonusRequestStatus.objects.get(status_name="Created")
    return default.pk


class BonusRequest(models.Model):
    class BonusRequestType(models.TextChoices):
        REFERAL = "Referral", _("Referral")
        OVERTIME = "Overtime", _("Overtime")

    creator = models.ForeignKey(LannisterUser, on_delete=models.PROTECT)
    status = models.ForeignKey(
        "BonusRequestStatus",
        related_name="statuses",
        default=set_request_status,
        on_delete=models.CASCADE,
    )
    reviewer = models.ForeignKey(
        LannisterUser, related_name="reviewer", on_delete=models.SET_NULL, null=True
    )
    bonus_type = models.CharField(max_length=50, choices=BonusRequestType.choices)
    description = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=3, null=True)
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
        if self.reviewer == self.creator:
            raise ValueError(_("You cannot review self request."))
        self.reviewer = reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.pk} {self.creator}'s bonus request. Reviewer assigned - {self.reviewer}"

    class Meta:
        db_table = "bonus_requests"


class BonusRequestsHistory(models.Model):

    bonus_request = models.ForeignKey(
        BonusRequest, related_name="history_requests", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        BonusRequestStatus,
        related_name="history_statuses",
        on_delete=models.CASCADE,
        null=True,
    )
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Request id: {self.bonus_request.pk}, opened by {self.bonus_request.creator}"

    class Meta:
        db_table = "bonus_requests_history"
        verbose_name_plural = "Bonus requests history"


@receiver(post_save, sender=BonusRequest)
def add_status_to_history(sender, created, instance, *args, **kwargs):
    if created:
        BonusRequestsHistory.objects.create(
            bonus_request=instance,
            status=instance.status,
            updated_at=instance.updated_at,
        )
    previous = (
        BonusRequestsHistory.objects.filter(bonus_request=instance.id)
        .order_by("-updated_at")
        .first()
    )
    if previous and previous.status != instance.status:
        BonusRequestsHistory.objects.create(
            bonus_request=instance,
            status=instance.status,
            updated_at=instance.updated_at,
        )
