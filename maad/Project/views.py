from django.views.generic import CreateView, TemplateView, DeleteView, FormView, UpdateView
from .models import Project, URLData, Picture, TextData, Folder
from Account.models import User
from tagging.models import Tag, TaggedItem
from django.db.models import Q
from django.utils import timezone
from .forms import PostSearchForm, UpdatePictureForm, CreatePictureForm, TextForm, CreateURLForm, ProjectForms
from .response import JSONResponse, response_mimetype, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FolderForms


# Create your views here.

class LoginDoneView(TemplateView):
    template_name = "registration/login_done.html"

class ProjectIndex(LoginRequiredMixin, TemplateView):
	model = Project
	template_name = "moodboard/Project_index.html"

	def get(self, request, *args, **kwargs):
		context={}
		project = Project.objects.all()
		folder = Folder.objects.all()
		that=[]
		for projects in project:
			print(projects.name)
			for fol in folder:
				if fol.proj.name == projects.name:	
					that.append(fol)
					break		
		context['Pro_all'] = Project.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date') & Project.objects.filter(user = self.request.user)
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
		context['folder'] = that
		context['user_name'] = User.objects.get(name= self.request.user.name)
			
		return render(self.request,'moodboard/Project_index.html', context)
			

class ProjectCreateView(LoginRequiredMixin,FormView):
	model = Project
	template_name = "moodboard/Project_create.html"
	success_url = reverse_lazy('Project:index')
	form_class = PostSearchForm
	project_form_class = ProjectForms

	def get_context_data(self, **kwargs):
		context = super(ProjectCreateView, self).get_context_data(**kwargs)
		context['Pro_all'] = Project.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
		context['user_name'] = User.objects.get(name= self.request.user.name)
		
		return context
		
	def post(self, request, *args, **kwargs):
		context = {}
		if 'find' in request.POST:
			schWord = '%s' % self.request.POST['search_word']
		
			if schWord[0]=="#":
		 		tag = URLData.objects.filter(Q(tag__icontains=schWord)).distinct()[:10]
			else:
				tag = Project.objects.filter(Q(name__icontains=schWord)).distinct()[:10]
			context['search_term'] = '%s' % self.request.POST['search_word']
			context['tag'] =tag
			return render(self.request,'moodboard/search.html', context)
		elif 'cre_pro' in request.POST:
			context={}
			form= ProjectForms(request.POST)
			if form.is_valid():
				form.save()
		
			context['Pro_all'] = Project.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date') & Project.objects.filter(user = self.request.user)
			return render(request, 'moodboard/Project_index.html', context)

		context['Pro_all'] = Project.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date') & Project.objects.filter(user = self.request.user)
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
		context['user_name'] = User.objects.get(name= self.request.user.name)

		return render(request, 'moodboard/Project_index.html', context)

