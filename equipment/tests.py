from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BorrowRecord, Category, Equipment, MaintenanceRecord


class DashboardAndMaintenanceTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            username='admin',
            password='secret',
            is_staff=True,
            is_superuser=True,
        )
        self.user = User.objects.create_user(username='student', password='secret')
        self.category = Category.objects.create(name='Máy tính')

        self.available = Equipment.objects.create(
            name='Laptop Dell',
            category=self.category,
            serial_number='LT-001',
            status='available',
            purchase_date='2024-01-01',
            description='Máy mới',
        )
        self.broken = Equipment.objects.create(
            name='Máy ảnh',
            category=self.category,
            serial_number='MA-001',
            status='broken',
            purchase_date='2023-12-01',
            description='Hỏng màn hình',
        )
        self.overdue = Equipment.objects.create(
            name='Máy in',
            category=self.category,
            serial_number='MI-001',
            status='borrowed',
            purchase_date='2024-02-01',
            description='Đang mượn quá hạn',
        )

        BorrowRecord.objects.create(
            equipment=self.overdue,
            borrower=self.user,
            borrow_date=timezone.now() - timedelta(days=20),
            expected_return_date=timezone.now() - timedelta(days=3),
            actual_return_date=None,
            is_returned=False,
        )

        self.record = MaintenanceRecord.objects.create(
            equipment=self.available,
            maintenance_date='2025-01-10',
            description='Thay pin',
            cost='150000',
            next_maintenance_date='2025-02-10',
        )

    def test_dashboard_shows_status_counts_and_overdue_equipment(self):
        client = Client()
        client.force_login(self.admin)

        response = client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Đang rảnh')
        self.assertContains(response, 'Đang hỏng')
        self.assertContains(response, 'Quá hạn')
        self.assertContains(response, self.overdue.name)

    def test_maintenance_page_lists_and_allows_new_record(self):
        client = Client()
        client.force_login(self.user)

        response = client.get(reverse('equipment_maintenance', args=[self.available.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.record.description)

        response = client.post(
            reverse('equipment_maintenance', args=[self.available.pk]),
            {
                'maintenance_date': '2025-02-15',
                'description': 'Vệ sinh máy',
                'cost': '250000',
                'next_maintenance_date': '2025-03-15',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            MaintenanceRecord.objects.filter(
                equipment=self.available,
                description='Vệ sinh máy',
            ).exists()
        )
