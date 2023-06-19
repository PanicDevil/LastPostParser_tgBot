from bs4 import BeautifulSoup
import requests
import time

# first_parsing_data = []

# print(first_parsing_data)

def start_parse():
        try:
            with open('tg_chanels.txt', 'r', encoding='utf-8') as file:
                data = file.read()
                spliting = data.split(' ')
                parsing_data = []
                for i in spliting:
                    TG_link = 'https://t.me/s/' + i
                    req = requests.get(TG_link)
                    html_code = req.text
                    
                    #parse_starting
                    soup = BeautifulSoup(html_code, 'lxml')
                    find_class = soup.find_all('div', class_ = 'tgme_widget_message_wrap js-widget_message_wrap')
                    if find_class:
                        last_element = find_class[-1]
                        
                        parse_in_class_chan_name = last_element.find(class_ = 'tgme_widget_message_author accent_color').find('span')
                        parse_in_class_content = last_element.find(class_ = 'tgme_widget_message_text js-message_text')
                        parse_in_class_post_link = last_element.find(class_ = 'tgme_widget_message_footer compact js-message_footer').find('a')
                        url = parse_in_class_post_link.get('href')

                        # first_parsing_data.append('Телеграм канал: ' + parse_in_class_chan_name.text + '\n\nПослдений пост: ' + parse_in_class_content.text + '\nссылка на пост: ' + url)
                        parsing_data.append('Телеграм канал: ' + parse_in_class_chan_name.text + '\n\nПослдений пост: ' + parse_in_class_content.text + '\nссылка на пост: ' + url)
                    else:
                        print('Я не нашел такого канала')
                print(parsing_data[0])
                return parsing_data
        except Exception as e:
             print('Ой что то пошло не так, проверьте корректность введенных данных', e)
            