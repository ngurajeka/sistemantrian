from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
 # Examples:
	url(r'^$', 'queue.views.home', name='home'),
	url(r'^user/login/$', 'queue.views.user_login', name='user_login'),
	url(r'^panel/loket/$', 'queue.views.panel_loket', name='panel_loket'),
	url(r'^queue/add/$', 'queue.views.queue_add', name='queue_add'),
	url(r'^queue/queue_add_post/$', 'queue.views.queue_add_post', name='queue_add_post'),
	url(r'^queue/getremaining/$', 'queue.views.getRemainingQueue', name='getremaining'),
	url(r'^queue/getongoing/$', 'queue.views.getOnGoingQueue', name='getongoing'),
	url(r'^queue/getordernumber/$', 'queue.views.getQueueOrderNumber', name='getqueueordernumber'),
	url(r'^queue/getqueueforpanelloket/$', 'queue.views.getQueueForPanelLoket', name='getqueueforpanelloket'),
	url(r'^queue/queuecallnext/$', 'queue.views.queueCallNext', name='queuecallnext'),
 # url(r'^blog/', include('blog.urls')),
 url(r'^grappelli/', include('grappelli.urls')),
 url(r'^admin/', include(admin.site.urls)),
)
