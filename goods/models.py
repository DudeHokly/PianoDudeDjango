from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    image_url = models.URLField()
    slug = models.SlugField(unique=True)

    color = models.CharField(
        max_length=50,
        choices=[
            ("Черный", "Черный"),
            ("Коричневый", "Коричневый"),
            ("Белый", "Белый"),
            ("Палисандр", "Палисандр"),
            ("Серый", "Серый"),
            ("Красный", "Красный"),
            ("Синий", "Синий"),
            ("Жёлтый", "Жёлтый"),
        ],
        default="Черный",
    )

    manufacturer = models.CharField(
        max_length=50,
        choices=[
            (m, m)
            for m in ["Yamaha", "Casio", "Roland", "Artesia", "Virtuozo", "Ringway"]
        ],
        default="Yamaha",
    )

    polyphony = models.PositiveIntegerField(
        choices=[(int(p), p) for p in ["16", "32", "48", "64", "80", "128", "256"]],
        default=64,
    )

    keys = models.PositiveIntegerField(
        choices=[(int(k), k) for k in ["61", "68", "73", "76", "88"]],
        default=88,
    )

    metronome = models.BooleanField(default=True)
    recorder = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)

    tones = models.CharField(max_length=50, default="1")

    hammer_keyboard = models.BooleanField(default=False)

    size = models.CharField(max_length=100, default="Стандартные")
    weight = models.PositiveIntegerField(default=15000)

    power = models.CharField(max_length=100, default="От сети 220В")
    warranty = models.CharField(max_length=50, default="12 месяцев")

    sound_effects = models.CharField(max_length=255, default="Reverb")

    key_weight = models.CharField(
        max_length=50,
        choices=[
            ("Взвешенная", "Взвешенная"),
            ("Невзвешенная", "Невзвешенная"),
            ("Полувзвешенная", "Полувзвешенная"),
        ],
        default="Невзвешенная",
    )

    key_size = models.CharField(
        max_length=50,
        choices=[
            ("Полуразмерная", "Полуразмерная"),
            ("Полноразмерная", "Полноразмерная"),
        ],
        default="Полноразмерная",
    )

    interfaces = models.CharField(max_length=255, default="USB")

    def __str__(self):
        return self.name
