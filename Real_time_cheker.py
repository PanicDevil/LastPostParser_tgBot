import time

def real_t_chek():
    # while True:
    from parse_func import start_parse
    pre_parse = start_parse()
    time.sleep(15)
    parse = start_parse()
    get_uniq_post = list(set(parse) - set(pre_parse))
    if get_uniq_post == []:
        print('not found')
    else:
        print('last post' + str(get_uniq_post))

real_t_chek()