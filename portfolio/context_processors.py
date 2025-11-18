from .models import About

def about_data(request):
    try:
        about = About.objects.first()
    except About.DoesNotExist:
        about = None
    return {'about': about}
