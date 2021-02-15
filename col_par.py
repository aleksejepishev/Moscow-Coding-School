from bs4 import BeautifulSoup
import requests

url = 'https://history.columbia.edu/graduate/doctoral-students/'

text = requests.get(url).text
soup = BeautifulSoup(text, 'html5lib')

tags = soup('a')
lst_href = []
for tag in tags:
    lst_href.append(tag.get('href'))

lst_href = lst_href[:-1]
new_lst = []
for href in lst_href:
    if type(href) == 'NoneType':
        continue
    if href.startswith('https://history.columbia.edu/faculty/'):
        new_lst.append(href)


list_of_students = []
for url in new_lst:
    url2 = url
    text2 = requests.get(url2).text
    soup2 = BeautifulSoup(text2, 'html5lib')

    title = soup2.title.text
    try:
        print('Crawling in progress')
        main = soup2.find('div', 'expert-info-text').text #cmed_content_box, expert-info-text
        print('Crawling success')
    except:
        print('Something went wrong')
        main = 'No Bio'
        continue
    bio = str(main)
    list_of_students.append((title, bio))

with open('doctora_students.txt', 'w', encoding="utf-8") as ds:
    for name in list_of_students:
        ds.write(name[0])
        ds.write('\n')
        ds.write(name[1])
        ds.write('\n')
