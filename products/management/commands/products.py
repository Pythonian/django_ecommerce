import random
import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from faker import Faker
from PIL import Image, ImageOps
from io import BytesIO
from products.models import Category, Product

fake = Faker()


class Command(BaseCommand):
    help = "Populate the database with sample data for the Product model"

    def add_arguments(self, parser):
        parser.add_argument("total", type=int, help="Indicates the number of Products to be created")

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        total = kwargs["total"]
        paragraphs = fake.paragraphs(nb=50)
        text = "\n\n".join(paragraphs)

        # Download images from the API
        api_url = "https://picsum.photos/v2/list?page=1&limit=100"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            images = [item["download_url"] for item in data]
        else:
            images = []

        for _ in range(total):
            name = fake.sentence(nb_words=2)
            slug = slugify(name)
            category = random.choice(categories)
            description = text
            price = fake.random_int(min=1000, max=10000)
            old_price = fake.random_int(min=10000, max=15000)
            sku = fake.unique.random_int(min=10000, max=99999)
            created = fake.date_this_year()

            # Download and crop image for the Product
            if images:
                image_url = random.choice(images)
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    # Open the image using Pillow
                    image = Image.open(BytesIO(image_response.content))

                    # Resize and crop the image
                    image = image.resize((960, 520))
                    width, height = image.size
                    left = (width - 960) / 2
                    top = (height - 520) / 2
                    right = (width + 960) / 2
                    bottom = (height + 520) / 2
                    image = image.crop((left, top, right, bottom))

                    # Convert the image background to gray
                    image = ImageOps.grayscale(image)

                    # Create a temporary file to save the image
                    img_temp = NamedTemporaryFile(delete=True)
                    image.save(img_temp, format="JPEG")
                    img_temp.flush()

                    # Set the image field of the Product model
                    image_filename = image_url.split("/")[-1]
                    image_filename = f"{image_filename}.jpg"
                    image = File(img_temp, name=image_filename)
                else:
                    image = "Product.jpg"
            else:
                image = "Product.jpg"
            # if images:
            #     image_url = random.choice(images)
            #     image_response = requests.get(image_url)
            #     if image_response.status_code == 200:
            #         # Open the image using Pillow
            #         image = Image.open(BytesIO(image_response.content))

            #         # Resize and crop the image
            #         image = image.resize((960, 520))
            #         width, height = image.size
            #         left = (width - 960) / 2
            #         top = (height - 520) / 2
            #         right = (width + 960) / 2
            #         bottom = (height + 520) / 2
            #         image = image.crop((left, top, right, bottom))

            #         # Create a temporary file to save the image
            #         img_temp = NamedTemporaryFile(delete=True)
            #         image.save(img_temp, format="JPEG")
            #         img_temp.flush()

            #         # Set the image field of the Product model
            #         image_filename = image_url.split("/")[-1]
            #         image_filename = f"{image_filename}.jpg"
            #         image = File(img_temp, name=image_filename)
            #     else:
            #         image = "Product.jpg"
            # else:
            #     image = "Product.jpg"

            Product.objects.create(
                name=name,
                slug=slug,
                category=category,
                description=description,
                price=price,
                old_price=old_price,
                sku=str(sku),
                created=created,
                image=image,
            )
        self.stdout.write(self.style.SUCCESS(f"Successfully added {total} Products."))
