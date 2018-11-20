from django.db import models


class Recipe(models.Model):
    name = models.TextField()


class Instruction(models.Model):
    step = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
