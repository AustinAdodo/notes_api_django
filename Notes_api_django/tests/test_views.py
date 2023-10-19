import json
from django.contrib.auth.models import User
from django.test import TestCase

TestCase.maxDiff = None


class NoteViewTests(TestCase):
    def test_post_notes(self):
        """POST /notes/"""
        user = User.objects.create(username="foo")
        self.client.force_login(user)
        payload = {"title": "aa", "text": "bb"}
        response = self.client.post("/notes/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        expected = {
            "id": 1,
            "title": "aa",
            "text": "bb",
            "owner": "foo",
        }
        self.assertJSONEqual(response.content, expected)

    def test_get_notes(self):
        """GET /notes/"""
        user = User.objects.create(username="foo")
        self.client.force_login(user)
        payload = {"title": "aa", "text": "bb"}
        response = self.client.post("/notes/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        expected = {
            "id": 1,
            "title": "aa",
            "text": "bb",
            "owner": "foo",
        }
        self.assertJSONEqual(response.content, expected)
        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "title": "aa",
                    "text": "bb",
                    "owner": "foo",
                }
            ]
        }
        response = self.client.get("/notes/")
        self.assertJSONEqual(response.content, expected)

    def test_pagination_size(self):
        """pagination size"""
        page_size = 10
        user = User.objects.create(username="foo")
        self.client.force_login(user)
        results = []

        for i in range(1, page_size + 2):
            payload = {"title": f"aa_{i}", "text": f"bb_{i}"}
            response = self.client.post("/notes/", payload, format="json")
            self.assertEqual(response.status_code, 201)
            expected = {
                "id": i,
                "title": f"aa_{i}",
                "text": f"bb_{i}",
                "owner": "foo",
            }
            self.assertJSONEqual(response.content, expected)
            results.append(expected)

        expected = {
            "count": page_size + 1,
            "next": "http://testserver/notes/?page=2",
            "previous": None,
            "results": results[:page_size],
        }
        response = self.client.get("/notes/")
        self.assertJSONEqual(response.content, expected)

    def test_pagination_invalid_page(self):
        """pagination -- invalid page"""
        user = User.objects.create(username="foo")
        self.client.force_login(user)
        response = self.client.get("/notes/?page=1")
        expected = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        }
        self.assertJSONEqual(response.content, expected)

    def test_pagination_bad_request(self):
        """pagination -- bad request"""
        user = User.objects.create(username="foo")
        self.client.force_login(user)
        response = self.client.get("/notes/?page=0")
        self.assertJSONEqual(response.content, {"detail": "Invalid page."})
