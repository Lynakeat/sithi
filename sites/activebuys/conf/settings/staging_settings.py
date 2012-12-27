DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'activebuys_staging',
        'USER': 'activebuys_u',
        'PASSWORD': 'V@hss!hr*@G2qdoj2m4x',
    }
}

MEDIA_URL = 'http://staging.activebuys.com/static/'

FOXYCART_SHOP_NAME = 'activebuys'
FOXYCART_URL = 'https://activebuys.foxycart.com/'
FOXYCART_CDN_URL = 'http://cdn.foxycart.com/activebuys/'
FOXYCART_API_URL = FOXYCART_URL + 'api'
FOXYCART_API_KEY = "sQgUGuCzuHCXAFw8irjTI6EbJ6v16xhnhn8TIEm7dPYHpqGBGQlgQUluQGkL"

ADMINS = (
    ('shannon', 'smcoll@gmail.com'),
)
MANAGERS = ADMINS