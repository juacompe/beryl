from django.conf import settings
import locale

def number_to_currency(number):
    locale.setlocale(locale.LC_ALL, settings.LOCALE)
    #$
    converted = unicode(locale.currency(number,grouping=True),errors='ignore')
    return converted.replace('$','')
