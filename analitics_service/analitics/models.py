from django.db import models


class UserWatchData(models.Model):
    user_id = models.IntegerField()
    content_id = models.IntegerField()
    watch_duration = models.IntegerField(help_text="Duration in seconds")
    timestamp = models.DateTimeField(auto_now_add=True)


class UserActivity(models.Model):
    user_id = models.IntegerField()
    content_id = models.IntegerField()
    activity_type = models.CharField(
        max_length=100)  # e.g., 'watched', 'liked'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - {self.activity_type} - Content {self.content_id}"


class Review(models.Model):
    user_id = models.IntegerField()
    content_id = models.IntegerField()
    review_text = models.TextField()
    rating = models.IntegerField()  # Assuming a numerical rating
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by User {self.user_id} for Content {self.content_id}"


class ContentRevenue(models.Model):
    content_id = models.IntegerField()
    subscription_plan_id = models.IntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.movie.title} - {self.date} - Revenue"
