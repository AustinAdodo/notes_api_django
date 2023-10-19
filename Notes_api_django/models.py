from django.db import models


class Note(models.Model):
    objects = None
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    text = models.TextField()
    owner = models.ForeignKey("auth.User", related_name="notes", on_delete=models.CASCADE)

    class Meta:
        ordering = "created",
        # db_table = "custom_table_name"  # Specify your custom table name here

# using = "tests"  # Specify the database alias to use here
