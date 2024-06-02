from .settings import *

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', None),
        'NAME': os.environ.get('DATABASE_NAME', None), 
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
        'HOST': os.environ.get('DATABASE_HOST', None), 
        'PORT': os.environ.get('DATABASE_PORT', None),
    }
}

