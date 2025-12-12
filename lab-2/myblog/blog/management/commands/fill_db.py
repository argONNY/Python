from django.core.management.base import BaseCommand
from blog.models import Category, Post
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **options):
        # Создаем пользователя
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpassword123')
            user.save()

        # Создаем категории
        categories_data = [
            {'name': 'Программирование', 'description': 'Статьи о программировании'},
            {'name': 'Путешествия', 'description': 'Рассказы о путешествиях'},
            {'name': 'Кулинария', 'description': 'Рецепты и советы по готовке'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(**cat_data)
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

        # Создаем посты
        posts_data = [
            {
                'title': 'Мой первый пост в блоге',
                'content': 'Это содержимое моего первого поста. Я только начинаю вести блог и хочу делиться своими мыслями и идеями.',
                'author': user,
                'category': Category.objects.get(name='Программирование')
            },
            {
                'title': 'Лучшие места для путешествий',
                'content': 'В этом посте я расскажу о самых красивых местах, которые я посетил за последний год.',
                'author': user,
                'category': Category.objects.get(name='Путешествия')
            },
            {
                'title': 'Простой рецепт пасты',
                'content': 'Сегодня поделюсь с вами своим любимым рецептом пасты карбонара.',
                'author': user,
                'category': Category.objects.get(name='Кулинария')
            },{
                'title': 'Мой первый пост в блоге',
                'content': 'Это содержимое моего первого поста. Я только начинаю вести блог и хочу делиться своими мыслями и идеями.',
                'author': user,
                'category': Category.objects.get(name='Программирование')
            },
            {
                'title': 'Лучшие места для путешествий',
                'content': 'В этом посте я расскажу о самых красивых местах, которые я посетил за последний год.',
                'author': user,
                'category': Category.objects.get(name='Путешествия')
            },
            {
                'title': 'Простой рецепт пасты',
                'content': 'Сегодня поделюсь с вами своим любимым рецептом пасты карбонара.',
                'author': user,
                'category': Category.objects.get(name='Кулинария')
            },{
                'title': 'Мой первый пост в блоге',
                'content': 'Это содержимое моего первого поста. Я только начинаю вести блог и хочу делиться своими мыслями и идеями.',
                'author': user,
                'category': Category.objects.get(name='Программирование')
            },
            {
                'title': 'Лучшие места для путешествий',
                'content': 'В этом посте я расскажу о самых красивых местах, которые я посетил за последний год.',
                'author': user,
                'category': Category.objects.get(name='Путешествия')
            },
            {
                'title': 'Простой рецепт пасты',
                'content': 'Сегодня поделюсь с вами своим любимым рецептом пасты карбонара.',
                'author': user,
                'category': Category.objects.get(name='Кулинария')
            },{
                'title': 'Мой первый пост в блоге',
                'content': 'Это содержимое моего первого поста. Я только начинаю вести блог и хочу делиться своими мыслями и идеями.',
                'author': user,
                'category': Category.objects.get(name='Программирование')
            },
            {
                'title': 'Лучшие места для путешествий',
                'content': 'В этом посте я расскажу о самых красивых местах, которые я посетил за последний год.',
                'author': user,
                'category': Category.objects.get(name='Путешествия')
            },
            {
                'title': 'Простой рецепт пасты',
                'content': 'Сегодня поделюсь с вами своим любимым рецептом пасты карбонара.',
                'author': user,
                'category': Category.objects.get(name='Кулинария')
            },
        ]

        for post_data in posts_data:
            post = Post.objects.create(**post_data)
            post.publish()  # Устанавливаем дату публикации
            self.stdout.write(f'Создан пост: {post.title}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))