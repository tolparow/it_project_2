# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from uuid import uuid4
#
#
# def get_hash():
#     """
#     Unique hash generator for users.
#     This hash is used fot user identification while message sending.
#     :return: four uuid4 hex hashes in one string
#     """
#     return uuid4().hex + uuid4().hex + uuid4().hex + uuid4().hex
#
#
# class User(AbstractUser):
#     """
#     User model, to be able to customize
#     standard user model.
#     """
#     REQUIRED_FIELDS = []
#
#     secret_hash = models.CharField(
#         default=get_hash,
#         null=False,
#         max_length=65,
#         unique=True,
#     )
#
#     def __str__(self):
#         return self.first_name + ' ' + self.last_name
