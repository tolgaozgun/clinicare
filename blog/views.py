import json
from collections import OrderedDict

from clinic.settings import BLOG_POST_SUGGESTIONS
from blog.forms import BlogPostForm
from blog.models import BlogPost
from django.shortcuts import render, redirect
from django.core.management import call_command
from django.utils.timezone import now
from django.views import View
from panel.views import PanelView


class IndexView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)


class PostView(View):
    def get(self, request, pk):
        try:
            post = BlogPost.objects.get(id=pk)
        except BlogPost.DoesNotExist:
            post = None
        similarities = json.loads(post.similarity)
        top_similarities = get_top_similarities(similarities)
        posts = []
        for similar in top_similarities:
            try:
                post = BlogPost.objects.get(id=similar)
            except BlogPost.DoesNotExist:
                print("error: blog post not found %s" % similar)
            posts.append(post)
        context = {'post': post, 'similar_posts': posts}
        return render(request, 'blog/post.html', context)


class AddPostView(PanelView):
    def get(self, request):
        form = BlogPostForm()
        context = {"current_page": "add_post", "form": form}
        return render(request, 'blog/add_post.html', context)

    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            form.cleaned_data.pop('captcha')

            post = BlogPost(**form.cleaned_data,
                            author=request.user,
                            lastUpdated=now,
                            dateCreated=now)
            post.save()
            call_command('blog_get_wordlist', post.id)
            return redirect('blog:posts')
        else:
            context = {"current_page": "add_post", "form": form}
            return render(request, "blog/add_post.html", context)


class EditPostView(PanelView):
    def get(self, request, pk):
        try:
            post = BlogPost.objects.get(id=pk)
        except BlogPost.DoesNotExist:
            post = None
        form = BlogPostForm(instance=post)
        context = {"current_page": "add_post", "form": form}
        return render(request, 'blog/edit_post.html', context)

    def post(self, request, pk):
        try:
            post = BlogPost.objects.get(id=pk)
        except BlogPost.DoesNotExist:
            post = None
        form = BlogPostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.cleaned_data.pop('captcha')
            post.save()
            return redirect('blog:posts')
        else:
            context = {"current_page": "add_post", "form": form}
            return render(request, "blog/add_post.html", context)


class DeletePostView(PanelView):
    def get(self, request, pk):
        context = {'current_page': 'delete_post'}
        return render(request, 'blog/delete_post.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('blog:post', pk)

        post = BlogPost.objects.get(id=pk)
        post.delete()
        return redirect('blog:posts')


def get_top_similarities(data):
    n = BLOG_POST_SUGGESTIONS
    return OrderedDict(sorted(data.items())[:n])

