# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)

from django.test import TestCase
from django.urls import reverse

from .models import Category, Report


class ReportTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat = Category.objects.create(name="Cat1")  # type:ignore Attribute object is unknown

    def test_create_report_get(self):
        """
        Test the create report view if get is called
        """
        url = reverse("georeport:create")
        response = self.client.get(url)

        # Test create view
        self.assertEqual(response.status_code, 200)  # type:ignore Attribute status_code unknown
        self.assertTemplateUsed(response, "georeport/create.html")
        # Check if category is in context of request
        self.assertIn(self.cat.id, response.context)  # type:ignore

    def test_create_report_post(self):
        """
        Test create_report_view with a post call
        """
        # Testcase setup
        post_data = {
            "title": "Test",
            "description": "description",
            "category": self.cat.id,
            "email": "test@example.de",
            "longitude": 8.741698,
            "latitude": 51.715841,
        }
        url = reverse("georeport:create")
        response = self.client.post(url, post_data)

        # check response
        self.assertEqual(response.status_code, 302)  # type: ignore
        self.assertEqual(response.url, reverse("georeport:index"))  # type:ignore

        report = Report.objects.get(pk=1, title=post_data["title"])  # type: ignore
        self.assertEqual(report.description, post_data["description"])
        self.assertEqual(report.category.id, post_data["category"])
        self.assertEqual(report.email, post_data["email"])
        self.assertEqual(float(report.latitude), float(post_data["latitude"]))
        self.assertEqual(float(report.longitude), float(post_data["longitude"]))
        self.assertFalse(report.published)
        self.assertEqual(report.state, 0)

    def test_detail_view(self):
        self.assertTrue(True)
        url = reverse("georeport:report", kwargs={"id": 1})
        # Test report not existsing
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # type:ignore
        report = Report.objects.create(  # type:ignore
            title="Test",
            category=self.cat,
            email="test@pinpoint.de",
            longitude=8.741698,
            latitude=51.715841,
        )
        # Test unpulished report
        self.assertFalse(report.published)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # type:ignore

        report.published = True
        report.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertContains(response, f"Title: {report.title}", status_code=200)
        self.assertTemplateUsed(response, "georeport/detail.html")
        # TODO: test if response contains title


class GetCategoryViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Creates a test dataset:
        - Root categories (no parent)
        - Nested categories (children of other categories)
        """
        cls.root1 = Category.objects.create(name="Root 1")  # type: ignore Attribute object unknown
        cls.root2 = Category.objects.create(name="Root 2")  # type: ignore Attribute object unknown

        cls.child1 = Category.objects.create(name="Child 1", parent=cls.root1)  # type: ignore Attribute object unknown
        cls.child2 = Category.objects.create(name="Child 2", parent=cls.root1)  # type: ignore Attribute object unknown
        cls.child3 = Category.objects.create(name="Child 3", parent=cls.root2)  # type: ignore Attribute object unknown

        cls.subchild1 = Category.objects.create(name="SubChild 1", parent=cls.child1)  # type: ignore Attribute object unknown

    def test_get_all_categories(self):
        """
        Test if all categories are within the response
        """
        response = self.client.get(reverse("georeport:category-list"))
        self.assertEqual(response.status_code, 200)  # type: ignore Attribute status_code unknown
        data = response.json()  # type: ignore Attribute json unknown
        expected_ids = {
            self.root1.id,
            self.root2.id,
            self.child1.id,
            self.child2.id,
            self.child3.id,
            self.subchild1.id,
        }
        response_ids = {cat["id"] for cat in data["categories"]}
        self.assertEqual(response_ids, expected_ids)

    def test_get_children_of_valid_category(self):
        """Test that only direct children of a given category are returned when accessing 'subcategories/<id>/'."""
        response = self.client.get(
            reverse("georeport:subcategories", args=[self.root1.id])
        )
        self.assertEqual(response.status_code, 200)  # type: ignore Attribute status_code unknown

        data = response.json()  # type: ignore Attribute json unknown
        expected_ids = {self.child1.id, self.child2.id}
        response_ids = {category["id"] for category in data["categories"]}
        self.assertSetEqual(response_ids, expected_ids)

    def test_get_children_of_category_without_children(self):
        """Test that requesting children of a category with no children returns an empty list."""
        response = self.client.get(
            reverse("georeport:subcategories", args=[self.child2.id])
        )
        self.assertEqual(response.status_code, 200)  # type: ignore Attribute status_code unknown

        data = response.json()  # type: ignore Attribute json unknown
        self.assertEqual(data["categories"], [])

    def test_get_children_of_non_existent_category(self):
        """Test that requesting children of a non-existent category returns an empty list."""
        response = self.client.get(reverse("georeport:subcategories", args=[99999]))
        self.assertEqual(response.status_code, 200)  # type: ignore Attribute status_code unknown

        data = response.json()  # type: ignore Attribute json unknown
        self.assertEqual(data["categories"], [])

    def test_response_format(self):
        """Test that response format is correct."""
        response = self.client.get(reverse("georeport:category-list"))
        self.assertEqual(response.status_code, 200)  # type: ignore Attribute status_code unknown

        data = response.json()  # type: ignore Attribute json unknown
        self.assertIn("categories", data)
        if data["categories"]:  # If categories exist, check their structure
            category = data["categories"][0]
            self.assertIn("id", category)
            self.assertIn("name", category)
