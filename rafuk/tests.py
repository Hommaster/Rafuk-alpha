from django.test import TestCase
from  .models import Categories, UserPr


class TestCategory(TestCase):

    def setUp(self):
        self.category = Categories.objects.create(
            name="a name here",
            slug="a slug here",
        )
        self.category.save()

    def test_category(self):
        self.name = self.category.name
        self.slug = self.category.slug

        self.assertEqual(self.name, "a name here")
        self.assertEqual(self.slug, "a slug here")



