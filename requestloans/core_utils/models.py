from django.db.models import DateTimeField, Model


class TimeStampModel(Model):
    created = DateTimeField(auto_now_add=True, null=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
