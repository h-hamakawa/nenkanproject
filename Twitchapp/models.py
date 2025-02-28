from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()

class Profile(models.Model):
    status_message  = models.CharField(
        verbose_name='ステータスメッセージ',
        max_length=100,
        null=False,
    )
    icon = models.ImageField(
        verbose_name='アイコン',
        upload_to='Twitchapp',
        null=False,
    )

    profile_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    posted_at=models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True)
    
class Follow(models.Model):
    Follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Following')

    Following = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Follower')

    posted_at=models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True)


class Subscribe(models.Model):
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='subscribing')

    subscribing = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='subscriber')

    posted_at=models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True)

class TwitchPost(models.Model):
    GAME_TAG=(('sum','サマナーズウォー'),
              ('valorant','ヴァロラント'),
              ('chat','雑談'),
              ("csgo","csgo"),
              ("minecraft","マインクラフト"),
              ("gtv","グランドセフトオートV"),
              ('fortnite','フォートナイト'),
              ("among us","アモングアス"),
              ("st5","ストリートファイター６"),
              ("apex","エイペックス"),)
    
    GAME_TAG_IMAGE = {
        'sum': 'img/sum.jpg',
        'valorant': 'img/valorant.jpg',
        'chat': 'img/chat.jpg',
        'csgo': 'img/csgo.png',
        'minecarft': 'img/minecraft.jpg',
        'gtv': 'img/gtv.jpg',
        'fortnite': 'img/fortnite.jpg',
        'among us': 'img/among us.jpg',
        'st5': 'img/st5.jpg',
        'apex': 'img/apex.jpg',
    }
    movie_title = models.CharField(
        verbose_name='タイトル',
        max_length=16
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    content=models.TextField(
        verbose_name='説明文'
    )
    posted_at=models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    category = models.CharField(
        verbose_name='ゲームタグ',
        max_length=50,
        choices=GAME_TAG
        )
    movie = models.FileField(
        verbose_name='動画ファイル',
        upload_to='videos/',
    )

    posted_at=models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True)



    def __str__(self):
        return self.movie_title


class Comment(models.Model):
    video = models.ForeignKey(TwitchPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='コメント内容')
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"