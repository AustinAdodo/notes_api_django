import json
from django.contrib.auth.models import User
from django.test import TestCase


class NoteViewTests1(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="foo")
        self.client.force_login(self.user)

    def test_create_note(self):
        """Test creating a new note."""
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

    def test_get_single_note(self):
        """Test retrieving a single note."""
        created_note = self.create_sample_note()

        response = self.client.get(f"/notes/{created_note['id']}/")
        self.assertEqual(response.status_code, 200)
        expected = {
            "id": created_note["id"],
            "title": created_note["title"],
            "text": created_note["text"],
            "owner": "foo",
        }
        self.assertJSONEqual(response.content, expected)

    def test_get_all_notes(self):
        """Test retrieving all notes."""
        expected_results = [self.create_sample_note() for _ in range(5)]

        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, 200)
        expected = {
            "count": len(expected_results),
            "next": None,
            "previous": None,
            "results": expected_results,
        }
        self.assertJSONEqual(response.content, expected)

    def create_sample_note(self):
        payload = {"title": "aa", "text": "bb"}
        response = self.client.post("/notes/", payload, format="json")
        return json.loads(response.content)

    # Add more test cases for pagination, error handling, etc.
