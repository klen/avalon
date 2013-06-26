from django.conf import settings

settings.configure(
    ROOT_URLCONF='tests.django_app.urls',
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'USER': '',
            'PASSWORD': '',
            'TEST_CHARSET': 'utf8',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'tests.django_app',)
)

# lint_ignore=C0110
