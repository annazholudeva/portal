from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка для команды по удалению новостей из категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            'Вы действительно хотите удалить все новости в категории {options["category"]? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            # Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Удаление отменено'))
            return

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Новости категории {category.name} удалены'))

        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.category_name}'))