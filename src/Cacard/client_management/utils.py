'''
Created on Feb 22, 2013

@author: oleg
'''
from django.contrib.auth.models import Group, User, Permission
from django.db.models import get_app, get_models


def create_client_infrastructure(client_name):
    group, created = Group.objects.get_or_create(name=client_name)
    user, created = User.objects.get_or_create(username=client_name)

    group.user_set.add(user)

    # TODO: rework this (get models from config)
    model_names=[i._meta.verbose_name
                      for i in get_models(get_app('calling_card'))]
    cacard_perms = Permission.objects.filter(
                              content_type__app_label='calling_card',
                              content_type__name__in=model_names)
    group.permissions = cacard_perms
