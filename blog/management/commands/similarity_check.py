import json
import string

import time
from django.core.management.base import BaseCommand, CommandError
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Checks the similarity of existing posts'

    def handle(self, *args, **options):
        posts = BlogPost.objects.all()
        start = time.time()

        for post in posts:
            post.related_posts.clear()

            post_words_string = post.word_list
            post_words = json.loads(post_words_string)

            similarity = {}
            for compare_post in posts:
                if post is compare_post:
                    continue

                compare_words_string = compare_post.word_list
                compare_words = json.loads(compare_words_string)

                score = calculate_jaccard(set(post_words), set(compare_words))
                similarity[compare_post.id] = score

            post.similarity = json.dumps(similarity)
            post.save()
        print("Similarity calculation completed in %s ms" % int(((time.time()-start) * 1000)))


def calculate_jaccard(set1, set2):
    # Find the intersection set of words for two texts
    intersection = set1.intersection(set2)

    # Find the uninon set of words for two texts
    union = set1.union(set2)

    # Calculate Jaccard similarity score
    # using the division of intersection set with union set
    return float(len(intersection)) / len(union)