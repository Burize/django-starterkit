from ajax_select import LookupChannel
from ajax_select import register

from authentication.models import Account


@register('account_channel')
class ProductLookup(LookupChannel):
    model = Account
    search_field = 'email'
