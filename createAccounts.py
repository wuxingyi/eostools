import string
import sys
import time
import os

def make_new_words(start_word):
    """create new words from given start word and returns new words"""
    new_words = []
    for i, letter in enumerate(start_word):
        word_as_list = list(start_word)
        for char in string.ascii_lowercase:
            word_as_list[i] = char
            new_words.append("".join(word_as_list))

    return new_words

def createAccounts(startword):
    s = make_new_words(startword)
    print len(s)
    # in my system keosd is runing at 8889 port
    os.system('cleos --wallet-url=http://127.0.0.1:8889 wallet unlock --password=PW5JDUhcbjYFmeW6yYAgpVRZZBH3jRcPr7VWAmcj5Puqaapzutjd8')
    print s
    for i in s:
        r = os.system('cleos --wallet-url=http://127.0.0.1:8889 create account eosio %s EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV' % i)
        if r is not 0:
            time.sleep(0.1)
            os.system('cleos --wallet-url=http://127.0.0.1:8889 create account eosio %s EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV' % i)


if __name__ == "__main__":
    createAccounts(sys.argv[1])
