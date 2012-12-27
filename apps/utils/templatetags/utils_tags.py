from django import template
register = template.Library()

# @register.filter
# def truncatewords_by_chars(value, arg):
#     """Truncate the text when it exceeds a certain number of characters.
#     Delete the last word only if partial.
#     Adds '...' at the end of the text.
    
#     Example:
    
#         {{ text|truncatewords_by_chars:25 }}
#     """
#     try:
#         length = int(arg)
#     except ValueError:
#         return value
    
#     if len(value) > length:
#         if value[length:length + 1].isspace():
#             return value[:length].rstrip() + '...'
#         else:
#             return value[:length].rsplit(' ', 1)[0].rstrip() + '...'
#     else:
#         return value

@register.filter
def truncatechars(s, num):
    """
    Truncates a word after a given number of chars  
    Argument: Number of chars to truncate after
    """
    length = int(num)
    string = []
    for word in s.split():
        if len(word) > length:
            string.append(word[:length]+'...')
        else:
            string.append(word)
    return u' '.join(string)

@register.filter
def startswith(value, arg):
    """ 
    Determines whether a value starts with an argument.
    Returns True or False.
    Usage, {% if value|startswith:"arg" %}"""
    return value.startswith(arg)