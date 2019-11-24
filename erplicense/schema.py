import graphene
from graphene_django import DjangoObjectType
from .models import Modules, License, CompanyUsers
from core.models import Company, CompanyDatabase
from graphql_jwt.decorators import login_required
from common_utils.switch_database import SwitchDatabase
from django.core.management import call_command
from django.db import transaction, connections, connection, utils
from graphql import GraphQLError


class ModuleType(DjangoObjectType):
    class Meta:
        model = Modules


class LicenseType(DjangoObjectType):
    class Meta:
        model = License


class BulkInputType(graphene.InputObjectType):
    module = graphene.Int(required=True)
    type = graphene.String(required=True)
    duration = graphene.Int(required=True)


class Query(graphene.ObjectType):
    modules = graphene.List(ModuleType)

    def resolve_modules(self, info, **kwargs):
        return Modules.objects.all()


class CreateLicense(graphene.Mutation):
    license = graphene.List(LicenseType)

    class Arguments:
        checkout = graphene.List(BulkInputType)

    @login_required
    def mutate(self, info, checkout):
        current_user = info.context.user or None
        company = Company.objects.filter(user=current_user).first()
        if company is None:
            raise GraphQLError("Please create a company first!")

        licenses = []

        for c in checkout:
            app = Modules.objects.filter(id=c.module).first()
            if app is None:
                raise GraphQLError("No such module/app found!")

            check_license = License.objects.filter(company=company, module=app).first()
            if check_license is not None:
                raise GraphQLError("License already exists! Please upgrade the package to extend!")

            db = CompanyDatabase.objects.filter(company=company).first()
            if db is None:
                raise GraphQLError("No database found! Please contact support center!")

            with transaction.atomic():
                license = License(
                    company=company,
                    created_by=current_user,
                    module=app,
                    type=c.type,
                    duration=c.duration,
                )
                license.save()
                licenses.append(license)

                company_user = CompanyUsers(
                    company=company,
                    user=current_user,
                    module=app,
                    is_owner=True
                )
                company_user.save()

            SwitchDatabase.switch(db.db_name)
            try:
                cursor = connections[db.db_name].cursor()
            except utils.OperationalError:
                with connection.cursor() as cursor:
                    cursor.execute("CREATE DATABASE company_" + str(company.id))
            except:
                GraphQLError("Something went wrong! Please contact the support center!")
            finally:
                call_command('migrate', '--database=' + db.db_name)
                call_command('init_drmp', license.id)
                cursor.close()

        return CreateLicense(license=licenses)


class Mutation(graphene.ObjectType):
    create_license = CreateLicense.Field()