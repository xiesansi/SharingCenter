#encoding=utf-8
import re
import base64
from django import forms
from django.contrib import auth
#from .forms improt UploadFileForm
from django.core.mail import send_mail
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from itsdangerous import URLSafeTimedSerializer as utsr
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response,redirect
from django.views.decorators.csrf import requires_csrf_token,csrf_protect
from django.http import HttpResponse,JsonResponse,Http404,HttpResponseRedirect

from registe_form import RegisterForm
from login_form  import LoginForm

# Create your views here.
class Token():
	def __init__(self,security_key):
		self.security_key = security_key
		self.salt = base64.encodestring(security_key)
	def generate_validate_token(self,username):
		serializer = utsr(self.security_key)
		return serializer.dumps(username,self.salt)
	def confirm_validate_token(self,token,expiration=3600):
		serializer = utsr(self.security_key)
		return serializer.loads(token,salt=self.salt,max_age=expiration)

token_confirm = Token('q1_^p*=c6s*9c&whfr@54#%aiuoo$_j44a87w99$2@^)uk3*!@')

class RegisterView(FormView):
    template_name = 'registe.html'
    form_class = RegisterForm
    success_url = reverse_lazy('')
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password,email=email)
        user.is_active='False'
        #login(self.request)
        return HttpResponseRedirect('/login')
        #return super(RegisterView, self).form_valid(form)

def login(request):
	if request.method == 'GET':
		form = LoginForm()
		return render_to_response('login.html', RequestContext(request, {'form': form,}))
	else:
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				request.session['member_id'] = user.pk
				request.session['user']=username
				auth.login(request, user)
				#return render_to_response('file_center.html', RequestContext(request,{"session":sess}))
				return HttpResponseRedirect("/files_center")
			else:
				notice="Your account isn't actived"
				return render_to_response('login.html',
				        RequestContext(request, {'form': form, 'notice': notice}))
		else:
			return render_to_response('login.html', RequestContext(request, {'form': form,}))

@login_required(login_url='/login')
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
	#return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def user_activate(request, activation_key):
	SHA1_RE = re.compile('^[a-f0-9]{40}$')
	if SHA1_RE.search(activation_key):
		try:
			user_profile = UserProfile.objects.get(activation_key=activation_key)
		except:
			return render_to_response('wrong_url.html', RequestContext(request, locals()))
		if not user_profile.activation_key_expired():
			user = user_profile.user
			user.is_active = True
			user.save()
			user_profile.activation_key = u"ALREADY_ACTIVATED"
			user_profile.save()
			return render_to_response('activate_complete.html', RequestContext(request, locals()))


def index(request):
	return render_to_response('index.html')

@login_required(login_url='/login')
def files_center(request):
	if request.user.is_authenticated():
		files_count='34675'
		user=request.session['user']
		return render_to_response('file_center.html',locals())
	else:
		return HttpResponseRedirect("/")
@login_required(login_url='/login')
def user_center(request):
	return render_to_response('user_center.html',locals())

@login_required(login_url='/login')
def test(request):
	if request.user.is_authenticated():
		user=request.session['user']
		token=token_confirm.generate_validate_token(user)
		message = "\n".join([
			u'{0},欢迎加入Sharing Center'.format(user),
			u'请访问该链接，完成用户验证:',
			'/'.join(['http://localhost', 'account_activate', token])
		])
		email='xiesansi@qq.com'
		#send_mail(u'Activate your account', message, None, [email])
		return render_to_response('document.html',locals())
	else:
		return HttpResponseRedirect("/")

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def handle_uploaded_file(f):
	with open('some/file/name.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def upload_file(request):
	if request.method == 'POST':
		un = request.POST.get('username')
		f = request.FILES.get('uploadfile')

		filename = '/'.join(['upload', f.name])
		#with open(filename, 'a+') keys:
		#for chunk in f.chunks():
		#	keys.write(chunk)
		#mongodb
		#uf = UploadFile(username=un, uploadfile=filename)
		#uf.save()
		#return HttpResponse(filename + ' OK')
		return render_to_response('upload_files.html',RequestContext(request, locals()))
	return render_to_response('upload_files.html', RequestContext(request, locals()))
