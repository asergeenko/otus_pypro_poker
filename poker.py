# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.

# https://en.wikipedia.org/wiki/List_of_poker_hands
# -----------------

import itertools

RANKS = '23456789TJQKA'

# Масти для джокеров
SUITS = {'B':'CS', 'R':'HD'}

NUM_RANKS = {rank:num for num,rank in enumerate(RANKS)}


def wild_hands(hand):
    '''Возвращает генератор комбинаций из 7 карт с заменой джокеров на все комбинации карт, которых еще нет в "руке"'''

    # "Рука" без джокеров
    no_jockers_hand = [h for h in hand if not h.startswith('?')]

    # Джокеров нет - возвращаем список с исходной "рукой"
    if no_jockers_hand == hand:
        return [hand]

    j_group = [joker for k,v in itertools.groupby(hand, lambda card: card[0]) for joker in v if k=='?']
    jokers = []

    for j in j_group:
        jokers.append([''.join(card) for card in itertools.product(RANKS,SUITS[j[1]])
                       if ''.join(card) not in no_jockers_hand])

    # Два джокера в "руке"
    if len(j_group) == 2:
        return (no_jockers_hand + list(wildcard) for wildcard in itertools.product(jokers[0], jokers[1]))
    # Один джокер в "руке"
    else:
        return (no_jockers_hand + [wildcard] for wildcard in jokers[0])


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if kind(5, ranks):
        return (9, max(ranks))
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""

    return sorted([ NUM_RANKS[card[0]] for card in hand ], reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""

    # Группируем по мастям
    suit_groups = itertools.groupby(hand, lambda card:card[1])

    return next(suit_groups, True) and not next(suit_groups, False)



def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""

    return all(i - j == 1 for i, j in zip(ranks[:-1], ranks[1:]))



def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    for k, g in itertools.groupby(ranks):
        if len(list(g)) == n:
            return k

def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""

    pair_ranks = []

    for k, g in itertools.groupby(ranks):
        group_len = len(list(g))
        if group_len == 2:
            pair_ranks.append(k)
            if len(pair_ranks) == 2:
                return sorted(pair_ranks,reverse=True)

def best_5_of_7(hand,best_hand5,max_rank):
    for hand5 in itertools.combinations(hand, 5):
        rank = hand_rank(hand5)
        change_max = False  # является ли текущая рука лучшей
        # Получен более высокий ранг "руки"
        if rank[0] > max_rank[0]:
            change_max = True
        # Ранги "рук" одинаковы, проверяем ранги карт
        elif rank[0] == max_rank[0]:
            # Five of a kind / Straight flush / Straight
            if rank[0] in [4, 8, 9]:
                if rank[1] > max_rank[1]:
                    change_max = True

            # Four of a kind / Fullhouse
            elif rank[0] in [6, 7]:
                if rank[1] > max_rank[1] or (rank[1] == max_rank[1] and rank[2] > max_rank[2]):
                    change_max = True

            # Flush / High card
            elif rank[0] in [0, 5] and rank[1][0] > max_rank[1][0]:
                change_max = True

            # Three of a kind / Two pair /One pair
            elif rank[0] in [1, 2, 3]:
                if rank[1] > max_rank[1] or (rank[1] == max_rank[1] and rank[2][0] > max_rank[2][0]):
                    change_max = True

        if change_max:
            best_hand5 = hand5
            max_rank = rank

    return best_hand5,max_rank


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """

    best_hand5 = []
    max_rank = (-1, None)

    best_hand5, max_rank = best_5_of_7(hand, best_hand5, max_rank)
    return best_hand5

def best_wild_hand(hand):
    """best_hand но с джокерами"""

    best_hand5 = []
    max_rank = (-1, None)
    for hand7 in wild_hands(hand):
        best_hand5, max_rank = best_5_of_7(hand7, best_hand5, max_rank)
    return best_hand5


def test_best_hand():
    print ("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print ('OK')


def test_best_wild_hand():
    print ("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print ('OK')

if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
