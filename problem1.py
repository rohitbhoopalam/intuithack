def read_screen_user_file():
    _screen_user_count = {}
    _user_set = set()

    f = open("screen_to_users_100000.tsv", "r")
    i = 0
    for screen_user in f:
        screen, user = screen_user.split()
        _user_set.add(int(user))
        try:
            _screen_user_count[int(screen)] += 1
        except KeyError:
            _screen_user_count[int(screen)] = 1
        i += 1
        print i
    
    return _screen_user_count, _user_set

(screen_user_count, user_set) = read_screen_user_file() 

total_number_of_users = len(user_set) 
