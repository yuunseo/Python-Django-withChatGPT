from django.contrib import admin
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm


# admin페이지에 추가될 admin 생성
@admin.register(RolePlayingRoom)
class RolePlayingRoomAdmin(admin.ModelAdmin):
    # 사용할 폼 가져오기
    form = RolePlayingRoomForm

    # .user 속성 할당을 위해 메소드 재정의
    def save_model(self, request, obj, form, change):
        # change여부를 통해 신규 생성 여부 check 및 유효성 검사
        if change is False and form.is_valid():
            obj.user = request.user

        super().save_model(request, obj, form, change)
