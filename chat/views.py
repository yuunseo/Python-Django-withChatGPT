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
        role_playing_room = form.dave(commit=False)
        role_playing_room.user = self.request.user
        return super().form_valid(form)


# .as_view()를 통해 클래스의 로직을 활용하는 새로운 뷰 함수를 생성
role_playing_room_new = RolePlayingRoomCreateView.as_view()
