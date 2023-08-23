from django import template

register = template.Library()

@register.filter(name='format_pin')
def format_pin(pin_number):
    if pin_number > 100:
        first_digit = pin_number // 100
        second_digit = pin_number % 100
        return f"{first_digit} (DHT - {second_digit:02})"
    return pin_number
