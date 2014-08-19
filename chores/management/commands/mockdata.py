from chores import models
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Makes mockdata'

    def handle(self, *args, **options):
      my_house= models.House.objects.create(
        name="Pimlico Palace",
        address="2781 Pimlico Crescent",
        recurs="sunday"
      )

      models.Chore.objects.create(
        name="Garbage",
        description="Garbage",
        house=my_house
      )
      models.Chore.objects.create(
        name="Vacuuming",
        description="Vacuuming",
        house=my_house
      )
      models.Chore.objects.create(
        name="Bathrooms",
        description="Bathrooms",
        house=my_house
      )
      models.Chore.objects.create(
        name="Kitchen",
        description="Kitchen",
        house=my_house
      )
