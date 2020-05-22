"""
The Database schema or model for people in Company is designed here.
This conpany model is being referenced over citizen model.
"""
from django.db import models


class Companies(models.Model):
    """
    This model save the details of Company in Paranuara.
    """
    index = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False)
    company = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.index},{self.company}"
