import json

""" 
1) Which 3 user IDs have most followers?
"""
"""
3) Use the graph data to answer the following questions:
- Is the graph sparse or dense? Does the answer somehow determine how the solution
to questions 1 and 2 should be found?
- If the graph is dense, provide an example of a sparse graph (and vice versa).
"""
"""
4) Suppose that instead of Twitter following, the data represents money transfers. What
patterns would you look for to flag a high risk of money laundering? What other additional
information should be added to the graph to simplify money-laundering identification?
"""

def extract_numbers(string):
    """
    Returns USERID and FOLLOWERID as integers, from 
    a string of the form USERID\tFOLLOWERID\n

    Arguments:
        :string: The mentioned string
    """
    for k in range(len(string)):
        if string[k] == '\t':
            return int(string[:k]), int(string[k+1:-1])

# Initializing users set variables.
followed_users = set()
following_users = set()

# Initializing 'followers' and 'following' users dictionaries.
followers = dict()
following_dict = dict()

# Initializing users counters.
followed_user_count = 0
following_user_count = 0

# Setting how many lines from each file
how_many = 10000000

# Setting how many files
how_many_files = 1

names = ['twitter_rv.net.00','twitter_rv.net.01','twitter_rv.net.02','twitter_rv.net.03']

# Collecting data from the four files.
for nome_file in names[:how_many_files]:
    with open(nome_file, mode='r') as f:
        counter = 0
        while counter< how_many:
            first_line = f.readline()
            user, follower = extract_numbers(first_line)
            followed_users.add(user)
            # If not already present, this adds 'user' to the 'followed' set.
            new_followed_count = len(followed_users)
            if new_followed_count > followed_user_count:
                # This means 'user' was not in the set before.
                followers[user] = 1  # Initialize new key-value pair.
                followed_user_count = new_followed_count
            else:
                # If 'user' was already present, then the key-value pair was already created.
                followers[user] += 1  # Update key-value pair.

            following_users.add(follower)
            # If not already present, this adds 'follower' to the 'following' set.
            new_following_count = len(following_users)
            if new_following_count > following_user_count:
                # This means 'follower' was not in the set before.
                following_dict[follower] = {user}  # Initialize new key-value pair.
                following_user_count = new_following_count
            else:
                # If 'user' was already present, then the key-value pair was already created.
                following_dict[follower].add(user)  # Update key-value pair.
            counter += 1


# Printing some information.
print(f'The followers dictionary has a total of {len(followers)} keys.\n')
print(f'The following_dict has a total of {len(following_dict)} keys.\n')
print(f'There are {len(followed_users)} followed users.\n')
print(f'There are {len(following_users)} following users.\n')

# Initializing counting variable.
top = 3  # Change in case you want to extend the list.

# Initializing first IDs list.
first_IDs = []

# Initializing the variable for computing the highest number of followers.
# Since there are 10 million edges, a single user must have less than 10000001 followers.
max_number = how_many + 1

# Initializing the loop to find the first 'top' IDs. The loop stops when the first_IDs
# variable is filled as requested or when the followers set contains less than 'top' users.
while len(first_IDs) < top and followers:
    max_number = max([followers[user]
                     for user in followers if followers[user] < max_number])
    # Computes the highest number of followers for a single user.

    for user, followers_number in followers.items():
        # Looping through all the items of the dictionary and add all the followers
        # with max_number users to the first_IDs list.
        if followers_number == max_number and user not in first_IDs:
            first_IDs.append([user, followers[user]])

# Printing the findings.
print('The first users with the most IDs are the following:')
for k in range(len(first_IDs[:top])):
    print(
        f'The user in position {k+1} is {first_IDs[k][0]} with {first_IDs[k][1]} followers')

total = 0
for k in range(top):
    total += first_IDs[k][1]

print(f'\nAll together they have {total} followers\n')

"""
2) Identify the user following the highest number of accounts (user f).
"""

# Initializing the variable for computing the highest number of followed users.
max_following = max([len(value) for value in following_dict.values()])

# Initializing the user f node.
user_f = 0

# Looping through the following dictionary. Looking for matches with 'max_following'.
for user, followed in following_dict.items():
    if len(followed) == max_following:
        user_f = user
        break  # so.. if there are more, following the same amount, I only consider the
        # first match. I will check later if there are more.

# Printing the findings.
print(f'The user f is {user_f}\n')
print(f'He follows {max_following} profiles.\n')

# Checking uniqueness of user_f

# Deleting user_f from the following dictionary keys, while keeping track of its value.
temp_data_user_f = following_dict.pop(user_f)

# Repeat the process.
max_following_2 = max([len(value) for value in following_dict.values()])
user_f_2 = 0
for user, followed in following_dict.items():
    if len(followed) == max_following_2:
        user_f_2 = user
        break
print(f'The second user f is {user_f_2}\n')
print(f'He follows {max_following_2} profiles.\n')
if max_following > max_following_2:
    print('Therefore the user_f is unique.\n')
else:
    print('Therefore the user_f is not unique.\n')

