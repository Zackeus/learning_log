from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, EntryForm
from .models import Topic, Entry

# Create your views here.


def index(request):
    """ 学习笔记的主页 """
    return render(request, 'learning_logs/index.html')


@login_required()
def topics(request):
    """ 显示所有的主题 """
    context = {'topics': Topic.objects.filter(
        owner=request.user).order_by('date_added')}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """ 显示单个主题及其所有的条目 """
    topic_data = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic_data.owner != request.user:
        raise Http404
    entries = topic_data.entry_set.order_by('-date_added')
    context = {'topic': topic_data, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
    """ 添加新主题 """
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据u，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            topic_data = form.save(commit=False)
            topic_data.owner = request.user
            topic_data.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """ 在特定的主题中添加新条目 """
    topic_data = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建新表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry_data = form.save(commit=False)
            entry_data.topic = topic_data
            entry_data.save()
            return HttpResponseRedirect(
                reverse(
                    'learning_logs:topic',
                    args=[topic_id]))

    context = {'topic': topic_data, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """ 编辑既有条目 """
    entry = Entry.objects.get(id=entry_id)
    topic_data = entry.topic

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'learning_logs:topic',
                    args=[
                        topic_data.id]))

    context = {'entry': entry, 'topic': topic_data, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
