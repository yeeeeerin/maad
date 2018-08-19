from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
import datetime
from tagging.fields import TagField
from bs4 import BeautifulSoup
import requests
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from Account.models import User

# Create your models here.

class Project(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=30)
	slug = models.SlugField(blank=True)
	publish_date = models.DateTimeField(default=timezone.now)

	TYPE_CHOICES =(
				('business scope', 'Business Scope'),
				('history', 'History'),
				('change in capital', 'Change in Capital'),
				('share with voting right', 'Share with Voting Right'),
				('dividend', 'Dividend'),
			)
	project_type = models.CharField(max_length = 15, choices=TYPE_CHOICES, default='A')
	project_field = models.CharField(max_length = 50)
	project_co = models.CharField(max_length = 20)
	
	start_date = models.DateTimeField(null=True)
	end_date = models.DateTimeField(null=True)

	TOOL_CHOICES = (
				('business scope', 'Business Scope'),
				('history', 'History'),
				('change in capital', 'Change in Capital'),
				('share with voting right', 'Share with Voting Right'),
				('dividend', 'Dividend'),
		)

	project_tool = models.CharField(max_length = 15, choices=TOOL_CHOICES, default='A')

	description = models.TextField(blank=True)
	project_result = models.TextField(blank=True)

	def publish(self, *args, **kwargs):
		self.publish_date = datetime.timezone.now()
		return super(Project, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		if not self.id:
		# Newly created object, so set slug
			self.slug = slugify(self.name)

		super(Project, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

def get_upload_path(instance, filename):

	return os.path.join('documents', instance.user.username,filename)

class Folder(models.Model):
	title = models.CharField(max_length=30)
	slug = models.SlugField(blank=True)
	proj = models.ForeignKey(Project)			
	created_date = models.DateTimeField(default = timezone.now)

	def save(self, *args, **kwargs):
		if not self.id:
		# Newly created object, so set slug
			self.slug = slugify(self.title)

		super(Folder, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.title

class Picture(models.Model):
	folder = models.ForeignKey(Folder, null =True)
	title = models.CharField(max_length=30, null = True)
	publish_date = models.DateTimeField(default=timezone.now)
	detail = models.TextField(max_length=30,null=True,blank=True)
	tag = TagField()
	"""
	This is a small demo using just two fields. ImageField depends on PIL or
	pillow (where Pillow is easily installable in a virtualenv. If you have
	problems installing pillow, use a more generic FileField instead.
	"""

	file = models.ImageField(upload_to="pictures")

	def __unicode__(self):
		return self.file.name

	def publish(self, *args, **kwargs):
		self.publish_date = datetime.timezone.now()
		return super(Picture, self).save(*args, **kwargs)


class URLData(models.Model):
	title = models.CharField(max_length=200)
	link = models.URLField()
	tag = TagField()
	image = models.ImageField(blank=True , default='media/images.jpeg')
	publish_date = models.DateTimeField(default=timezone.now)
	folder = models.ForeignKey(Folder, null =True)

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

			#다 없으면 디폴트 이미지로 들어감

		super(URLData, self).save(*args, **kwargs)	

	def publish(self, *args, **kwargs):
		self.publish_date = datetime.timezone.now()
		return super(URLData, self).save(*args, **kwargs)

class TextData(models.Model):
	title = models.CharField(max_length=20)
	text = models.TextField(null=True,blank=True)
	folder = models.ForeignKey(Folder, null =True)
	
