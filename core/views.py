from core.models import Profile, Movies
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
    
@method_decorator(login_required, name='dispatch')
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
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profile.add(profile)
                return redirect('core:profile_list')
                       
        return render(request, 'profileCreate.html', {
            'form': form
        })    
@method_decorator(login_required, name='dispatch')        
class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid = profile_id)
            movies = Movies.objects.filter(age_limit = profile.age_limit)
            
            if profile not in request.user.profile.all():
                return redirect('core:profile_list')    
            return render(request, 'movieList.html', {
                'movies': movies
            })
        except Profile.DoesNotExist:
            return redirect('core:profile_list')    
        
@method_decorator(login_required, name='dispatch')          
class ShowMovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movies.objects.get(uuid=movie_id)
            
            return render(request, 'movieDetail.html', {
                'movie': movie
            })        
        
        except Movies.DoesNotExist:
            return redirect('core:profile_list')    
 

@method_decorator(login_required, name='dispatch')        
class ShowMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movies.objects.get(uuid=movie_id)
            movie = movie.videos.values()
            return render(request, 'showMovie.html', {
                'movie': list(movie)
            })
        
        except Movies.DoesNotExist:
            return redirect('core:profile_list')    