import json
import string
import time

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from blog.models import BlogPost


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('post_id', type=int)

    def handle(self, *args, **options):
        start = time.time()
        post_id = options['post_id']
        try:
            post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            raise CommandError('Post %s does not exist' % post_id)

        post_text = post.text
        word_list = get_word_list(post_text)

        json_string = json.dumps(word_list)
        post.word_list = json_string
        post.save()
        print("Word list for post with ID %s is now updated. Took %s ms" % (post_id, int((time.time() - start) * 1000)))
        call_command("similarity_check")


def get_word_list(text):
    stripped_text = text.translate(str.maketrans('', '', string.punctuation))
    return list(set(stripped_text.lower().split()))
