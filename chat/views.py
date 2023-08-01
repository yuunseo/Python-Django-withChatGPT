from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse_lazy
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


# 마찬가지로 로그인 된 유저가 필요하므로 유효성 확인을 위해 데코레이터.
@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomUpdateView(UpdateView):
    model = RolePlayingRoom
    form_class = RolePlayingRoomForm

    # user 본인의 queryset만 가져오기 위해 구현.
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


role_playing_room_edit = RolePlayingRoomUpdateView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomListView(ListView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


role_playing_room_list = RolePlayingRoomListView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomDetailView(DetailView):
    model = RolePlayingRoom

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


role_playing_room_detail = RolePlayingRoomDetailView.as_view()


@method_decorator(staff_member_required, name="dispatch")
class RolePlayingRoomDeleteView(DeleteView):
    model = RolePlayingRoom
    # 삭제 후, 해당 url로 이동
    success_url = reverse_lazy("role_playing_room_list")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    # 삭제 후, 삭제됨을 알리는 message 표시
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "채팅방을 삭제했습니다.")
        return response


role_playing_room_delete = RolePlayingRoomDeleteView.as_view()
