from django import template

from flyer_api.models import ProjectPageSpecialCell

register = template.Library()

@register.filter(name='page_banner')
def page_banner(page, banner):
    try:
        if banner=="header":
            obj = ProjectPageSpecialCell.objects.get(page_id=page.id, type='header')
        elif banner =="footer":
            obj = ProjectPageSpecialCell.objects.get(page_id=page.id, type='footer')
        if obj.image.image:
            return obj.image.image.url
    except:
        pass
    return ""