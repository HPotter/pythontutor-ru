from django import template


register = template.Library()


@register.filter
def getitem(mydict, mykey):
    """
    Get value from `mydict` by `mykey`. Returns None if not found
    :param mydict: dict
    :param mykey: object
    :return: object
    """
    return mydict.get(mykey, None)
