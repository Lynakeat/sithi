DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'activebuys',
        'USER': 'activebuys_u',
        'PASSWORD': 'V@hss!hr*@G2qdoj2m4x',
    }
}

MEDIA_URL = 'http://activebuys.com/static/'

FOXYCART_SHOP_NAME = 'activebuys-secure'
#FOXYCART_URL = 'https://activebuys-secure.foxycart.com/'
#FOXYCART_CDN_URL = 'http://cdn.foxycart.com/activebuys-secure/'
FOXYCART_URL = 'https://secure.activebuys.com/'
FOXYCART_CDN_URL = 'http://cdn.foxycart.com/secure.activebuys.com/'
FOXYCART_API_KEY = "PfD3aCCUe3swljd64D4bKTgNr14J4XyM42K4zdSHbf5rp8rmFlpg9zZruX5n"

#FOXYCART_SHOP_NAME = 'activebuys'
#FOXYCART_URL = 'https://activebuys.foxycart.com/'
#FOXYCART_CDN_URL = 'http://cdn.foxycart.com/activebuys/'
