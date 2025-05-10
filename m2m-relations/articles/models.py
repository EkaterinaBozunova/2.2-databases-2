from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    main_section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name='main_articles',
        null=True,
        blank=True,
        help_text='Основной раздел статьи'
    )
    sections = models.ManyToManyField(
        Section,
        through='Scope',
        related_name='articles'
    )
    tags = models.ManyToManyField(
        Tag,
        through='Scope',
        related_name='articles'
    )

    def clean(self):
        super().clean()
        main_scopes = [scope for scope in self.scopes.all() if scope.is_main]
        if len(main_scopes) == 0:
            raise ValidationError('Должен быть выбран один основной раздел.')
        elif len(main_scopes) > 1:
            raise ValidationError('Можно выбрать только один основной раздел.')

    def get_tags_in_order(self):
        scopes = self.scopes.select_related('tag').order_by(
            '-is_main',  # основному сначала
            'tag__name'  # остальные по алфавиту
        )
        return [scope.tag for scope in scopes]
        
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title
    
class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('article', 'tag')