from typing import Any
from django.core.management.base import BaseCommand

from app.models import *

from tqdm import tqdm
import time

from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = "Fill database"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, nargs='?', default=10, help='Ratio value')

    def __first_id_to_generation(self, class_name):
        if len(class_name.objects.all()) > 0:
            return class_name.objects.last().id + 1
        return 1
    
    def __random_like_value(self, id):
        return id % 2 == 0

    def handle(self, *args: Any, **kwargs: Any) -> None:
        time_begin = time.time()

        ratio = kwargs['ratio']

        TAGS = ratio
        USERS = ratio
        PROFILES = ratio
        QUESTIONS = 10 * ratio
        ANSWERS = 100 * ratio
        QUESTION_LIKES = 100 * ratio
        ANSWER_LIKES = 100 * ratio

        first_tag_id = self.__first_id_to_generation(Tag)
        first_user_id = self.__first_id_to_generation(User)
        first_profile_id = self.__first_id_to_generation(Profile)
        first_question_id = self.__first_id_to_generation(Question)
        first_answer_id = self.__first_id_to_generation(Answer)
        first_question_like_id = self.__first_id_to_generation(QuestionLike)
        first_answer_like_id = self.__first_id_to_generation(AnswerLike)


        self.stdout.write("Creating tags")
        tags = [
            Tag(name=f"tag {tag_id}")
            for tag_id in range(first_tag_id, first_tag_id + TAGS)
        ]
        Tag.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS("Tags created"))


        self.stdout.write("Creating users")
        users = [
            User(
                username=f'user_{user_id}',
                first_name=f'first_name_{user_id}',
                last_name=f'last_name_{user_id}',
                email=f'user_{user_id}@gmail.com',
                password=make_password(f'password_{user_id}'),
            )
            for user_id in tqdm(range(first_user_id, first_user_id + USERS))
        ]
        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS("Users created"))


        self.stdout.write("Creating profiles")
        profiles = [
            Profile(
                user=users[profile_id % USERS],
            ) for profile_id in range(first_profile_id, first_profile_id + PROFILES)
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS("Profiles created"))


        self.stdout.write("Creating questions")
        questions = [
            Question(
                title=f"Title of question #{question_id}",
                text=f"Text of question #{question_id}",
                author=profiles[question_id % PROFILES],
            )
            for question_id in range(first_question_id, first_question_id + QUESTIONS)
        ]
        Question.objects.bulk_create(questions)
        for i in tqdm(range(len(questions))):
            for j in range(3):
                questions[i].tags.add(tags[(i + j) % TAGS])
        
        self.stdout.write(self.style.SUCCESS("Questions created"))

        self.stdout.write("Creating answers")
        answers = [
            Answer(
                question=questions[answer_id % QUESTIONS],
                author=profiles[answer_id % PROFILES],
                text=f"Text of answer #{answer_id}",
            )
            for answer_id in range(first_answer_id, first_answer_id + ANSWERS)
        ]
        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS("Answers created"))


        self.stdout.write("Creatings question likes")
        quistion_likes = [
            QuestionLike(
                question=questions[question_id % QUESTIONS],
                user=profiles[(question_id + i) % PROFILES], # По 10 разных пользователей на каждый вопрос
                value=self.__random_like_value(question_id),
            )
            for question_id in range(first_question_id, first_question_id + QUESTIONS)
            for i in range(10)
        ]
        QuestionLike.objects.bulk_create(quistion_likes)
        self.stdout.write(self.style.SUCCESS("Question likes created"))


        self.stdout.write("Creating answer likes")
        answer_likes = [
            AnswerLike(
                answer=answers[answer_id % ANSWERS],
                user=profiles[(answer_id + i) % PROFILES], # По 10 разных пользователей на каждый ответ
                value=self.__random_like_value(answer_id),
            )
            for answer_id in range(first_answer_like_id, first_answer_like_id + ANSWERS)
            for i in range(10)
        ]
        AnswerLike.objects.bulk_create(answer_likes)
        self.stdout.write(self.style.SUCCESS("Answer likes created"))


        time_end = time.time()
        time_total = time_end - time_begin
        self.stdout.write(f"Total time: {round(time_total, 4)} seconds")
