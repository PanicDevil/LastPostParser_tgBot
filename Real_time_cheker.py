import time

def real_t_chek():
    from parse_func import start_parse
    pre_parse = start_parse()
    time.sleep(15)
    parse = start_parse()
    get_uniq_post = list(set(parse) - set(pre_parse))
    if get_uniq_post == []:
        print('ищу новые посты')
    else:
        # print('last post' + str(get_uniq_post))
        return str(get_uniq_post)
