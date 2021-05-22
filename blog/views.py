from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Blog,post_suggestion,BlogComment,Like
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
def index(request):
	mypost = Blog.objects.all()[::-1]
	popularblogs = Blog.objects.order_by('-views','post_name')[0:4]
	tags=[]
	for tag in mypost:
		tags.append(tag.category_tag)
	realtags=[]
	for j in tags:
		if j not in realtags:
			realtags.append(j)
	return render(request,'blog/index.html',{'mypost':mypost,'popular':popularblogs,'tags':realtags})


def suggestpost(request):
	if request.method=="POST":
		name=request.POST['name']
		email=request.POST['email']
		post_title=request.POST['post_title']
		post_category=request.POST['post_category']
		suggestion=post_suggestion(name=name, email=email, suggestion_title=post_title, category_tag=post_category)
		suggestion.save()
		messages.success(request, "Thanks for the suggestion :)")
		return redirect('/')
	return render(request,'blog/suggest_post.html')


def blogpost(request,slug):
	#try:
		post = Blog.objects.filter(slug=slug).first()
		post.views=post.views+1
		post.save() 
		comments = BlogComment.objects.filter(post=post,parent=None)
		replies = BlogComment.objects.filter(post=post).exclude(parent=None)
		replyDict={}
		for reply in replies:
			if reply.parent.sno not in replyDict.keys():
				replyDict[reply.parent.sno]=[reply]
			else:
				replyDict[reply.parent.sno].append(reply)
		if  request.user.is_anonymous:
			return render(request,'blog/blogpost.html',{'post':post,'comments':comments,'user':request.user,'replies':replyDict})		
		else:
			likes = Like.objects.filter(post=post,user=request.user)
			return render(request,'blog/blogpost.html',{'post':post,'comments':comments,'user':request.user,'replies':replyDict,'likes':likes})
				
		
	#except Exception as e:
	#	print("there is a problm!",e)
	#	return redirect('/')



def search(request):
	query = request.GET['search']
	if len(query)>70:
		 results=Blog.objects.none()
	else:
		resultsTitle = Blog.objects.filter(post_name__icontains=query)
		resultsSub= Blog.objects.filter(subheading__icontains=query)
		resultsCat= Blog.objects.filter(category_tag__icontains=query)
		resultsContent = Blog.objects.filter(content__icontains=query)
		results=  resultsTitle.union(resultsContent, resultsSub,resultsCat)
	if results.count()==0:
		messages.warning(request, "No search results found. Please refine your query.")

	return render(request,'blog/search.html',{'results':results,'query':query})


def handleSignup(request):
	try:
		if request.method=='POST':
			name = request.POST.get('name')
			email= request.POST.get('email')
			pass1 = request.POST.get('password')
			pass2 = request.POST.get('conpass')
			


			if len(name)>15:
				messages.error(request, "Username must be below 15 characters")
			if pass1!= pass2:
				messages.error(request, "Password and Confirm password are not the same.Please double check them again.")
			if len(name)<3 or len(email)<4 or len(pass1)<4 or len(pass2)<4:
				messages.error(request, "Information must be more than 4 characters")
			

			else:
				auser = User.objects.create_user(name,email,pass1)
				auser.save()
				messages.success(request, "Account Created :)")
				login(request,auser)
				return redirect('/')
			return redirect('/')
		else:
			return HttpResponse('404-- Not Allowed')
	except Exception as e:
		messages.error(request, "There was a problem please try again.The username or email is already registered")
		return redirect('/')

def handleLogin(request):
	try:
		if request.method=='POST':
			lname = request.POST.get('lname')
			lpass = request.POST.get('lpassword')
			user = authenticate(username=lname,password=lpass)

			if user is not None:
				login(request,user)
				messages.success(request, "Successfully Logged in :)")
				redirect("/")
			else:
				messages.error(request, "Invalid Credentials.Please try again.")
				return redirect("/")
			return redirect('/')
		else:
			return HttpResponse('404-- Not Allowed')
	except Exception as e:
		messages.error(request, "There was a problem please try again.")
		return redirect('/')

def handleLogout(request):
	try:
		logout(request)
		messages.success(request, "Successfully Logged Out :)")
		return redirect("/")
	except Exception as e:
		messages.error(request, "There was a problem please try again.")
		return redirect('/')


def postComment(request):
	if request.method=="POST":
		comment = request.POST.get('comment')
		user = request.user
		postid = request.POST.get("Parentpostid")
		parentid= request.POST.get("parentsno")
		post = Blog.objects.get(post_id=postid)	
		
		if parentid=="":
			comment = BlogComment(comment=comment,user=user,post=post)
			comment.save()
			messages.success(request, "Comment has been successfully posted")
		
		else:
			parentsno = BlogComment.objects.get(sno=parentid)
			comment = BlogComment(comment=comment,user=user,post=post,parent=parentsno)
			comment.save()
			messages.success(request, "Reply has been successfully posted")
	return redirect(f"/blogpost/{post.slug}")


def postLike(request):
	if request.method=="POST":
		post_sno = request.POST.get("postsno")
		user= request.user
		post = Blog.objects.filter(post_id=post_sno).first()
		post.likes+=1
		post.save()
		like = Like(post=post,user=user)
		like.save()
	return redirect(f"/blogpost/{post.slug}")

def removeLike(request):
	if request.method=="POST":
		post_sno = request.POST.get("postsno")
		post = Blog.objects.filter(post_id=post_sno).first()
		user = request.user
		like = Like.objects.filter(post=post,user=user)

		post.likes-=1
		post.save()
		like.delete()
	return redirect(f"/blogpost/{post.slug}")
