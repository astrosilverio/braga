# Grammar rules

# password
# oops
# action phrase
# noun phrase, action phrase

import six
from collections import OrderedDict


# CC  coordinating conjunction
# CD  cardinal digit
# DT  determiner
# EX  existential there (like: "there is" ... think of it like "there exists")
# FW  foreign word
# IN  preposition/subordinating conjunction
# JJ  adjective   'big'
# JJR adjective, comparative  'bigger'
# JJS adjective, superlative  'biggest'
# LS  list marker 1)
# MD  modal   could, will
# NN  noun, singular 'desk'
# NNS noun plural 'desks'
# NNP proper noun, singular   'Harrison'
# NNPS    proper noun, plural 'Americans'
# PDT predeterminer   'all the kids'
# POS possessive ending   parent's
# PRP personal pronoun    I, he, she
# PRP$    possessive pronoun  my, his, hers
# RB  adverb  very, silently,
# RBR adverb, comparative better
# RBS adverb, superlative best
# RP  particle    give up
# TO  to  go 'to' the store.
# UH  interjection    errrrrrrrm
# VB  verb, base form take
# VBD verb, past tense    took
# VBG verb, gerund/present participle taking
# VBN verb, past participle   taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present  takes
# WDT wh-determiner   which
# WP  wh-pronoun  who, what
# WP$ possessive wh-pronoun   whose
# WRB wh-abverb   where, when

class Switch(object):

    def __init__(self, *args):
        self.patterns = list(args)
        self.allow_multiple = False
        self.is_optional = False

    def __len__(self):
        return max([len(pattern) if not isinstance(pattern, str) else len(pattern.split()) for pattern in self.patterns])

    def __call__(self, expr):
        """Evaluates an expression against a set of patterns, in order.
        """
        for pattern in self.patterns:
            if isinstance(pattern, str):
                match = expr if expr == pattern else None
            else:
                match = pattern(expr)
            if match:
                return match


class RootWordType(Switch):

    def __init__(self, name, *words):
        self.name = name
        self.patterns = list(args)

    def __str__(self):
        return self.name


class Phrase(object):

    def __init__(self, *components):
        if len(components) == 1:
            component = components[0]
            if isinstance(component, tuple):
                component = component[0]
            self.components = [component]
        else:
            self.components = list(components)
        self.allow_multiple = False
        self.is_optional = False

    def __len__(self):
        return len(self.components)

    def __call__(self, expr):
        best_match = []
        expr_pointer = 0
        for component in self.components:
            match = component(expr[expr_pointer])
            if match and component.allow_multiple:
                pass
            elif match:
                best_match.append(match)
                expr_pointer += 1
            else:
                probe_pointer = expr_pointer + 1
                while probe_pointer < len(self.components):
                    try:
                        match = component(expr[expr_pointer:probe_pointer])
                    except ValueError:
                        expr_pointer = probe_pointer
                        best_match.append(match)
                        break
                    else:
                        probe_pointer += 1
                else:
                    raise ValueError

        return best_match if best_match else None


def multi(phrase_or_word):
    phrase_or_word.allow_multiple = True


def opt(phrase_or_word):
    phrase_or_word.is_optional = True


valid_patterns = Switch(oops_phrase, action_phrase, noun_action_phrase)

oops_phrase = Phrase(oops_word, any)
oops_word = RootWordType('oops word', 'oops', 'nvm')

action_phrase = Phrase(multi(verb_phrase))
verb_phrase = Switch(again_word, password_phrase, imperative_command)

again_word = RootWordType('again_word', 'again')
password_phrase = Phrase(opt(password_word), any)
password_word = RootWordType('password', 'password')
imperative_command = Phrase(verb_word, grammar_line)

verb_word = RootWordType('verb', 'take', 'get', 'go')  # autogenerate from game commands
grammar_line = Switch(noun_phrase, preposition_word, number)
noun_phrase = Phrase(opt(multi(basic_noun_phrase, connective_word)), basic_noun_phrase)
preposition_word = RootWordType('preposition', 'from', 'between', 'in', 'out')
number = RootWordType('number', 'one', 'two', 'three', 'four', 'five')

basic_noun_phrase = Switch(descriptor_list, noun_list)
connective_word = Switch(and_word, but_word, not_word)
and_word = RootWordType('and word', 'and', 'also')
but_word = RootWordType('but word', 'but', 'except')
not_word = RootWordType('negation', 'not')

descriptor_list = Phrase(multi(descriptor))
noun_list = Phrase(multi(noun_word))
noun_word = Switch(name_word, me_word, pronoun_word)
name_word = RootWordType('game object name', 'wand', 'other player')  # autogenerate from game nouns
me_word = RootWordType('me word', 'me', 'I')
pronoun_word = RootWordType('pronoun', 'it', 'she', 'they', 'he', 'us', 'them', 'her', 'him')

descriptor = Switch(article_word, all_word, any_word, other_word, number, possessive)
article_word = RootWordType('article', 'a', 'an', 'the', 'some')
all_word = RootWordType('all word', 'all')
any_word = RootWordType('any word', 'any')
other_word = RootWordType('other word', 'other')
possessive = RootWordType('possessive', 'my', 'your', 'their', 'her', 'his', 'its')

noun_action_phrase = Phrase(noun_phrase, action_phrase)

Token = namedtuple('Token', ['pos', 'value'])
