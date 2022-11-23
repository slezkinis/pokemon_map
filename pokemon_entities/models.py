from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Имя покемона', max_length=200)
    photo = models.ImageField(verbose_name='Картинка покемона', null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Прошлая эволюция покемона',
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='next_evolutions',
    )
    description = models.TextField(verbose_name='Описание покемона', blank=True)
    title_en = models.CharField(verbose_name='Имя покемона на английском', blank=True, max_length=200)
    title_jp = models.CharField(verbose_name='Имя покемона на японском', max_length=200, blank=True)

    def __str__(self) -> str:
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='К кому привязано местоположения',
        on_delete=models.CASCADE
    )
    lat = models.FloatField(verbose_name='Геог. ширина', null=True)
    lon = models.FloatField(verbose_name='Геог. долгота', null=True)
    appeared_at = models.DateTimeField(verbose_name='Во сколько появится')
    disappeared_at = models.DateTimeField(verbose_name='Во сколько пропадёт')
    level = models.IntegerField(verbose_name='Уровень', default=1, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', default=1, blank=True)
    strength = models.IntegerField(verbose_name='Сила', default=1, blank=True)
    defence = models.IntegerField(verbose_name='Защита', default=1, blank=True)
    stamina = models.IntegerField(verbose_name='Стамина', default=1, blank=True)