import os

environment = os.getenv('DJANGO_ENVIRONMENT', 'dev')

if environment == 'prod':
    from .prod import *
else:
    from .dev import *
