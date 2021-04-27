import socket
import threading
import string

DOMAINS = ['com', 'ru', 'net', 'org', 'info', 'cn', 'es',
           'top', 'au', 'pl', 'it', 'uk', 'tk', 'ml', 'ga', 'cf', 'us', 'xyz', 'top', 'site', 'win', 'bid']
PORT = 53
SYMBOLS_TO_APPEND = [symb for symb in string.digits + string.ascii_lowercase]


def get_homoglyphs(word):
    homoglyphs = set()
    if word.find('i') != -1:
        homoglyphs.add(word.replace('i', '1'))
        homoglyphs.add(word.replace('i', 'l'))
    if word.find('l') != -1:
        homoglyphs.add(word.replace('l', '1'))
        homoglyphs.add(word.replace('l', 'i'))
    if word.find('1') != -1:
        homoglyphs.add(word.replace('1', 'l'))
        homoglyphs.add(word.replace('1', 'i'))
    if word.find('0') != -1:
        homoglyphs.add(word.replace('0', 'o'))
    if word.find('o') != -1:
        homoglyphs.add(word.replace('o', '0'))
    return homoglyphs


class DomainsChecker(threading.Thread):

    def __init__(self, hosts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hosts = hosts
        self.results = []

    def run(self):
        for host in self.hosts:
            for dom in DOMAINS:
                complete_host = host + '.' + dom
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.150)

                try:
                    ip = socket.gethostbyname(complete_host)
                    result = f'{complete_host} {ip}'
                    self.results.append(result)
                except socket.gaierror:
                    pass
                sock.close()


class Extractor:

    def __init__(self, key_words):
        self.key_words = key_words
        self.extended_words_dict = {}
        self.homoglyphs = set()

    def format_key_words(self):

        for word in self.key_words:
            if word not in self.extended_words_dict:
                self.extended_words_dict['key_word'] = []
                self.extended_words_dict['append_symbol'] = []
                self.extended_words_dict['add_homoglyph'] = []
                self.extended_words_dict['add_point'] = []
                self.extended_words_dict['del_symbol'] = []
            word_by_char = [i.lower() for i in word]

            for symb in SYMBOLS_TO_APPEND:
                word_by_char.append(symb)
                self.extended_words_dict['append_symbol'].append(''.join(word_by_char))
                word_by_char.pop()

            homoglyphs = get_homoglyphs(word)
            for hg in homoglyphs:
                self.homoglyphs = self.homoglyphs.union(get_homoglyphs(hg))
            if word in self.homoglyphs:
                self.homoglyphs.remove(word)
            for glyph in list(self.homoglyphs):
                self.extended_words_dict['add_homoglyph'].append(glyph)

            for s in range(1, len(word_by_char)):
                if not word_by_char[s].isalpha() or not word_by_char[s - 1].isalpha():
                    continue
                word_by_char.insert(s, '.')
                self.extended_words_dict['add_point'].append(''.join(word_by_char))
                word_by_char.pop(s)

            for s in range(len(word_by_char)):
                symb = word_by_char[s]
                word_by_char.pop(s)
                self.extended_words_dict['del_symbol'].append(''.join(word_by_char))
                word_by_char.insert(s, symb)

            self.extended_words_dict['key_word'].append(word)

    def scan(self):

        scanners = [DomainsChecker(hosts=self.extended_words_dict[key])
                    for key, hosts in self.extended_words_dict.items()]
        for scanner in scanners:
            scanner.start()
        for scanner in scanners:
            scanner.join()
        for scanner in scanners:
            if scanner.results:
                for result in scanner.results:
                    print(result)
        if all(len(scanner.results) == 0 for scanner in scanners):
            print('There is no domains')

    def run(self):
        self.format_key_words()
        self.scan()
