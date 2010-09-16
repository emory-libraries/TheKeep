from eulcore.django.fedora import server
from digitalmasters.accounts.views import decrypt

class Repository(server.Repository):
    """Extend the Django-ized Fedora Repository object to take a request object
    and connect to Fedora using a user is logged in and the required credentials
    are available.  If no request is specified or no user is logged in, falls
    back to the default logic, which uses Django settings for Fedora credentials.
    """
    def __init__(self, username=None, password=None, request=None):        
        if request is not None and request.user.is_authenticated() and \
            'fedora_password' in request.session:            
                username =request.user.username
                password = decrypt(request.session['fedora_password'])            
        super(Repository, self).__init__(username=username, password=password)

