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
    },{
        'name': 'Forum',
        'href': '/forum',
        'icon': 'fa-comment', #look for your icon here https://fontawesome.com/search?ic=free
    },{
        'name': 'Add post',
        'href': '/forum/add/',
        'icon': 'fa-plus',
    }]
    