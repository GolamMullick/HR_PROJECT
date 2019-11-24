from django.db import models
from django.contrib.auth.models import User
from common_utils.base_entity import BaseEntityBasicAbstract
from common_utils.file_manager import FileManager


class Country(models.Model):
    """System generated"""
    name = models.CharField(max_length=255)
    phone_code = models.CharField(max_length=255)
    short_name = models.CharField(max_length=20)

    @classmethod
    def load_from_json(cls, json_file_path):
        country_json_data = FileManager.read_json(json_file_path)
        countries = country_json_data.get('countries', [])
        total_countries = len(countries)
        for i, country in enumerate(countries):
            short_name = country['short_name']
            name = country['name']
            phone_code = country['phone_code']

            country_instances = cls.objects.filter(name=name, short_name=short_name)
            if country_instances.exists():
                country_instance = country_instances.first()
            else:
                country_instance = cls()

            country_instance.name = name
            country_instance.short_name = short_name
            country_instance.phone_code = phone_code
            country_instance.save()


class Company(BaseEntityBasicAbstract):
    """Created when user registers"""
    name = models.CharField(max_length=191)
    domain = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    portfolio = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ActivationCode(BaseEntityBasicAbstract):
    """Created when user registers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, blank=True)


class CompanyDatabase(BaseEntityBasicAbstract):
    """Created when user registers"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    db_name = models.CharField(max_length=255, unique=True)
    db_host = models.CharField(max_length=255, blank=True)
    db_port = models.CharField(max_length=255, blank=True)
    db_user = models.CharField(max_length=255, blank=True)
    db_pass = models.CharField(max_length=255, blank=True)


class ResetPassword(BaseEntityBasicAbstract):
    """Password reset table for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
