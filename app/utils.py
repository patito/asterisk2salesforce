#!/usr/bin/python


def get_number_term(phone):
    '''
    Returns wildcarded version of phonenumber.
    Strips +/00 off of the beginning, and the next
    two digits to account for country codes
    '''

    if (phone.startswith('0') and not phone.startswith('00')):
        stripTwo = False
    else:
        stripTwo = True

    number = phone.lstrip('+')
    number = number.lstrip('00')
    if stripTwo:
        number = number[2:len(number)]
    term = '%'
    for digit in number:
        term += (digit + "%")
    return term
