from django import template

register = template.Library()


@register.filter
def format_price_range(price_range):
    min_price, max_price = price_range
    return f"{int(min_price)}₸ - {int(max_price)}₸"
