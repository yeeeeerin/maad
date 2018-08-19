from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from Account.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from .mixins import AjaxFormMixin


class LoginDoneView(TemplateView):
    template_name = "registration/login_done.html"


#--- User Creation
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


