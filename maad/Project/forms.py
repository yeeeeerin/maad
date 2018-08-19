from django import forms
from .models import TextData, Folder, Picture, URLData, Project
from ckeditor.widgets import CKEditorWidget
from django.forms.models import modelform_factory
from django.forms import ModelForm
from django.utils import timezone
import datetime

class PostSearchForm(forms.Form):
	search_word = forms.CharField(
		max_length=100,
		widget=forms.TextInput(
			attrs={
				'placeholder' : '  Type In Company Name',
				'required': 'True',
			}
		)
	)
class ProjectForms(ModelForm):
	class Meta:
		model = Project
		fields = ['name','user']

class TextForm(ModelForm):
	class Meta:
		model = TextData
		fields = ['text','folder']

class FolderForms(ModelForm):
	class Meta:
		model = Folder
		fields = ['title', 'proj']

class CreateURLForm(ModelForm):
	class Meta:
		model = URLData
		fields = ['title','link','image','tag','folder']

		def save(self, *args, **kwargs):
			if self.link:
				soup = BeautifulSoup(requests.get(self.link).content, "lxml")
				if soup.title.string and not self.title: #title tag 문자 가져옴
					self.title = soup.title.string
				meta = soup.find_all('meta')
		
				if soup.find(property = "og:image"):  #페이스북 open graph
					image = soup.find(property = "og:image").get('content')
					self.image = image
				elif soup.find(property = "twitter:image"): #트위터 open graph
					image = soup.find(property = "twitter:image").get('content')
					self.image = image
				elif soup.find_all('img')[0]: #둘다 없을 시 이미지 아무거나 때옴
					self.image = soup.find_all('img')[0].get('src')

			if self.link[12:18] == "google":
				image = self.link + image
				self.image = image

				#다 없으면 디폴트 이미지로 들어감
		#	self.publish_date = datetime.timezone.now()
			super(URLData, self).save(*args, **kwargs)

class CreatePictureForm(ModelForm):
	class Meta:
		model = Picture
		fields = ['file','folder']

class UpdatePictureForm(ModelForm):
	class Meta:
		model = Picture
		fields = ('title', 'detail', 'tag')

	def __init__(self, *args, **kwargs):
		super(UpdatePictureForm, self).__init__(*args,**kwargs)
	def save(self, id):
		print(id)
		instance = super(UpdatePictureForm, self).save(commit = False)
		instance.save()
		return instance
