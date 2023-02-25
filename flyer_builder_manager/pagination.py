from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def custom_pagination(page,query,limit=5):
    paginator = Paginator(query, limit)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    return query
