from django.shortcuts import render
from .models import TwitchPost
# Create your views here.
from django.views.generic import ListView
class IndexView(ListView):
    template_name='Twitch index.html'
    context_object_name= 'orderby_records'
    paginate_by=4
    model = TwitchPost
    context_object_name = 'video_list'