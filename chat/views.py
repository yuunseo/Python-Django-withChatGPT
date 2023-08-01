from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .models import RolePlayingRoom
from .forms import RolePlayingRoomForm


# 로그인 기능 구현하지 않으므로 admin의 staff_member_required 장식자 활용
@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomCreateView(CreateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    # user 데이터 전달
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        role_playing_room = form.save(
            commit=False
        )  # form을 통한 instance생성 시, instance.save()이 호출되지 않도록 commit=False
        role_playing_room.user = self.request.user  # save() 전에 user field 할당
        return super().form_valid(form)  # 이제 save() 가능 -> 부모 호출 -> save()를 통해 DB에 저장


# .as_view()를 통해 클래스의 로직을 활용하는 새로운 뷰 함수를 생성
# .as_view()를 통해 뷰 호출
role_playing_room_new = RolePlayingRoomCreateView.as_view()
