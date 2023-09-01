from django.db import models

# Create your models here.


class BasicAnimalInformation(models.Model):
    name = models.CharField(max_length=100) # Name of the animal
    description = models.TextField()        # Description of the animal

    def __str__(self):
        return self.name

    class Meta:
        managed = False  # This indicates that Django won't create a table in the database


class MoreAnimalsInfo(models.Model):
    pet = models.OneToOneField('BasicAnimalInformation', on_delete=models.CASCADE, related_name='more_info')
    # One-to-One relationship with 'BasicAnimalInformation' model
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2)  # Minimum temperature
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2)  # Maximum temperature
    humidity_min = models.DecimalField(max_digits=5, decimal_places=2)     # Minimum humidity
    humidity_max = models.DecimalField(max_digits=5, decimal_places=2)     # Maximum humidity

    def __str__(self):
        return f"More info for {self.pet.name}"  # String representation of the model

    class Meta:
        managed = False  # This indicates that Django won't create a table in the database