from django import forms
from .models import RolePlayingRoom
from .translators import google_translate


# model을 기반으로 움직이는 form 생성
class RolePlayingRoomForm(forms.ModelForm):
    class Meta:
        model = RolePlayingRoom
        exclude = "user"

    # clean method란, 폼 필드 다수에 대한 유효성 검사 수행 및
    # 값의 변환 또한 가능
    def clean(self):
        situation = self.cleaned_data.get("situation")
        situation_en = self.cleaned_data.get("situation_en")
        if situation and not situation_en:
            self.cleaned_data["situation_en"] = self._translate(situation)

        my_role = self.cleaned_data.get("my_role")
        my_role_en = self.cleaned_data.get("my_role_en")
        if my_role and not my_role_en:
            self.cleaned_data["my_role_en"] = self._translate(my_role)

        gpt_role = self.cleaned_data.get("gpt_role")
        gpt_role_en = self.cleaned_data.get("gpt_role_en")
        if gpt_role and not gpt_role_en:
            self.cleaned_data["gpt_role_en"] = self._translate(gpt_role)

        return self.cleaned_data

    # 1번째 인자: 번역할 문자열
    @staticmethod
    def _translate(origin_text: str) -> str:
        translated = google_translate(origin_text, "auto", "en")
        if not translated:
            raise forms.ValidationError("구글 번역에 실패했습니다.")
        return translated
