import random
from django.contrib.auth import get_user_model
from .models import Profile, User,Follow
User = get_user_model()

def get_recommended_users(request):
    all_users = list(User.objects.all())
    random.shuffle(all_users)
    recommended_users = all_users[:10]
    while len(recommended_users) < 10:
        recommended_users.append("Not Found")

    return {
        'recommended_users': recommended_users,
    }
def global_context(request):
    context = {}
    
    # ログインしているユーザーのプロフィールを取得
    if request.user.is_authenticated:
        context['current_user_profile'] = Profile.objects.filter(profile_user=request.user).first()

    # Profile が存在し、User も存在するもののみ取得
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

    # ランダムに 10 ユーザーを取得
    context['recommended_users'] = random.sample(recommended_users_with_profile, min(len(recommended_users_with_profile), 10))

    return context