import argparse
from similar_domains import Extractor


class DomainScannerManager:
    def __init__(self):
        self.scanner_parser = argparse.ArgumentParser('Script is defining domains that are similar to given')

    def add_arguments(self):
        self.scanner_parser.add_argument('-k', '--key_words', required=True, nargs='*',
                                         help='Input key word(words) which domain you want to chek.\n'
                                              'It can be singe word, so script will check him.\n'
                                              'Or you may print some word separated with spaces and script will'
                                              'check all of them.')
        return self.scanner_parser.parse_args()

    def run(self):
        args = self.add_arguments()
        print('Running ...')
        extractor = Extractor(key_words=args.key_words)
        extractor.run()


manager = DomainScannerManager()
manager.run()

#  input example
#  $ python3 console_domain_scanner.py -k <key_word>
