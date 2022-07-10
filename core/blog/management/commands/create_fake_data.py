from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Category, Post
from random import choice
from datetime import datetime

categoryList = [
    'programming',
    'django',
    'nodeJs',
    'AI',
    'machine learning',
]

class Command(BaseCommand):
    help = 'creating 10 users who each of them create 10 posts'

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        # creating 10 users
        for __ in range(10):
            user = User.objects.create_user(email=self.faker.email(), password='complexpassword123@')
            profile = Profile.objects.get(user=user)
            profile.first_name = self.faker.first_name()
            profile.last_name = self.faker.last_name()
            profile.description = self.faker.paragraph(nb_sentences=5)
            profile.save()

            for name in categoryList:
                Category.objects.get_or_create(name=name)

            # creating 10 posts by each user
            for _ in range(10):
                Post.objects.create(
                    author = profile,
                    title = self.faker.paragraph(nb_sentences=1),
                    content = self.faker.paragraph(nb_sentences=10),
                    status = choice([True, False]),
                    category = Category.objects.get(name=choice(categoryList)),
                    published_date = datetime.now()
                )
