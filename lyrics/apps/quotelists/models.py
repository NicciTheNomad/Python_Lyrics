from __future__ import unicode_literals
from django.db import models
from ..users.models import User

# Create your models here.
#Quote - quotelists

class QuoteManager(models.Manager):
    def validate_quote(self, data, user_id):
        errors = []
        if len(data['quote']) == 0:
            errors.append('please enter quote.')
        if len(data['quote_author']) == 0:
            errors.append('please enter author of quote.')    
        if len(data['quote']) < 11 and len(data['quote']) != 0:
            errors.append('Quote must be at least 11 characters.')
        if len(data['quote_author']) < 4 and len(data['quote_author']) != 0:
            errors.append('Author of quote must be at least 4 characters.')
        if not errors:
            new_quote = self.create(
                quote = data['quote'],
                quote_author = data['quote_author'],
                quote_creator = User.objects.get(id=user_id),
                current = User.objects.get(id=user_id)
            )
            return new_quote
        return errors

    def validate_favorite(self, data, user_id, quote_id):
        new_favorite = self.create(
            user = User.objects.get(id=user_id),
            quote = Quote.objects.get(id=quote_id),
        )
        return new_favorite

class Quote(models.Model):
    quote_author = models.CharField(max_length = 255)
    quote = models.TextField()
    quote_creator = models.ForeignKey(User, related_name="creator_of_quote", null=True)
    current = models.ForeignKey(User, related_name="current")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorite(models.Model):
    # on_list = models.BooleanField(default=False)
    quote = models.ForeignKey(Quote, related_name="fav_quote")
    user = models.ForeignKey(User, related_name="fav_user")  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = QuoteManager() 


