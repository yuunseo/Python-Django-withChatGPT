from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.
class RolePlayingRoom(models.Model):
    # 선택지 생성 class
    class Language(models.TextChoices):
        ENGLISH = "en-US", "English"
        JAPANESE = "ja-JP", "Japanese"
        CHINESE = "zh-CN", "Chinese"
        SPANISH = "es-ES", "Spanish"
        FRENCH = "fr-FR", "French"
        GERMAN = "de-DE", "German"
        RUSSIAN = "ru-RU", "Russian"

    # 선택지 생성 class
    class Level(models.IntegerChoices):
        BEGINNER = 1, "초급"
        ADVANCED = 2, "고급"

    # 이 모델(RolePlayingRoom)로 부터 파생되는 QuerySet의 default 정렬방향 지정
    class Meta:
        ordering = ["-pk"]

    # user 필드를 외래키로 지정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # lansguage 필드를 charfiled로 지정 -> 선택지
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.ENGLISH,
        verbose_name="대화 언어",
    )
    # level 필드(1,2,3)-> 선택지
    level = models.SmallIntegerField(
        choices=Level.choices, default=Level.BEGINNER, verbose_name="레벨"
    )
    # situation 필드 -> 한글 저장
    # situation_en 필드 -> 영문 저장
    situation = models.CharField(max_length=100, verbose_name="상황")
    situation_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="상황 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, situation 필드를 번역하여 자동 반영됩니다.",
    )
    my_role = models.CharField(max_length=100, verbose_name="내 역할")
    my_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="내 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, my_role 필드를 번역하여 자동 반영됩니다.",
    )
    gpt_role = models.CharField(max_length=100, verbose_name="GPT 역할")
    gpt_role_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="GPT 역할 (영문)",
        help_text="GPT 프롬프트에 직접적으로 활용됩니다. 비워두시면, gpt_role 필드를 번역하여 자동 반영됩니다.",
    )

    def get_absolute_url(self) -> str:
        return reverse("role_playing_room_datail", args=[self.pk])