class FolderCreate(CreateView):
	model = Folder
	fields = ['title', 'proj']
	template_name = "moodboard/Folder_create.html"
	
	def get_context_data(self,**kwargs):
		context = super(FolderCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['name'] = Folder.objects.filter(proj__name= self.kwargs['slug'])
			context['project'] = Project.objects.get(name= self.kwargs['slug'])
		else:
			context['name'] = Folder.objects.filter(proj__name= self.kwargs['slug'])
			context['project'] = Project.objects.get(name= self.kwargs['slug'])
		
		return context
	
	def get_success_url(self):
		return reverse_lazy('Project:create_pic', kwargs = {'pk': self.object.proj.user.id, 'slug':self.object.proj.name, 'ti':self.object.title})
	

class PictureCreateView(FormView):
	model = Picture
	template_name = "moodboard/picture_form.html"
	form_class = CreatePictureForm
	update_form_class = UpdatePictureForm
	search_form_class = PostSearchForm

	def post(self,request, *args, **kwargs):
		context = {}
		if 'img_save' in request.POST:	
			form = CreatePictureForm(request.POST, request.FILES)
			subform = UpdatePictureForm()
			if form.is_valid():
				self.object = form.save()
				data = {'status': 'success'}
				response = JSONResponse(data, mimetype=response_mimetype(self.request))
				return super(PictureCreate, self).form_valid(form)
		elif 'save' in request.POST:
			context = {}
			pic = get_object_or_404(Picture, pk = request.POST.get('save'))
			form = UpdatePictureForm(request.POST, instance = pic)
			subform = CreatePictureForm()
			if form.is_valid():
				pic=form.save(id = pic.pk)
		elif 'find' in request.POST:
			schWord = '%s' % self.request.POST['search_word']
		
			if schWord[0]=="#":
		 		tag = URLData.objects.filter(Q(tag__icontains=schWord)).distinct()[:10]
			else:
				tag = Project.objects.filter(Q(name__icontains=schWord)).distinct()[:10]
			context['search_term'] = '%s' % self.request.POST['search_word']
			context['tag'] =tag
			return render(self.request,'moodboard/search.html', context)

		context['Pro_view'] = Project.objects.get(name=self.kwargs['slug'])
		context['Folder_view'] = Folder.objects.get(title = self.kwargs['ti'])
		context['pic'] = Picture.objects.filter(folder__title = self.kwargs['ti']) & Picture.objects.filter(folder__proj__name = self.kwargs['slug']) & Picture.objects.filter(folder__proj__user__id = self.kwargs['pk'])
		context['Folder_all'] = Folder.objects.filter(proj__name=self.kwargs['slug']) & Folder.objects.filter(proj__user__id = self.kwargs['pk'])
		context['create'] = CreatePictureForm
		context['update'] = UpdatePictureForm
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]

		return render(request,'moodboard/picture_form.html',context)
	
	def get_context_data(self, **kwargs):
		context = super(PictureCreateView, self).get_context_data(**kwargs)
		context['Pro_view'] = Project.objects.get(name=self.kwargs['slug'])
		context['Folder_view'] = Folder.objects.get(title=self.kwargs['ti'])
		context['pic'] = Picture.objects.filter(folder__title = self.kwargs['ti']) & Picture.objects.filter(folder__proj__name = self.kwargs['slug']) & Picture.objects.filter(folder__proj__user__id = self.kwargs['pk'])
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
		context['Folder_all'] = Folder.objects.filter(proj__name=self.kwargs['slug']) & Folder.objects.filter(proj__user__id = self.kwargs['pk'])
	
		context['create'] = CreatePictureForm
		context['update'] = UpdatePictureForm
		
		return context

	def get_success_url(self):
		context= {}
		context['Project'] = Project.objects.get(name=self.kwargs['ti'])
		context['folder'] = Folder.objects.get(title = self.kwargs['slug'])
		context['pic'] = Picture.objects.filter(folder__title = self.kwargs['slug'])

		return reverse_lazy('Project:create_pic',context)

class Delete(DeleteView):
	model = Picture

	def get_success_url(self):
		return reverse_lazy('Project:create_pic',kwargs ={'slug':self.object.folder.proj.name,'ti':self.object.folder.title})

class URLDelete(DeleteView):
	model = URLData

	def get_success_url(self):
		return reverse_lazy('Project:create_url',kwargs ={'slug':self.object.folder.proj.name,'ti':self.object.folder.title})

def index(request, slug, ti):
	model = TextData
	form = TextForm()
	context = {'form': form, 'Pro_view': Project.objects.get(name=slug), 'Folder_view': Folder.objects.get(title=ti), 'Folder_id': Folder.objects.get(title=ti) and Folder.objects.get(proj__name=slug), 'tag' : URLData.objects.filter(folder__proj__user = request.user)}

	if request.method == 'POST':
		if 'find' in request.POST:
			schWord = '%s' % self.request.POST['search_word']
		
			if schWord[0]=="#":
		 		tag = URLData.objects.filter(Q(tag__icontains=schWord)).distinct()[:10]
			else:
				tag = Project.objects.filter(Q(name__icontains=schWord)).distinct()[:10]
			context['search_term'] = '%s' % self.request.POST['search_word']
			context['tag'] =tag
			return render(self.request,'moodboard/search.html', context)
		elif 'text_save' in request.POST:
			form= TextForm(request.POST)
			if form.is_valid():
				form.save()
			else:
				print(1)

	return render(request, 'moodboard/text_create.html', context)


