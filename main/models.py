from django.db import models

# Create your models here.


class Report(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Issues(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    number = models.IntegerField()
    issue = models.CharField(max_length=100)
    description = models.TextField()
    recommendation = models.TextField()
    risk = models.CharField(max_length=10, choices=(
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ))
    status = models.CharField(max_length=10, choices=(
        ('open', 'Open'),
        ('closed', 'Closed'),
    ))
    proof = models.ImageField(upload_to='images/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.issue
