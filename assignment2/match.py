from os import PRIO_PGRP
import numpy as np
from typing import List, Tuple

from numpy.core.fromnumeric import mean

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    import random
    population_size = len(gender_id)
    proposers = random.sample(range(population_size), round(population_size/2))
    receivers = list(set(range(population_size)) - set(proposers))

    propscrDict = {}

    def gender_compatibility(proposer_gender, proposer_pref, \
                             receiver_gender, receiver_pref):
        d = {
            'Female': -1,
            'Women': -1,
            'Nonbinary': 0,
            'Bisexual': 0,
            'Male': 1,
            'Men': 1
        }
        if proposer_pref != 'Bisexual' and receiver_pref != 'Bisexual':
            print('hetero', proposer_gender, proposer_pref, \
                             receiver_gender, receiver_pref)
            if d[proposer_pref] != d[receiver_gender] or d[receiver_pref] != d[proposer_gender]:
                return 0
            else:
                return 1

        elif proposer_pref == 'Bisexual':
            print('proposer is bi ', proposer_gender, proposer_pref, \
                             receiver_gender, receiver_pref)
            if d[receiver_pref] == 0:
                return 1
            elif d[receiver_pref] != d[proposer_gender]:
                return 0
            else:
                return 1

        elif receiver_pref == 'Bisexual':
            print('receiver is bi ', proposer_gender, proposer_pref, \
                             receiver_gender, receiver_pref)
            if d[proposer_pref] == 0:
                return 1
            elif d[proposer_pref] != d[receiver_gender]:
                return 0
            else:
                return 1

    scoreDict = {}
    for proposer in proposers:
        scoreDict[proposer] = []

        for receiver in receivers:
            score = scores[proposer][receiver]
            # I deleted this check because in our original sample, there are 
            # 3 nonbinary people, but only one person who is bisexual, and the 
            # others' preferences are binary (either men or women), so no
            # matter what random sample is chosen logically two of the 
            # nonbinary people will never be accepted as a partner...
            # print(gender_compatibility(gender_id[proposer], \
            #                         gender_pref[proposer], \
            #                         gender_id[receiver], \
            #                         gender_pref[receiver]))
            # if gender_compatibility(gender_id[proposer], \
            #                         gender_pref[proposer], \
            #                         gender_id[receiver], \
            #                         gender_pref[receiver]) == 1:
                # if score > 0:
                #     scoreDict[proposer].append((receiver, score))
            if score > 0:
                scoreDict[proposer].append((receiver, score))

        scoreDict[proposer].sort(key=lambda x: x[1], reverse=True)
    
        # print("Initial score list for ", proposer, " is: ", scoreDict[proposer])
    import copy

    
    while len(proposers) != 0:
        this_round_proposers = copy.deepcopy(proposers)
        # print("The proposers are: ", this_round_proposers)
        for proposer in proposers:
            # print("proposer: ", proposer)
            # print("This round's score list for ", proposer, " is: ", scoreDict[proposer])
            # for proposer in scoreDict:
            if len(scoreDict[proposer]) == 0:
                continue
            highest_receiver = scoreDict[proposer][0][0]
            # print('highest_receiver: ', highest_receiver)
            highest_score = scoreDict[proposer][0][1]
            # print('highest_score: ', highest_score)
            if highest_receiver not in propscrDict.keys():
                propscrDict[highest_receiver] = (proposer, highest_score)
                # print("Added proposer, receiver, score: ", (proposer, highest_receiver, highest_score))
                this_round_proposers.remove(proposer)
            else:
                # If the receiver prefers new proposer over current partner
                if highest_score > propscrDict[highest_receiver][1]:
                    curr_partner = propscrDict[highest_receiver][0]
                    propscrDict[highest_receiver] = (proposer, highest_score)
                    # print('Freed old proposer: ', curr_partner)
                    # print("Added proposer, receiver, score: ", (proposer, highest_receiver, highest_score))
                    this_round_proposers.append(curr_partner)
                    this_round_proposers.remove(proposer)
                    # print("New proposers: ", this_round_proposers)
                else:
                    scoreDict[proposer].remove((highest_receiver, highest_score))
                    # print(highest_receiver, " rejected ", proposer)

        # print("Final propscrDict is: ", propscrDict)
        # print('len(proposers): ', len(this_round_proposers), " and the free proposers are: ", this_round_proposers)
        proposers = this_round_proposers
        # print("Proposers after this round: ", proposers)
        # print("COMPLETED A ROUND")
        if 0 == len(this_round_proposers):
            break

    # print(propscrDict)
    matches = []
    for item in propscrDict.items():
        matches.append((item[0], item[1][0]))
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
    print(gs_matches)
