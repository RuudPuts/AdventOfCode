#!/usr/bin/env python3

import os
import sys
import re
import requests
from jinja2 import Environment, FileSystemLoader


SESSION = 'AOC_SESSION_COOKIE'


def fetch_day(year, day, path_suffix=''):
    print("Fetching %s day %s %s" % (year, day, path_suffix))
    url = "https://adventofcode.com/%s/day/%s%s" % (year, day, path_suffix)
    return requests.get(url, headers={'Cookie': "session=%s" % SESSION, 'User-Agent': "https://github.com/RuudPuts/AdventOfCode by ruud.puts@gmail.com"}).text.strip()


def write_file(year, filename, content):
    print("Writing to %s/%s" % (year, filename))

    with open("%s/%s" % (year, filename), "w+") as file:
        file.write(content)


def fetch_description(year, day):
    print("Fetching description")
    return fetch_day(year, day).strip()


def parse_description(description):
    description = description.split("<main>")[1].split("</main>")[0].split('To begin, <a href="')[0].split('Although it hasn\'t changed')[0].split('You can also <span class="share">[Share<span class="share-content">on')[0]

    remove_regexes = [
        r"<script>.*?<\/script>",
        r"<article class=\"day-desc\">",
        r"<\/article>",
        r"<ul>",
        r"<\/ul>",
        r"<\/li>",
    ]

    for regex in remove_regexes:
        description = re.sub(regex, '', description)

    replace_actions = {
        '<p>': '\n',
        '</p>': '\n',
        '<code>': '`',
        '</code>': '`',
        '<pre>': '``',
        '</pre>': '``',
        '<li>': ' - ',
        '<em>': '**',
        '</em>': '**',
        '&gt;': '>',
        '&lt;': '<',
        '<h2 id="part2">--- Part Two ---</h2>': '\n## Task 2',
        '<h2>---': '#',
        '---</h2>': '\n\n## Task 1\n',
        '```': '\n```\n'
    }

    for find, replace in replace_actions.items():
        description = description.replace(find, replace)

    description = description.replace('\n\n', '\n').strip()
    title = description.split("\n")[0].split(":")[1].strip()

    return title, description

def fetch_input(year, day):
    print("Fetching input")
    return fetch_day(year, day, '/input')

def generate_script(day, title):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('day.stencil')

    return template.render(
        day=day,
        title=title
    )

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Usage: ./gen_day.py <year> <day>")

    year = sys.argv[1]
    day = sys.argv[2]

    print("Generating %s day %s" % (year, day))
    print("")
    if not os.path.exists(year):
        os.makedirs(year)

    description_raw = fetch_description(year, day)
    title, description = parse_description(description_raw)
    write_file(year, "day%s.md" % day, description)

    print("")
    print("")
    if len(sys.argv) > 3 and sys.argv[3] == 'update':
        exit()

    input = fetch_input(year, day)
    write_file(year, "day%s-input.txt" % day, input)


    print("")
    print("")

    if not os.path.isfile("./%s/%s" % (year, "day%s.py" % day)):
        print("Generating day%s.py" % (day))
        script = generate_script(day, title)
        write_file(year, "day%s.py" % day, script)

    year_init_file = "./%s/__init__.py" % year
    year_init_data = open(year_init_file).read().splitlines()
    day_import_line = "from .day%s import Day%s" % (day, day)
    if day_import_line not in year_init_data:
        print("Updating %s __init__.py" % (year))
        year_init_data.append(day_import_line)
        with open("./%s/__init__.py" % year, "w+") as file:
            file.write("\n".join(sorted(year_init_data)))
