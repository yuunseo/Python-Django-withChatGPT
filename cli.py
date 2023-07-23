# openai로부터 받은 api_key 사용을 위한 준비
import os
import openai
import pygame
from io import BytesIO
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# 상황극 설정
language = "English"
gpt_name = "Steve"
level_string = f"a beginner in {language}"
level_word = "simple"
situation_en = "make new friends"
my_role_en = "me"
gpt_role_en = "new friend"


# 프롬프트 작성
SYSTEM_PROMPT = (
    f"You are helpful assistant supporting people learning {language}. "
    f"Your name is {gpt_name}. Please assume that the user you are assisting "
    f"is {level_string}. And please write only the sentence without "
    f"the character role."
)

USER_PROMPT = (
    f"Let's have a conversation in {language}. Please answer in {language} only "
    f"without providing a translation. And please don't write down the "
    f"pronunciation either. Let us assume that the situation in '{situation_en}'. "
    f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
    f"Please make sure that "
    f"I'm {level_string}, so please use {level_word} words as much as possible. "
    f"Now, start a conversation with the first sentence!"
)

RECOMMEND_PROMPT = (
    f"Can you please provide me an {level_word} example "
    f"of how to respond to the last sentence "
    f"in this situation, without providing a translation "
    f"and any introductory phrases or sentences."
)

# 전역변수로, 대화 내역을 쌓는 리스트.
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


# gpt의 응답을 받는 함수. skip_save라는 인자를 넣음으로써 대화 내역 누적 여부 결정
def gpt_query(user_query: str, skip_save: bool = False) -> str:
    "유저 메세지에 대한 응답을 반환합니다."

    global messages

    # 유저 입력을 받으면 API호출 전, message 리스트에 user role로서 메시지를 추가한다.
    messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    # messages를 gpt에게 넘겨준다.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # 응답에서 우리가 필요한 문자열만 뽑아서 반환한다.
    assistant_message = response["choices"][0]["message"]["content"]

    if skip_save == False:
        # 대답한 응답도 messages에 누적이 돼야 하니까 append해 줘야 한다.
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )

    return assistant_message


def play_file(file_path: str) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.quit()


def say(message: str, lang: str) -> None:
    io = BytesIO()

    gTTS(message, lang=lang).write_to_fp(io)

    with NamedTemporaryFile() as f:
        f.write(io.getvalue())
        play_file(f.name)


def main():
    # main함수를 실행하면, USER_PROMPT문자열을 출력해 사용자의 입력을 받아서 넘긴다.
    assistant_message = gpt_query(USER_PROMPT)
    print(f"[assistant] {assistant_message}")

    while line := input("[user] ").strip():
        if line == "!recommend":
            recommended_message = gpt_query(RECOMMEND_PROMPT, skip_save=True)
            print("추천 표현: ", recommended_message)
        elif line == "!say":
            say(messages[-1]["content"], "en")
        else:
            response = gpt_query(line)
            print(f"[assistant] {response}")


if __name__ == "__main__":
    main()
