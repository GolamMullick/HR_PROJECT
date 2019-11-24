from django.db import connections
from decouple import config
from graphql import GraphQLError
from core.models import Company, CompanyDatabase
from users.models import CompanyUsers


class SwitchDatabase:

    @classmethod
    def switch(self, db_name):
        newDatabase = {}
        newDatabase['ENGINE'] = config('DATABASE_ENGINE', cast=str)
        newDatabase['NAME'] = db_name
        newDatabase['USER'] = config('DATABASE_USER', cast=str)
        newDatabase['PASSWORD'] = config('DATABASE_PASSWORD', cast=str)
        newDatabase['HOST'] = config('DATABASE_HOST', cast=str)
        newDatabase['PORT'] = config('DATABASE_PORT', cast=int)
        connections.databases[db_name] = newDatabase

    @classmethod
    def user_db(self, user):
        if user.is_anonymous:
            raise GraphQLError("Login required!")

        company = Company.objects.filter(user_id=user.id).first()

        if company is None:
            raise GraphQLError("Company info not found!")

        db = CompanyDatabase.objects.filter(company_id=company.id).first()

        if db is None:
            raise GraphQLError("No database found for the company!")

        return db.db_name

    @classmethod
    def company_domain(self, domain):
        if domain is None:
            raise GraphQLError("Please provide company domain!")

        company = Company.objects.filter(domain=domain).first()
        if company is None:
            raise GraphQLError("Provided company domain doesn't exist!")

        return company

    @classmethod
    def company_database(self, domain):
        if domain is None:
            raise GraphQLError("Please provide company domain!")

        company = Company.objects.filter(domain=domain).first()
        if company is None:
            raise GraphQLError("Provided company domain doesn't exist!")

        db = CompanyDatabase.objects.filter(company=company).first()
        if db is None:
            raise GraphQLError("No database found!")

        self.switch(db.db_name)

        return db.db_name

    @classmethod
    def company_user(self, domain, user):
        if domain is None:
            raise GraphQLError("Please provide company domain!")

        company = Company.objects.filter(domain=domain).first()
        if company is None:
            raise GraphQLError("Provided company domain doesn't exist!")

        if user is None:
            raise GraphQLError("No user data provided!")

        db = CompanyDatabase.objects.filter(company=company).first()
        if db is None:
            raise GraphQLError("No database found!")

        self.switch(db.db_name)

        check_user = CompanyUsers.objects.using(db.db_name).filter(user_id=user.id).first()
        if check_user is None:
            raise GraphQLError("User not found!")

        return db.db_name
