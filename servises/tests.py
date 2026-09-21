from django.test import TestCase

from django.utils.safestring import mark_safe

def show_comment(request):
    comment = request.GET.get('comment')
    return HttpResponse(mark_safe(comment))  