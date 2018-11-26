''' 定义learning_logs的url模式 '''

from django.urls import path
from . import views

urlpatterns = [
    # 主页
    path('', views.index, name='index'),

    # 显示所有主题
    path('topics/', views.topics, name='topics'),

    # 特定主题的详细页面
    path('topic/<int:topic_id>', views.topic, name='topic'),

    # 用于添加新主题的网页
    path('new_topic/', views.new_topic, name='new_topic'),

    # 添加新条目
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),

    # 编辑条目
    path('edit_entry<int:entry_id>', views.edit_entry, name='edit_entry')
]
