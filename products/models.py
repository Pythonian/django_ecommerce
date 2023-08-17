# from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidators
from django.core.files import File
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
# from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from PIL import Image

from accounts.models import User


class Category(models.Model):
    """
    Product category table
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("category name"),
        help_text=_("format: required, max-50"),
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("category safe URL"),
        help_text=_(
            "format: required, letters, numbers, underscore, or hyphens"
        ),
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_("category description"),
        blank=True,
        help_text=_("format: not required, max-1000"),
    )
    # ordering = models.PositiveIntegerField(default=0)
    # image = models.ImageField(
    #     verbose_name=_("image"),
    #     help_text=_("Upload a category image"),
    #     upload_to="categories/",
    # )

    class Meta:
        ordering = ("name",)
        # ordering = ['ordering']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def get_absolute_url(self):
        return reverse('products:category',
                       kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class Product(models.Model):
    """
    Product details table
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name=_("products"),
        verbose_name=_("category"),
        help_text=_("format: required"),
    )
    # uuid, impressions
    name = models.CharField(
        unique=True,
        max_length=255,
        verbose_name=_("name"),
        help_text=_("format: required, max-255"),
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        verbose_name=_("product safe URL"),
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens"
        ),
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_("product description"),
        help_text=_("format: required"),
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name=_("price"),
        help_text=_("format: maximum price 99999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 99999.99."),
            },
        },
    )
    image = models.ImageField(
        verbose_name=_("image"),
        # help_text=_("Upload a product image. It should not be more than 2MB and should be in High Definition (HD)."),
        upload_to="images/",
    )
    thumbnail = models.ImageField(
        verbose_name=_("thumbnail"),
        upload_to="thumbnails/",
        null=True,
        blank=True,
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text (Optional):"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(
        default=True,
        verbose_name=_("product availability"),
    )
    # units = models.IntegerField(
    #     default=0,
    #     verbose_name=_("units"),
    #     help_text=_("format: required, default-0"),
    # )
    units_sold = models.IntegerField(
        default=0,
        verbose_name=_("units sold to date"),
        help_text=_("format: required, default-0"),
    )
    vendor = models.ForeignKey(
        User, #Vendor
        related_name=_("products"),
        on_delete=models.CASCADE
    )
    featured = models.BooleanField(default=False)
    # trailer = models.FileField(
    #     upload_to='trailers',
    #     blank=True, null=True,
    #     validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    # )
    created = models.DateTimeField(
        # defaul=timezone.now,
        auto_now_add=True,
        verbose_name=_("created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date product last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    objects = models.Manager()
    active = ProductManager()

    class Meta:
        ordering = ("-created",)
        verbose_name = _("product")
        verbose_name_plural = _("products")
        # index_together = (('uuid', 'slug'),)

    def get_absolute_url(self):
        return reverse('products:detail',
                       kwargs={'slug': self.slug})

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(240, 180)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def average_review(self):
        reviews = Review.objects.filter(
            product=self, is_visible=True).aggregate(average=Avg('rating'))
        avg = 0.0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = Review.objects.filter(
            product=self, is_visible=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    rating = models.FloatField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent_data = models.CharField(
        max_length=255, blank=True, null=True)
    thumbsup = models.IntegerField(default="0")
    thumbsdown = models.IntegerField(default="0")
    thumbs = models.ManyToManyField(
        User, related_name="thumbs", default=None, blank=True)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.subject


class ReviewVote(models.Model):
    review = models.ForeignKey(
        Review, related_name="reviewid", on_delete=models.CASCADE,
        default=None, blank=True)
    user = models.ForeignKey(
        User, related_name="userid", on_delete=models.CASCADE,
        default=None, blank=True)
    vote = models.BooleanField(default=True)
    