following_dict[user_f] = temp_data_user_f  # Reinsert data about user_f.

"""
 Calculate:
- the shortest path between f and any other user u in the graph (i.e. the lowest number
of edges between f and u, where edge u1->u2 represents u1 following u2).
"""

# Initializing the 'following' tree. At the top there is user_f. The second layer,
# i.e. tree[1], there will be the users he follows. The third layer will contain
# the users followed by the users in layer 2, with the exception of the users that
# are already in the tree. Therefore each layer will contain only new users.
tree = [{user_f}]


def build_new_floor(most_recent_floor, old_users):
    """ 
    Builds the new floor of the tree.

    Arguments:
        :most_recent_floor: A set with the users of tree[-1]
        :old_users: A set with all the users of tree.

    """
    global following_dict
    global tree
    # Initializing the new floor.
    new_floor = set()
    # Looping through the users, in the last floor, who follow other users
    for user in most_recent_floor & following_dict.keys():
        new_floor.update(following_dict[user])
        new_floor = new_floor - old_users
        # second option 
        # for followed_user in following_dict[user]:
        #     # If the followed_user is already in the tree we exclude him, avoiding
        #     # unnecessary computations (we are looking for the shortest path).
        #     if followed_user not in old_users:
        #         new_floor.add(followed_user)
    tree.append(new_floor)


def check_existing_tree(u):
    """
    If the user u is already in the tree, returns True and the layer in which he lies.
    Otherwise returns False and -1.

    This way, while looking for the most distant nodes, we take advantage of the tree
    layers that have already been built while computing the distance of previous users.

    Arguments:
        :u: The user to be searched.
    """
    global tree
    for k in range(len(tree)):
        if u in tree[k]:
            return True, k
    return False, -1

# This approach is better if we want to compute only one distance.
# Otherwise, when we need all the distances, the approach in Twitter_graph_better_paths.py 
# is better. The difference seems small, but that's only because "followers" has very few 
# elements.
def shortest_path(u):
    """
    Returns the length of the shortest path starting from user_f and ending in u.

    It uses a while loop structure rather than a recursive one, because the latter
    strategy exceeds the recursion limit.

    Arguments:
        :u: The user whose distance is to be computed.
    """
    global tree
    global followers
    
    # Checking the preexisting layers of the tree
    already_found, dist = check_existing_tree(u)
    if already_found:
        return dist

    # Since u is not already in the tree, we build a new floor.
    most_recent_floor = tree[-1]
    distance = len(tree) - 1

    # Looping through the floors of 'tree' while building them, until u is in one of them.
    while u not in most_recent_floor:
        if len(most_recent_floor) == 0:
            # i.e. no other users are reachable from this tree.
            # In particular, u is not reachable.
            return -1
        else:
            # If the newly built floor is not empty, but u is yet to be found,
            # we build a new floor.

            # updating the old users variable, containing all the users already in the tree.
            old_users = {user for floor in tree for user in floor}
            build_new_floor(most_recent_floor, old_users)
            # After building the new floor, we update the most recent floor variable
            most_recent_floor = tree[-1]
            distance += 1
    return distance


# Initializing the paths dictionary, which provides the distance from user_f to any user.
# If the user is not reachable, the distance is set to -1.
paths_dict = dict()

""" Report the length of 3 longest paths and the ending nodes."""

# Initializing the set of all the users
users = followed_users | following_users

# Initializing the variable keeping track of how many users are reachable from f.
reachable = 0

# Looping through the users to build the paths dictionary.
for user in followed_users:
    temp_path = shortest_path(user)
    paths_dict[user] = temp_path

# Initializing the variable holding the most distant nodes, with respective distances.
first_3_paths = []

# Initializing the variable for holding the highest distance.
# Again, since there are 10 mil. edges, an upper bound is given by 10000001;
# even though, as we will see, the actual highest distance is much smaller.
max_path = how_many + 1

# Initializing the iterable of the lengths.
paths_lengths = paths_dict.values()

# Looping until the first 3 paths variable is filled.
while len(first_3_paths) < 3:
    # Computing the maximal distance.
    max_path = max([length for length in paths_lengths if length < max_path])
    # Looping through paths dictionary while looking for matches.
    for user in paths_dict:
        distance = paths_dict[user]
        # If the distance matches the maximum, append the user to the list.
        if distance == max_path and (user, distance) not in first_3_paths:
            first_3_paths.append((user, distance))

# Printing the findings.
print(f'\nThe first three (more if the third and some others coincide) paths are the following:')
for couple in first_3_paths:
    print(f'User: {couple[0]}, \t Distance: {couple[1]}')

"""
- Optional: The longest cycle, e.g. path starting and ending at f but visiting other users
at most once (report the length, or if the length is less or equal than 20 edges, report
the nod IDs).
"""

print(f'\nThe user f has no follower: {user_f not in followers}')
# the next "print" depends on how many lines we consider.
print(f'Since the user_f has no follower, there are no paths leading to him.')
print('In particular there is no cycle starting and ending at user_f.')