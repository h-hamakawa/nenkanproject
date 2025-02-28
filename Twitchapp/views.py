

from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,TwitchPost,Comment,Follow
# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,TemplateView,UpdateView,DetailView
from .forms import ProfileForm,TwitchPostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Q 
from django.contrib.auth import get_user_model
from django.views import View
import random




User = get_user_model()

class ContentListView(ListView):
    template_name = 'contents.html'
    context_object_name = 'videos'

    def get_queryset(self):
        game_tag = self.kwargs.get('game_tag')
        if game_tag:
            return TwitchPost.objects.filter(category=game_tag).order_by('-posted_at')
        return TwitchPost.objects.all().order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_tags'] = TwitchPost.GAME_TAG
        context['selected_tag'] = self.kwargs.get('game_tag')
        return context

class IndexView(ListView):
    template_name = 'Twitch index.html'
    context_object_name = 'orderby_records'
    paginate_by = 4
    model = TwitchPost

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not Profile.objects.filter(profile_user=request.user).exists():
            return redirect('Twitchapp:profile_create')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_videos = list(TwitchPost.objects.all())
        random_videos = random.sample(all_videos, min(len(all_videos), 4))
        context['random_videos'] = random_videos
        
        # Profile が存在するユーザーを取得
        users_with_profile = Profile.objects.filter(profile_user__isnull=False)
        recommended_users_with_profile = []

        for profile in users_with_profile:
            user = profile.profile_user
            if user:
                # フォロワー数を取得
                followers_count = Follow.objects.filter(Following=user).count()
                recommended_users_with_profile.append({
                    'user': user,
                    'profile': profile,
                    'followers_count': followers_count
                })

        context['recommended_users'] = recommended_users_with_profile
        
        # 現在のユーザーのプロフィールを取得
        if self.request.user.is_authenticated:
            context['current_user_profile'] = Profile.objects.filter(profile_user=self.request.user).first()
        
        return context



    
# class IndexView(ListView):
#     template_name='Twitch index.html'
#     context_object_name= 'orderby_records'
#     paginate_by=4
#     model = TwitchPost

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and not Profile.objects.filter(profile_user=request.user).exists():
#             return redirect('Twitchapp:profile_create')
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         all_videos = list(TwitchPost.objects.all())
#         random_videos = random.sample(all_videos, min(len(all_videos), 4))
        
#         context['random_videos'] = random_videos

#         all_users = list(User.objects.all())
#         recommended_users = random.sample(all_users, min(len(all_users), 10))


#         recommended_users_with_profile = []
#         for user in recommended_users:
#             profile = Profile.objects.filter(profile_user=user).first()
#             recommended_users_with_profile.append({
#                 'user': user,
#                 'profile': profile
#             })

#         context['recommended_users'] = recommended_users_with_profile
#         if self.request.user.is_authenticated:
#             context['current_user_profile'] = Profile.objects.filter(profile_user=self.request.user).first()
        
#         return context



    
class FollowToggleView(View):
    def post(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, pk=self.kwargs['pk'])
        current_user = request.user
        is_following = Follow.objects.filter(Follower=current_user, Following=target_user).exists()

        if is_following:
            Follow.objects.filter(Follower=current_user, Following=target_user).delete()
        else:
            Follow.objects.create(Follower=current_user, Following=target_user)
        return redirect('Twitchapp:profile_detail', pk=target_user.pk)

class UserSearchView(ListView):
    model = User
    template_name = 'search.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) & Q(profile__isnull=False)
            ).order_by('username')
            valid_users = []
            for user in users:
                if Profile.objects.filter(profile_user=user).exists():
                    valid_users.append(user)
            
            return valid_users
        
        return User.objects.none()
# class UserSearchView(ListView):
#     model = User
#     template_name = 'search.html'
#     context_object_name = 'users'

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         if query:
#             users = User.objects.filter(
#                 Q(username__icontains=query) & Q(profile__isnull=False)
#             ).order_by('username')
#             return users
        
#         return User.objects.none()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['query'] = self.request.GET.get('q')
#         return context


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        current_user = self.request.user

        if current_user.is_authenticated and user_id == current_user.pk:
            return redirect('Twitchapp:profile')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, profile_user__pk=user_id)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_user = self.get_object().profile_user
        current_user = self.request.user

        is_following = Follow.objects.filter(Follower=current_user, Following=target_user).exists()
        context['is_following'] = is_following
        followers = Follow.objects.filter(Following=target_user)
        followers_count = followers.count()
        context['followers'] = followers
        context['followers_count'] = followers_count

        videos = TwitchPost.objects.filter(user=target_user).order_by('-posted_at')
        context['videos'] = videos

        return context



class ProfileCreateView(LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    template_name = "profile_create.html"
    success_url = reverse_lazy('Twitchapp:Twitch index') 

    def form_valid(self, form):
        form.instance.profile_user = self.request.user
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile_update.html"
    success_url = reverse_lazy('Twitchapp:profile_done')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, profile_user=self.request.user)

    def form_valid(self, form):
        form.instance.profile_user = self.request.user
        return super().form_valid(form)




class ProfileSuccessView(TemplateView):
    template_name = "profile_success.html"

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(profile_user=self.request.user).first()
        context['profile'] = profile
        context['videos'] = TwitchPost.objects.filter(user=self.request.user).order_by('-posted_at')
        
        # フォロワーの数を取得
        followers_count = Follow.objects.filter(Following=self.request.user).count()
        context['followers_count'] = followers_count
        
        return context

# class ProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'profile.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['profile'] = Profile.objects.filter(profile_user=self.request.user).first()
#         context['videos'] = TwitchPost.objects.filter(user=self.request.user).order_by('-posted_at')

#         return context



@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = TwitchPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # 一旦保存を遅延させる
            post.user = request.user  # 現在のログインユーザーをセット
            post.save()
            return redirect('Twitchapp:index')
    else:
        form = TwitchPostForm()

    context = {
        'form': form
    }
    return render(request, 'post.html', context)

class VideoDetailView(LoginRequiredMixin, DetailView):
    model = TwitchPost
    template_name = 'video_page.html'
    context_object_name = 'video'


class VideoDetailView(DetailView):
    model = TwitchPost
    template_name = 'video_page.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(profile_user=self.object.user).first()
        context['comments'] = Comment.objects.filter(video=self.object).order_by('posted_at')  # コメント一覧
        return context

@login_required
def post_comment(request, pk):
    if request.method == 'POST':
        video = get_object_or_404(TwitchPost, pk=pk)
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(
                video=video,
                user=request.user,
                text=comment_text
            )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

