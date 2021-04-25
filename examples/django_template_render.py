import os
from optparse import OptionParser

try:
    import django
except ImportError:
    print("This example requires Django.")
    print("Install using `pip install Django`.")
    exit(1)

import django.conf
import django.template.loader


def main():
    parser = OptionParser()
    parser.add_option(
        "-i",
        "--iterations",
        dest="iterations",
        action="store",
        type="int",
        help="number of template render calls to make",
        default=100,
    )
    options, _ = parser.parse_args()

    os.chdir(os.path.dirname(__file__))

    django.conf.settings.configure(
        INSTALLED_APPS=(),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": ["./django_example/django_example/templates"],
            }
        ],
    )
    django.setup()

    for _ in range(0, options.iterations):
        django.template.loader.render_to_string("template.html")


if __name__ == "__main__":
    main()
