from django.db import models
from django.contrib.auth.models import User
from common_utils.base_entity import BaseEntityBasicAbstract
from common_utils.file_manager import FileManager
from core.models import Company


class Modules(models.Model):
    """System generated or can only be added by super admins"""
    name = models.CharField(unique=True, max_length=191)
    slug = models.CharField(unique=True, max_length=191)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)

    @classmethod
    def load_from_json(cls, json_file_path):
        module_json_data = FileManager.read_json(json_file_path)
        modules = module_json_data.get('modules', [])
        total_modules = len(modules)
        for i, module in enumerate(modules):
            description = module['description']
            name = module['name']
            slug = module['slug']
            status = module['status']

            module_instances = cls.objects.filter(name=name, slug=slug)
            if module_instances.exists():
                module_instance = module_instances.first()
            else:
                module_instance = cls()

            module_instance.name = name
            module_instance.slug = slug
            module_instance.description = description
            module_instance.status = status
            module_instance.save()


class License(BaseEntityBasicAbstract):
    """Created/updated when a user buy/extends license for a module"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    type = models.CharField(max_length=191, null=True, blank=True)
    duration = models.IntegerField(default=30, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('company', 'module')


class CompanyUsers(BaseEntityBasicAbstract):
    """Created/updated when a user included in a company module/app"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    class Meta:
        unique_together = ('company', 'user', 'module', 'is_owner')
