import re
from itertools import starmap
from operator import mul

def innLe(strINN):
    """
    Валидатор ИНН юр.лица
    """
    if len(strINN) == 10 and re.search(r"\D", strINN) is None:
        n = tuple(map(int, strINN))
        indWeights = (2, 4, 10, 3, 5, 9, 4, 6, 8)
        n9 = sum(starmap(mul, zip(indWeights, n))) % 11 % 10
        return n9 == n[9]
    return False
         
def innFl(strINN):   
    """
    Валидатор ИНН физ.лица
    """         
    if len(strINN) == 12 and re.search(r"\D", strINN) is None:
        n = tuple(map(int, strINN))
        entWeights1 = (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        entWeights2 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        n10 = sum(starmap(mul, zip(entWeights1, n))) % 11 % 10
        n11 = sum(starmap(mul, zip(entWeights2, n))) % 11 % 10
        return n10 == n[10] and n11 == n[11]
    return False

def ogrn(strOGRN):
    """
    Валидатор ОГРН
    """
    if len(strOGRN) in (13,15) and re.search(r"\D", strOGRN) is None:
        if int(strOGRN[:-1]) % (len(strOGRN)-2) % 10 == int(strOGRN[-1]):
            return True
    return False

# Тесты
if __name__ == '__main__':
    if innLe('7706267111'):
        print('ИНН ЮЛ 7706267111 корректен')
    if not(innLe('7706267110')):
        print('ИНН ЮЛ 7706267110 некорректен')
        
    if innFl('526317984689'):
        print('ИНН ФЛ 526317984689 корректен')
    if not(innFl('526317984688')):
        print('ИНН ФЛ 526317984688 некорректен')
        
    if ogrn('1027739067729'):
        print("ОГРН 1027739067729 корректен")
    if not(ogrn('1027739067728')):
        print("ОГРН 1027739067728 некорректен")