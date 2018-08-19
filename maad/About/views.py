from django.shortcuts import render
from django.views.generic.base import TemplateView
from Project.models import Project, URLData, Picture
from Account.models import User
from django.utils import timezone


# Create your views here.
class Landing(TemplateView):
	template_name = 'Landing.html'

	def get_context_data(self, **kwargs):
		context = super(Landing, self).get_context_data(**kwargs)
		context['Pro_all'] = Project.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
		context['user_name'] = User.objects.get(name= self.request.user.name)
		
		return context
