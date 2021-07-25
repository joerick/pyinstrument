import json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import collections
import operator
import sys

WIKIPEDIA_ARTICLE_API_URL = "https://en.wikipedia.org/w/api.php?action=query&titles=Spoon&prop=revisions&rvprop=content&format=json"


def download():
    return urlopen(WIKIPEDIA_ARTICLE_API_URL).read()


def parse(json_data):
    return json.loads(json_data)


def most_common_words(page):
    word_occurences = collections.defaultdict(int)

    for revision in page["revisions"]:
        article = revision["*"]

        for word in article.split():
            if len(word) < 2:
                continue
            word_occurences[word] += 1

    word_list = sorted(word_occurences.items(), key=operator.itemgetter(1), reverse=True)

    return word_list[0:5]


def main():
    data = parse(download())
    page = list(data["query"]["pages"].values())[0]

    sys.stderr.write("This most common words were %s\n" % most_common_words(page))


if __name__ == "__main__":
    main()
