# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)

from django.test import TestCase

from .models import Category, Report


class ReportTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Cat1")  # type:ignore Attribute object is unknown
        Report.objects.create(  # type:ignore Attribute object is unknown
            title="Test",
            email="test@test.de",
            category=Category.objects.first(),  # type:ignore Attribute object is unknown
        )

    def test_unpulished_as_default(self):
        report = Report.objects.get(title="Test")  # type:ignore Attribute object is unknown
        self.assertEqual(report.published, False)
