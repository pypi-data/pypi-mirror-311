'''
Set the value of a field in a nested dictionary.
'''

from collections import OrderedDict
from icecream import ic

def set_field_value(
    data: OrderedDict,
    field: str,
    value: any,
):
    if '.' in field:
        field, rest = field.split('.', 1)
        if field not in data:
            data[field] = OrderedDict()
        set_field_value(data[field], rest, value)
    else:
        data[field] = value
