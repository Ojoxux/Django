from datetime import date

from django.contrib.admin.sites import AdminSite
from django.test import Client, TestCase
from django.urls import reverse

from .admin import EmployeeAdmin
from .forms import EmployeeForm
from .models import Employee


class EmployeeModelTests(TestCase):
    """F-01: 従業員モデル定義"""

    # staff/models.pyの__str__が氏名を返すこと
    def test_str_returns_name(self):
        employee = Employee.objects.create(
            name="山田太郎",
            dept="営業部",
            role="一般",
            email="yamada@example.com",
            joined_date=date(2020, 4, 1),
        )
        self.assertEqual(str(employee), "山田太郎")


class EmployeeAdminTests(TestCase):
    """F-02: 管理画面のカスタマイズ"""

    # staff/admin.pyのlist_displayに4項目が設定されていること
    def test_list_display_shows_four_columns(self):
        admin = EmployeeAdmin(Employee, AdminSite())
        self.assertEqual(admin.list_display, ("name", "dept", "role", "joined_date"))


class EmployeeViewTests(TestCase):
    """F-03&F-04: Viewと表示"""

    @classmethod
    def setUpTestData(cls):
        cls.older = Employee.objects.create(
            name="古い社員",
            dept="営業部",
            role="一般",
            email="old@example.com",
            joined_date=date(2020, 1, 1),
        )
        cls.newer = Employee.objects.create(
            name="新しい社員",
            dept="開発部",
            role="マネージャー",
            email="new@example.com",
            joined_date=date(2024, 6, 1),
        )

    def setUp(self):
        self.client = Client()

    # portal/listの一覧が入社日の新しい順になること
    def test_list_orders_by_joined_date_desc(self):
        response = self.client.get(reverse("employee_list"))
        self.assertEqual(response.status_code, 200)
        names = [employee.name for employee in response.context["employees"]]
        self.assertLess(names.index("新しい社員"), names.index("古い社員"))

    # portal/listに登録件数が表示されること
    def test_list_shows_total_count(self):
        response = self.client.get(reverse("employee_list"))
        self.assertEqual(response.context["total_count"], Employee.objects.count())

    # portal/user/#idの詳細で氏名と入社日が表示されること
    def test_detail_shows_employee_and_joined_date(self):
        response = self.client.get(reverse("employee_detail", args=[self.newer.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "新しい社員")
        self.assertContains(response, str(self.newer.joined_date.year))

    # portal/user/#idで存在しないIDのとき404とメッセージが返ること
    def test_detail_returns_404_for_missing_employee(self):
        response = self.client.get(reverse("employee_detail", args=[9999]))
        self.assertContains(response, "社員が存在しません", status_code=404)


class EmployeeFormTests(TestCase):
    """第5回: 新規社員登録フォーム"""

    def test_form_contains_all_employee_fields(self):
        form = EmployeeForm()
        self.assertEqual(
            list(form.fields),
            ["name", "dept", "role", "email", "joined_date"],
        )

    def test_joined_date_uses_date_input(self):
        form = EmployeeForm()
        self.assertEqual(form.fields["joined_date"].widget.input_type, "date")


class EmployeeCreateViewTests(TestCase):
    """第5回: 新規社員登録画面"""

    def test_get_shows_empty_form(self):
        response = self.client.get(reverse("employee_create"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], EmployeeForm)
        self.assertContains(response, "新規社員登録")
        self.assertContains(response, "登録する")

    def test_valid_post_creates_employee_and_redirects_to_list(self):
        response = self.client.post(
            reverse("employee_create"),
            {
                "name": "田中 花子",
                "dept": "総務部",
                "role": "一般",
                "email": "tanaka@example.com",
                "joined_date": "2026-07-01",
            },
        )

        self.assertRedirects(response, reverse("employee_list"))
        self.assertTrue(
            Employee.objects.filter(
                name="田中 花子",
                email="tanaka@example.com",
            ).exists()
        )

    def test_invalid_post_shows_errors_without_creating_employee(self):
        response = self.client.post(
            reverse("employee_create"),
            {
                "name": "田中 花子",
                "dept": "総務部",
                "role": "一般",
                "email": "invalid-email",
                "joined_date": "2026-07-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "email",
            "有効なメールアドレスを入力してください。",
        )
        self.assertFalse(Employee.objects.filter(name="田中 花子").exists())

    def test_list_has_link_to_create_view(self):
        response = self.client.get(reverse("employee_list"))

        self.assertContains(response, reverse("employee_create"))
        self.assertContains(response, "＋新規社員登録")
