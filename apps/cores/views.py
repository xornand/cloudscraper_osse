from django.views.generic import TemplateView
from django.conf import settings

class CustomSearchView(TemplateView):

    template_name = "search.html"
    
    def get_context_data(self, **kwargs):
        
        context = super(CustomSearchView, self).get_context_data(**kwargs)
        
        user = self.request.user
        if not user.is_anonymous():
            if self.request.user.first_name:
                # title does not exist in django_auth_user table
                #context["title"] = self.request.user.username
                context["firstname"] = self.request.user.first_name
                context["lastname"] = self.request.user.last_name
            else:
                context["username"] = self.request.user.username
            context["uid"] = user.id
        else:
            context["uid"] = 0
        
        #context["hostname"] = "127.0.0.1"
        context["hostname"] = settings.SEARCH_PAGE_HOSTNAME
        #context["port"] = 8000
        context["port"] = settings.SEARCH_PAGE_PORT
        context["mode"] = "cm"
        
        
        return context