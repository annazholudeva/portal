from django import template

register = template.Library()


@register.filter()
def censor(words):
    censored = ''
    replace = '*'
    for word in words:
        if word.isupper():
            censored = word[0] + replace
            replace += '*'
        else:
            censored = words
    return censored
