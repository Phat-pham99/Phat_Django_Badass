from typing import cast

from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from redis_ui import services


class ServiceTests(TestCase):
    def setUp(self) -> None:
        self.fake_client = MagicMock()
        patcher = patch("redis_ui.services.get_redis", return_value=self.fake_client)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_list_keys_returns_keys(self) -> None:
        self.fake_client.scan.return_value = (0, ["balance_cash", "expense_cash"])
        keys, cursor = services.list_keys(pattern="*", count=100)
        self.assertEqual(keys, ["balance_cash", "expense_cash"])
        self.assertEqual(cursor, 0)

    def test_list_keys_iterates_until_cursor_zero(self) -> None:
        self.fake_client.scan.side_effect = [
            (1, ["a"]),
            (0, ["b"]),
        ]
        keys, cursor = services.list_keys(pattern="*", count=100)
        self.assertEqual(keys, ["a", "b"])
        self.assertEqual(cursor, 0)
        self.assertEqual(self.fake_client.scan.call_count, 2)

    def test_set_key_without_ttl(self) -> None:
        services.set_key("foo", "bar")
        self.fake_client.set.assert_called_once_with("foo", "bar")

    def test_set_key_with_ttl(self) -> None:
        services.set_key("foo", "bar", ttl_seconds=60)
        self.fake_client.set.assert_called_once_with("foo", "bar", ex=60)

    def test_get_key_info(self) -> None:
        self.fake_client.exists.return_value = 1
        self.fake_client.type.return_value = "string"
        self.fake_client.ttl.return_value = -1
        self.fake_client.get.return_value = "42"
        info = services.get_key_info("balance_cash")
        self.assertEqual(info["key"], "balance_cash")
        self.assertEqual(info["exists"], 1)
        self.assertEqual(info["type"], "string")
        self.assertEqual(info["value"], "42")

    def test_delete_key(self) -> None:
        self.fake_client.delete.return_value = 1
        self.assertEqual(services.delete_key("foo"), 1)


class RedisManagerAccessTests(TestCase):
    def test_anonymous_redirected_to_admin_login(self) -> None:
        response = cast(HttpResponse, self.client.get(reverse("redis_manager")))
        self.assertRedirects(response, "/admin/login/?next=/redis/")

    def test_non_staff_redirected_to_admin_login(self) -> None:
        user = User.objects.create_user(username="peasant", password="pass")
        self.client.force_login(user)
        response = cast(HttpResponse, self.client.get(reverse("redis_manager")))
        self.assertRedirects(response, "/admin/login/?next=/redis/")

    def test_staff_can_view(self) -> None:
        staff = User.objects.create_user(
            username="admin", password="pass", is_staff=True
        )
        self.client.force_login(staff)
        with patch("redis_ui.services.get_redis") as mock_get_redis:
            fake_client = MagicMock()
            fake_client.scan.return_value = (0, ["balance_cash", "expense_cash"])
            mock_get_redis.return_value = fake_client
            response = cast(HttpResponse, self.client.get(reverse("redis_manager")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Redis Proxy Interface")
        self.assertContains(response, "balance_cash")

    def test_staff_can_set_value(self) -> None:
        staff = User.objects.create_user(
            username="admin", password="pass", is_staff=True
        )
        self.client.force_login(staff)
        with patch("redis_ui.services.get_redis") as mock_get_redis:
            fake_client = MagicMock()
            fake_client.scan.return_value = (0, [])
            fake_client.set.return_value = "OK"
            mock_get_redis.return_value = fake_client
            response = cast(HttpResponse, self.client.post(
                reverse("redis_manager"),
                {"action": "set", "key": "foo", "value": "bar"},
            ))
        self.assertEqual(response.status_code, 200)
        fake_client.set.assert_called_once_with("foo", "bar")