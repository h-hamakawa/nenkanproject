from django.db import models

# Create your models here.
class TwitchPost(models.Model):
    GAME_TAG=(('valorant','ヴァロラント'),
              ('chat','雑談'),
              ('summonerswar','サマナーズウォー'),
              ('fortnite','フォートナイト'),
              ("apex","エイペックス"),
              ("minecarft","マインクラフト"))
    channel_name = models.CharField(
        verbose_name='チャンネル名',
        max_length=16
    )

    channel_number= models.IntegerField(
        verbose_name='チャンネル番号'
    )

    content=models.TextField(
        verbose_name='説明文'
    )

    category = models.CharField(
        verbose_name='ゲームタグ',
        max_length=50,
        choices=GAME_TAG
        )
    movie = models.FileField(
        verbose_name='動画ファイル',
        max_length='100'
    )
    def __str__(self):
        return self.title

