from __future__ import absolute_import

from mixer.backend.django import mixer

from .models import User, Post, Comment

from avalon import story, avalon


@story
def create_user():
    user = mixer.blend(User, is_active=False)
    return user


@story(chance=80)
def approve_user(user):
    user.is_active = True
    user.save()


@story
def write_post():
    post = mixer.blend(Post, user=mixer.select(is_active=True))
    return post


@story
def write_comment(post=None):
    if not post:
        post = Post.objects.order_by('?')[0]

    mixer.blend(
        Comment, post=Post, user=mixer.select(is_active=True))

    return post


@story
def make_rating(post=None):
    if not post:
        post = Post.objects.order_by('?')[0]

    post.rating += 1
    post.save()
    return post


avalon.register(create_user & approve_user)
avalon.register(make_rating, timeout=10)
avalon.register(write_post, timeout=20)
avalon.register(write_post & (
    story(write_comment, chance=30, cycle=5) | make_rating
))

if __name__ == 'main':
    avalon.run()


# lint_ignore=C0110
