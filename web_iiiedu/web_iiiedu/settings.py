# Import all default settings.
from .local_settings import *
from .my_settings import *

import dj_database_url


# DATABASES = {
#     'default': dj_database_url.config(),
# }

# Static asset configuration.
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure().
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers.
ALLOWED_HOSTS = ['*']

# Turn off DEBUG mode.
DEBUG = False