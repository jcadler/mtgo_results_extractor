#!/usr/bin/python3
import argparse

from collections import defaultdict
from html.parser import HTMLParser

COLORS = ['White', 'Blue', 'Black', 'Red', 'Green', 'Colorless']

class html_deck_parser(HTMLParser):

    def __init__(self):
        self.get_name = False
        self.get_category = False
        self.get_card_count = False
        self.get_card_name = False
        self.end_of_list = False
        self.name = 'NOTANAME'
        self.decklist = ''
        self.card_count = 0
        self.decks = []
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'h4':
            self.get_name = True
        elif tag == 'h5':
            self.get_category = True
        elif tag == 'span':
            for t in attrs:
                if t[0] == 'class':
                    if t[1] == 'card-count':
                        self.get_card_count = True
                    elif t[1] == 'card-name':
                        self.get_card_name = True
        

    def handle_data(self, data):
        if self.get_name:
            self.decklist += data + '\n'
            self.get_name = False
            self.end_of_list = False
        elif self.end_of_list:
            self.get_category = False
            self.get_card_count = False
            self.get_card_name = False
            return
        elif self.get_category and 'Sideboard' in data:
            self.decklist += 'Sideboard\n'
        elif self.get_category and any(x in data for x in COLORS):
            self.decks.append(self.decklist)
            
            self.decklist = ''
            self.end_of_list = True
        elif self.get_card_count:
            self.card_count = data
            self.get_card_count = False
        elif self.get_card_name:
            self.decklist += '{} {}\n'.format(self.card_count, data)
            self.get_card_name = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse mtgo results page into deck lists.')
    parser.add_argument('results_page')
    args = parser.parse_args()
    results_txt = ''
    with open(args.results_page, 'r') as results_file:
        results_txt = results_file.read()
    deck_parser = html_deck_parser()
    deck_parser.feed(results_txt)
    archetype_summary = defaultdict(int)
    for d in deck_parser.decks:
        print(d)
        arch = input('What archetype is this?: ')
        archetype_summary[arch] += 1
    arch_sort = sorted(archetype_summary.items(), key=lambda a: a[1], reverse=True)
    for a in arch_sort:
        print(a[0], a[1])
