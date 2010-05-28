from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

@permission_required('is_staff')  # sets ?next=/audio/ but does not return back here
def index(request):
    return HttpResponse("Hello, Euterpe!")