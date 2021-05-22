from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Blog(models.Model):
	post_id=models.AutoField(primary_key=True)
	post_name = models.CharField(max_length=50)
	subheading = models.CharField(max_length=50,default=" ")
	category_tag = models.CharField(max_length=50,default=" ")
	slug = models.CharField(max_length=20,default=" ",unique=True)
	content = models.CharField(max_length=40000)
	pub_date = models.DateField()
	views = models.IntegerField(default=0)
	thumbnail = models.CharField(max_length=8000,default="")
	likes= models.IntegerField(default=0)

	def __str__(self):
		return self.post_name


class post_suggestion(models.Model):
	suggestion_id=models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	suggestion_title = models.CharField(max_length=50)
	category_tag = models.CharField(max_length=50,default=" ")
	def __str__(self):
		return self.suggestion_title+' by ' + self.name
		

class BlogComment(models.Model):
	sno =models.AutoField(primary_key=True)
	comment = models.TextField()
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Blog, on_delete=models.CASCADE)
	parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
	timestamp = models.DateTimeField(default=now)
	def __str__(self):
		return self.comment[0:11]

class Like(models.Model):
	sno =models.AutoField(primary_key=True)
	post = models.ForeignKey(Blog, on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	
