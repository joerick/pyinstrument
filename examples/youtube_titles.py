import json
import urllib2
import collections
import operator


def download():
    url = 'https://gdata.youtube.com/feeds/api/videos?q=&orderby=published&start-index=1&max-results=50&alt=json'
    return urllib2.urlopen(url).read()

def parse(json_data):
    return json.loads(json_data)

def most_common_words(entries):
    word_occurences = collections.defaultdict(int)

    for entry in entries:
        for word in entry['title']['$t'].split():
            if len(word) < 2: 
                continue
            word_occurences[word] += 1

    word_list = sorted(word_occurences.items(), key=operator.itemgetter(1), reverse=True)

    return word_list[0:5]

if __name__ == '__main__':
    data = parse(download())
    entries = data['feed']['entry']

    print 'This most common words were %s' % most_common_words(entries)
