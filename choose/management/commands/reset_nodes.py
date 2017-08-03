#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.6
from django.core.management.base import BaseCommand, CommandError
from choose import models


class Command(BaseCommand):
    help = '每周六晚上18:00重置数据库中nodes的所有者。'

    # 必须实现的方法
    def handle(self, *args, **kwargs):
        models.Nodes.objects.all().update(owner=None)