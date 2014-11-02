from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import Menu, SubMenu, QueueCategory, QueueList, QueueOnGoing, NameList, UserDetail

admin.site.unregister(Group)
class SubMenu_AdminInline(admin.StackedInline):
	model = SubMenu
	extra = 1

class Menu_Admin(admin.ModelAdmin):
	list_display = ('name', 'link', 'permissions', 'sub_menu')
	exclude = ('sub_menu',)
	inlines = [SubMenu_AdminInline,]
	class Meta:
		model = Menu
admin.site.register(Menu, Menu_Admin)

class QueueCategory_Admin(admin.ModelAdmin):
	list_display = ('name', 'description')
	class Meta:
		model = QueueCategory
admin.site.register(QueueCategory, QueueCategory_Admin)

class QueueList_Admin(admin.ModelAdmin):
	list_display = ('order_number', 'day', 'date', 'category', 'time')
	class Meta:
		model = QueueList
admin.site.register(QueueList, QueueList_Admin)
admin.site.register(QueueOnGoing)
class UserDetail_Admin(admin.ModelAdmin):
	list_display = ('user', 'category', 'Nick_Name', 'Full_Name')
	class Meta:
		model = UserDetail
admin.site.register(UserDetail, UserDetail_Admin)
admin.site.register(NameList)