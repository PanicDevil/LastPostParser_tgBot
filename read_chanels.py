def read_chanels_func():
    with open('tg_chanels.txt', 'r') as read_file:
        file_data = read_file.read()
        split_data = file_data.split()
        chanels_list = []
        for i in split_data:
            result = '@' + i
            chanels_list.append(result)
        only_chanels = ' '.join(chanels_list)
        return str(only_chanels)