from typing import Any
from django.core.management.base import BaseCommand, CommandError

from app.models import *

class Command(BaseCommand):
    help = "Fill database"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, nargs='?', default=10, help='Ratio value')

    def __first_id_to_generation(self, class_name):
        if len(class_name.objects.all()) > 0:
            return class_name.objects.last().id + 1
        return 1

    def handle(self, *args: Any, **kwargs: Any) -> None:
        ratio = kwargs['ratio']

        TAGS_RATIO = ratio
        USERS_RATIO = ratio
        PROFILES_RATIO = ratio
        QUESTIONS_RATIO = 10 * ratio
        ANSWERS_RATIO = 100 * ratio

        first_tag_id = self.__first_id_to_generation(Tag)
        first_user_id = self.__first_id_to_generation(User)
        first_profile_id = self.__first_id_to_generation(Profile)
        first_question_id = self.__first_id_to_generation(Question)
        first_answer_id = self.__first_id_to_generation(Answer)

        tags = [
            Tag(name=f"tag {tag_id}")
            for tag_id in range(first_tag_id, first_tag_id + TAGS_RATIO)
        ]
        Tag.objects.bulk_create(tags)

        self.stdout.write("Created tags")

        users = [
            User(
                username=f'User {user_id}',
                first_name=f'FirstName{user_id}',
                last_name=f'LastName{user_id}',
                email=f'user{user_id}@gmail.com',
                password=f'pass{user_id}',
            )
            for user_id in range(first_user_id, first_user_id + USERS_RATIO)
        ]
        User.objects.bulk_create(users)

        self.stdout.write("Created users")

        profiles = [
            Profile(
                user=users[user_id % USERS_RATIO],
                avatar="Jacque_Fresco.jpg",
            ) for user_id in range(first_user_id, first_user_id + USERS_RATIO)
        ]
        Profile.objects.bulk_create(profiles)

        self.stdout.write("Created profiles")

        questions = [
            Question(
                title=f"Title of question #{question_id}",
                text=f"Text of question #{question_id}",
                author=profiles[question_id % PROFILES_RATIO],
            )
            for question_id in range(first_question_id, first_question_id + QUESTIONS_RATIO)
        ]
        Question.objects.bulk_create(questions)
        for i in range(len(questions)):
            for j in range(3):
                questions[i].tags.add(tags[(i + j) % TAGS_RATIO])
        
        self.stdout.write("Created questions")

        answers = [
            Answer(
                question=questions[(first_question_id + answer_id) % QUESTIONS_RATIO],
                author=profiles[(first_profile_id + answer_id) % PROFILES_RATIO],
                text=f"Text of answer #{answer_id}",
            )
            for answer_id in range(first_answer_id, first_answer_id + ANSWERS_RATIO)
        ]
        Answer.objects.bulk_create(answers)

        self.stdout.write("Created answers")