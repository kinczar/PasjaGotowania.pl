from django import template

register = template.Library();

@register.simple_tag
def get_links():
    return [{
        'name': 'Home',
        'href': '/',
        'icon': 'fa-house',
    }, {
        'name': 'Recipes',
        'href': '/recipes',
        'icon': 'fa-utensils',
    }, {
        'name': 'Forum',
        'href': '/forum',
        'icon': 'fa-comment',
    }, {
        'name': 'Add post',
        'href': '/forum/add/',
        'icon': 'fa-plus',
    }, {
        'name': 'Health',
        'href': '/health',
        'icon': 'fa-heart',
    }]