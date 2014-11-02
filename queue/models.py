from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

"define some choices"
choices_icon = (
		('icon-home', 'Home'),
		('icon-desktop', 'Desktop'),
		('icon-dashboard', 'DashBoard'),
		('icon-user', 'User'),
		('icon-off', 'Off'),
		('icon-list', 'LIst'),
	)
choices_permissions = (
		(0, 'All'),
		(1, 'Only Loket'),
		(2, 'Only HelpDesk'),
		(3, 'Loket and HelpDesk'),
		(4, 'Admin Only'),
	)
choices_category_menu = (
		(0, 'NavBar Left'),
		(1, 'NavBar Right'),
		(2, 'Sidebar Menu'),
	)
choices_yes_no = (
		(1, 'Yes'), (0, 'No'),
	)
choices_genre = (
		('Male', 'Male'), ('Female', 'Female'),
	)
choices_days = (
		(1, 'Monday'),
		(2, 'Tuesday'),
		(3, 'Wednesday'),
		(4, 'Thursday'),
		(5, 'Friday'),
		(6, 'Saturday'),
		(7, 'Sunday'),
	)
choices_usertype = (
		(1, 'Loket'),
		(2, 'HelpDesk'),
	)
choices_process = (
		(0, 'Not Yet'),
		(1, 'OnGoing'),
		(2, 'Done'),
	)

"define Menu Class"
class Menu(models.Model):
	class Meta:
		db_table = "menu"
		verbose_name=u'Menu'
		verbose_name_plural=u'Menu List'
	name = models.CharField(max_length=20,verbose_name=u'Menu Name')
	link = models.CharField(max_length=55,verbose_name=u'Menu Link',help_text='Started with / if a local link')
	icon = models.CharField(max_length=20,choices=choices_icon,default='icon-list',null=True)
	permissions = models.IntegerField(default=0,verbose_name='User Permissions',choices=choices_permissions)
	order = models.IntegerField()
	category = models.IntegerField(choices=choices_category_menu,default=0,verbose_name='Choose a category for this menu')
	sub_menu = models.IntegerField(default=0,verbose_name='Total SubMenu')

	def __unicode__(self):
		return self.name
	def getSubMenu(self):
		return SubMenu.objects.filter(menufrom=self.pk)

class SubMenu(models.Model):
	class Meta:
		db_table = "submenu"
		verbose_name='Sub Menu'
		verbose_name_plural="Sub Menu List"
	name = models.CharField(max_length=20,verbose_name='Sub Menu Name')
	link = models.CharField(max_length=55,verbose_name='Sub Menu Link',help_text='Started with / if a  local link')
	icon = models.CharField(max_length=20,choices=choices_icon,default='icon-list',null=True)
	permissions = models.IntegerField(default=0,verbose_name='User Permissions',choices=choices_permissions)
	order = models.IntegerField()
	menufrom = models.ForeignKey(Menu,verbose_name='Menu from')

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		super(SubMenu, self).save(*args, **kwargs)
		menu = Menu.objects.get(pk=self.menufrom_id)
		menu.sub_menu = menu.sub_menu+1
		menu.save()

	def delete(self, *args, **kwargs):
		super(SubMenu, self).save(*args, **kwargs)
		menu = Menu.objects.get(pk=self.menufrom_id)
		menu.sub_menu = menu.sub_menu - 1
		menu.save()

class QueueCategory(models.Model):
	class Meta:
		db_table = 'queue_kategori'
		verbose_name='Queue Category'
		verbose_name_plural='Queue Category'
	name = models.CharField(max_length=20,verbose_name='Category Name')
	description = models.TextField(max_length=512,verbose_name='Description')

	def __unicode__(self):
		return self.name

class QueueList(models.Model):
	class Meta:
		db_table = 'queue_list'
		verbose_name='Queue List'
		verbose_name_plural='Queue List'
	day = models.IntegerField(choices=choices_days,default=1)
	date = models.DateField()
	category = models.ForeignKey(QueueCategory)
	order_number = models.CharField(max_length=10)
	time = models.TimeField(auto_now=True,auto_now_add=True)
	process = models.SmallIntegerField(default=0,choices=choices_process)

	def __unicode__(self):
		return unicode(self.order_number)

class QueueSound(models.Model):
	class Meta:
		db_table = 'queue_sound'
		verbose_name='Queue Sound'
		verbose_name_plural='Queue Sound'
	queue = models.OneToOneField(QueueList)
	date = models.DateField(auto_now_add=True,auto_now=True)
	time = models.TimeField(auto_now=True,auto_now_add=True)

	def __unicode__(self):
		return unicode(self.pk)

class QueueOnGoing(models.Model):
	class Meta:
		db_table = 'queue_ongoing'
		verbose_name='Queue On Going'
		verbose_name_plural='List Queue On Going'
	queue = models.OneToOneField(QueueList,unique=True,limit_choices_to={'process':0})
	user = models.OneToOneField(User,unique=True,limit_choices_to={'is_staff':False})
	date = models.DateField()

	def __unicode__(self):
		return unicode(self.pk)

class NameList(models.Model):
	class Meta:
		db_table = 'namelist'
		verbose_name='Name List'
		verbose_name_plural='Name List'
	nickname = models.CharField(max_length=20,verbose_name='Nick Name',unique=True)
	fullname = models.CharField(max_length=36,verbose_name='Full Name')

	def __unicode__(self):
		return self.nickname

class UserDetail(models.Model):
	class Meta:
		db_table='user_detail'
		verbose_name_plural='User Details'
		verbose_name='User Detail'
	user = models.OneToOneField(User,unique=True,verbose_name='Choose a user',limit_choices_to={'is_staff':False})
	category = models.SmallIntegerField(choices=choices_usertype,default=1)
	fromnamelist = models.OneToOneField(NameList,unique=True)

	def __unicode__(self):
		return unicode(self.user)

	def Nick_Name(self):
		return unicode(NameList.objects.get(pk=self.fromnamelist_id).nickname)

	def Full_Name(self):
		return unicode(NameList.objects.get(pk=self.fromnamelist_id).fullname)