#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    grad_year_weight = 0.2
    responses_weight = 0.8

    # If a user is not in the other's preferences, the score is 0
    if not (user1.gender in user2.preferences): 
        return 0

    def grad_year_compatibility(user1, user2):
        # Each gap in grad_years is mapped to a score out of 100
        dictionary = {
            0:100,
            1:80,
            2:65,
            3:30
        }
        return dictionary[abs(user1.grad_year - user2.grad_year)]

    def responses_compatibility(user1, user2):
        # Take the sum of absolute differences between responses and subtract 
        # that sum from the possible maximum. Then, 
        # A response could be {0,...5}
        max_difference = 5
        responses_num = len(user1.responses)

        max_score = max_difference * responses_num
        scale = 100 / max_score

        compatibility_score = \
            max_score - (sum(abs(user1.responses[i] - user2.responses[i]) \
                                 for i in range(len(user1.responses))))
        return compatibility_score * scale

    final_score = grad_year_compatibility(user1, user2) * grad_year_weight + \
                  responses_compatibility(user1, user2) * responses_weight

    return round(final_score, 1)


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
