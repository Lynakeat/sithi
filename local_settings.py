
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'activebuys_pro',
        'USER': 'admin',
        'PASSWORD': 'myadmin',
    }
}

USE_TZ = True

FOXYCART_SHOP_NAME = 'activebuys'
FOXYCART_URL = 'https://activebuys.foxycart.com/'
FOXYCART_CDN_URL = 'http://cdn.foxycart.com/activebuys/'
FOXYCART_API_URL = FOXYCART_URL + 'api'
FOXYCART_API_KEY = "sQgUGuCzuHCXAFw8irjTI6EbJ6v16xhnhn8TIEm7dPYHpqGBGQlgQUluQGkL"

ADMINS = (
    ('lyna', 'lynakeat@gmail.com'),
)
MANAGERS = ADMINS



EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "yoyocam68@gmail.com"
EMAIL_HOST_PASSWORD = "tsanimol"
EMAIL_USE_TLS = True

SERVER_EMAIL = 'no-reply@activebuys.com'

