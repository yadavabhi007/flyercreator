import imp
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
 
register = template.Library()


@register.filter
@stringfilter
def switch_i18n_prefix(path, language):
    """takes in a string path"""
    return switch_lang_code(path, language)
 
@register.filter
def switch_i18n(request, language):
    """takes in a request object and gets the path from it"""
    return switch_lang_code(request.get_full_path(), language)


from django.conf import settings
from flyer_builder.urls import urlpatterns

def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    # validate the inputs
    if path == "":
        raise Exception('Url path for language switch is empty')
    elif path[0] != '/':
        raise Exception('Url path for language does not start with “/”')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)
    # split the parts of the path
    parts = path.split('/')
    # add or substitute the new language prefix
    if parts[1] in lang_codes:
        if not urlpatterns[1].pattern.prefix_default_language:
            if language != settings.LANGUAGE_CODE:
                parts[1] = language
            else:
                parts.pop(1)
        else:
            parts[1] = language
    else:
        if not urlpatterns[1].pattern.prefix_default_language and language != settings.LANGUAGE_CODE:
            parts[0] = '/' + language
        # return the full new path
    return '/'.join(parts)


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()