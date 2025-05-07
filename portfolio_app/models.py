from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50)
    icon_class = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Skill)
    image = models.ImageField(upload_to='projects/')
    url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class Experience(models.Model):
    EXPERIENCE_TYPES = (
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('volunteer', 'Volunteer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"