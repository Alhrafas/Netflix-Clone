from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .form import ProfileForm

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:profile_list')
        return render(request, 'index.html')
@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        profiles = request.user.profile.all()
        context = {
            'profiles': profiles
        }
        return render(request, 'profileList.html', context)
    
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        # form for creating profile
        form = ProfileForm()
        context = {
            'form': form
        }
        return render(request, 'profileCreate.html', context)    
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        
        if form.is_valid():
            print(form.cleaned_data)
            
        # context = {
        #     'form': form
        # }
        return render(request, 'profileCreate.html', {
            'form': form
        })    
        
    