class URLCreateView(FormView):
	model= URLData
	template_name = "moodboard/url_create.html"
	form_class = PostSearchForm
	url_form_class = CreateURLForm

	def get_context_data(self, **kwargs):
		context = super(URLCreateView, self).get_context_data(**kwargs)
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
		context['Pro'] = Project.objects.all()	
		context['Pro_view'] = Project.objects.get(name=self.kwargs['slug'])
		context['Folder_view'] = Folder.objects.get(title=self.kwargs['ti']) 
		context['Folder_all'] = Folder.objects.filter(proj__name=self.kwargs['slug']) & Folder.objects.filter(proj__user__id = self.kwargs['pk'])
		context['url'] = URLData.objects.filter(folder__title = self.kwargs['ti']) & URLData.objects.filter(folder__proj__name = self.kwargs['slug']) & URLData.objects.filter(folder__proj__user__id = self.kwargs['pk'])
		
		return context
		
	def post(self, request, *args, **kwargs):
		context = {}
		if 'find' in request.POST:
			schWord = '%s' % self.request.POST['search_word']
		
			if schWord[0]=="#":
		 		tag = URLData.objects.filter(Q(tag__icontains=schWord)).distinct()[:10]
			else:
				tag = Project.objects.filter(Q(name__icontains=schWord)).distinct()[:10]
			context['search_term'] = '%s' % self.request.POST['search_word']
			context['tag'] =tag
			return render(self.request,'moodboard/search.html', context)
		elif 'cre_url' in request.POST:
			form = CreateURLForm(request.POST, request.FILES)
			if form.is_valid():
				self.object = form.save()
				context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
				context['Pro'] = Project.objects.all()	
				context['Pro_view'] = Project.objects.get(name=self.kwargs['slug'])
				context['Folder_view'] = Folder.objects.get(title=self.kwargs['ti'])
				context['Folder_all'] = Folder.objects.filter(proj__name=self.kwargs['slug']) & Folder.objects.filter(proj__user__id = self.kwargs['pk'])
				context['url'] = URLData.objects.filter(folder__title = self.kwargs['ti']) & URLData.objects.filter(folder__proj__name = self.kwargs['slug']) & URLData.objects.filter(folder__proj__user__id = self.kwargs['pk'])
				return render(request,'moodboard/url_create.html',context)

			context['Pro_all'] = Project.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
			
		    # 다시 조회    
		context['tag'] = URLData.objects.filter(publish_date__lte=timezone.now()) & URLData.objects.filter(folder__proj__user = self.request.user).order_by('publish_date')[:4]
		context['Pro'] = Project.objects.all()	
		context['Pro_view'] = Project.objects.get(name=self.kwargs['slug'])
		context['Folder_view'] = Folder.objects.get(title=self.kwargs['ti'])
		context['Folder_all'] = Folder.objects.filter(proj__name=self.kwargs['slug']) & Folder.objects.filter(proj__user__id = self.kwargs['pk'])
		context['url'] = URLData.objects.filter(folder__title = self.kwargs['ti']) & URLData.objects.filter(folder__proj__name = self.kwargs['slug']) & URLData.objects.filter(folder__proj__user__id = self.kwargs['pk'])

		return render(request,'moodboard/url_create.html',context)

	def get_success_url(self):
		context= {}
		context['Pro_all'] = URLData.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')[:4]
		context['Pro'] = Project.objects.all()	
		context['Pro_view'] = Project.objects.get(name=self.kwargs['slug'])
		context['Folder_view'] = Folder.objects.get(title=self.kwargs['ti'])
		context['Folder_all'] = Folder.objects.filter(proj__name=self.kwargs['slug']) & Folder.objects.filter(proj__user__id = self.kwargs['pk'])
		context['url'] = URLData.objects.filter(folder__title = self.kwargs['ti']) & URLData.objects.filter(folder__proj__name = self.kwargs['slug']) & URLData.objects.filter(folder__proj__user__id = self.kwargs['pk'])

		return reverse_lazy('Project:url_create',context)

class SearchFormView(FormView):
	form_class = PostSearchForm
	template_name='moodboard/search.html'

	def post(self, request, *args, **kwargs):
		context = {}	
		schWord = '%s' % self.request.POST['search_word']
		
		if schWord[0]=="#":
	 		tag = URLData.objects.filter(Q(tag__icontains=schWord)).distinct()[:10]
		else:
			tag = Project.objects.filter(Q(name__icontains=schWord)).distinct()[:10]
		context['search_term'] = '%s' % self.request.POST['search_word']
		context['tag'] =tag
		return render(self.request,'moodboard/search.html', context)

class AutoCompleteView(FormView):
	def get(self,request,*args,**kwargs):
		data=request.GET
		name=data.get("term")
		results = []

		if name:
			if name[0]=="#":
				proj = Tag.objects.filter(name__icontains = name)
				for pro in proj:
					pro_json = {}
					pro_json['id'] = pro.id
					pro_json['label'] = pro.name
					pro_json['value'] = pro.name
					results.append(pro_json)

			else:
				proj = Project.objects.filter(name__icontains = name)
				for pro in proj:
					pro_json = {}
					pro_json['id'] = pro.id
					pro_json['label'] = pro.name
					pro_json['value'] = pro.name
					results.append(pro_json)
				
		else:
			if name[0]=="#":			
				proj = Tag.objects.all()
			else:
				proj = Project.objects.all()
		

		data=json.dumps(results)
		mimetype = 'application/json'

		return HttpResponse(data,mimetype)





			
                   

