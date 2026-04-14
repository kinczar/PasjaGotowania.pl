from django import template

register = template.Library();

@register.simple_tag
def get_links():
    return [{
        'name': 'Strona główna',
        'href': '/',
        'icon': 'fa-house',
    }, {
        'name': 'Przepisy',
        'href': '/recipes',
        'icon': 'fa-utensils',
    }, {
        'name': 'Forum',
        'href': '/forum',
        'icon': 'fa-comment',
    }, {
        'name': 'Dodaj wpis',
        'href': '/forum/add/',
        'icon': 'fa-plus',
    }, {
        'name': 'Zdrowie',
        'href': '/health',
        'icon': 'fa-heart',
    }]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)