from compare_functions import get_text_keywords, compare_keywords, compare_freq

URL_0 = 'http://lib.ru/DYACHENKO/r_hk.txt'
URL_1 = 'http://fan.lib.ru/b/baumgertner_o/kk1.shtml'
    
def get_text_from_url(url):
    from requests import get
    from bs4 import BeautifulSoup
    a_text = BeautifulSoup(get(url).content, 'lxml').body.text
    
    return a_text

if __name__ == '__main__':
    text_0, text_1 = get_text_from_url(URL_0), get_text_from_url(URL_1)
    text_0_ = text_0[0:len(text_0)//2]

    kw_0, kw_0_, kw_1 = get_text_keywords(text_0), \
                        get_text_keywords(text_0_), \
                        get_text_keywords(text_1)
                        
    print("Текст и фрагмент текста:", compare_keywords(kw_0, kw_0_))
    print("Критерий χ2", compare_freq(kw_0, kw_0_))
    print("Текст и другой текст:", compare_keywords(kw_0, kw_1))
    print("Критерий χ2", compare_freq(kw_0, kw_1))
