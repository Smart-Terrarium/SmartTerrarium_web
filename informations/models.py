from django.db import models

# Create your models here.


class BasicAnimalInformation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False  # To oznacza, że Django nie będzie tworzyć tabeli w bazie danych


class MoreAnimalsInfo(models.Model):
    pet = models.OneToOneField('BasicAnimalInformation', on_delete=models.CASCADE, related_name='more_info')
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_min = models.DecimalField(max_digits=5, decimal_places=2)
    humidity_max = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"More info for {self.pet.name}"

    class Meta:
        managed = False  # To oznacza, że Django nie będzie tworzyć tabeli w bazie danych