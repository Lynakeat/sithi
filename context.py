from django.conf import settings

def get_foxycart_shop_name(request):
    return {'FOXYCART_SHOP_NAME':settings.FOXYCART_SHOP_NAME,
            'FOXYCART_URL': settings.FOXYCART_URL,
            'FOXYCART_CDN_URL': settings.FOXYCART_CDN_URL}
