from requests import get
from bs4 import BeautifulSoup
from compare_functions import get_text_keywords, compare_keywords, compare_freq

def parse_text_a():    
    MAIN_URL = 'https://potter-1.bib.bz/'
    a_text= ""
    a = BeautifulSoup(get(MAIN_URL).content, 'lxml').find('nav', {'id':'list'})('a')
    for URL in [ x['href'] for x in a ]:
         a_text += BeautifulSoup(get(URL).content, 'lxml').find('article').text

    return a_text

def parse_text_b():
    URL = 'https://knizhnik.org/dmitrij-emets/tanja-grotter-i-magicheskij-kontrabas/%s'
    a_text= ""
    for x in range(1,26):
        a_text += BeautifulSoup(get(URL % x).content, 'lxml').find('div', {'class':'read'}).text
    
    return a_text

if __name__ == "__main__":
    text_a = parse_text_a()
    text_b = parse_text_b()
    
    kw_a, kw_b = get_text_keywords(text_a), get_text_keywords(text_b)

    print("Тексты похожи как:", compare_keywords(kw_a, kw_b))
    print("Критерий χ2", compare_freq(kw_a, kw_b))