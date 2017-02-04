from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from ..login_reg.models import User

class ItemManager(models.Manager):

    def validItem(self, request):
        errors = []

        if Item.objects.filter(itm=request.POST['itm']):
            errors.append("That Item already exists!")

        if len(request.POST['itm']) < 4:
            errors.append("The Item field may not be left blank and must contain at least 4 characters.")

        if errors:
            return(False, errors)

        curr_user = User.objects.get(id=request.session['user']['id'])

        item = self.create(creator=curr_user, itm=request.POST['itm'], addby=request.POST['addby'], dateadd=request.POST['dateadd'])

        return (True, item)

    def fetch_item_users(self, item_id):
        print "banana"
        item_id = int(item_id)
        item = self.get(id=item_id)
        users = item.users.all()
        return (item, users)

    def remove_item(self, user_id, item_id):
        int(item_id)
        # get user and itms to remove
        try:
            user = User.objects.get(id=user_id)
            item = self.get(id=item_id)
            item.users.remove(user)
            return True
        except:
            return False

    def add_item(self, user_id, item_id):
        int(item_id)
        # get user and items to add
        try:
            user = User.objects.get(id=user_id)
            item = self.get(id=item_id)
            item.users.add(user)
            return True
        except:
            return False

    def get_my_items(self, user_id):
        items = self.filter(users__id=user_id)
        return items

    def get_other_items(self, user_id):
        items = self.exclude(users__id=user_id)
        return items


    def update(self, id, form_info):
        item = Item.objects.get(id=id)
        item.itm = form_info['itm']
        item.addby = form_info['addby']
        item.dateadd = form_info['dateadd']
        item.save()


class Item(models.Model):
    users = models.ManyToManyField(User, related_name="items")
    creator = models.ForeignKey(User)
    itm = models.CharField(max_length=45)
    addby = models.CharField(max_length=200)
    dateadd = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
