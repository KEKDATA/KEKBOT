# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:08:28 2017

@author: andrew
"""
# import 
#import itertools

def getNumType(strNum):
    """
    Возвращает массив из 3х булевских элементов:
        метку корректности номера (True - корректный номер,
        тип номера(True - ИНН, False - ОГРН), 
        подтип номера (True - Юр. лицо, False - Физ. лицо)
    """
    if len(strNum) in (10,12):
        n = [int(i) for i in strNum]
        if len(strNum) == 10:
            indWeights = (2, 4, 10, 3, 5, 9, 4, 6, 8)
            n9 = (((sum(indWeights[i] * n[i] for i in range(len(strNum)-1))) % 11) % 10)
            if n9 == n[9]:
                return 'ИНН Юр. лица' #[True,True,True]
            else:
                raise ValueError('ИНН Юр. лица некорректен')
#                return [False,True,True]
        elif len(strNum) == 12:
            entWeights1 = (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
            entWeights2 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
            n10 = (((sum(entWeights1[i] * n[i] for i in range(len(strNum)-2))) % 11) % 10)
            n11 = (((sum(entWeights2[i] * n[i] for i in range(len(strNum)-1))) % 11) % 10)
            if (n10 == n[10]) & (n11 == n[11]):
                return 'ИНН Физ. лица' #[True,True,False]
            else:
                raise ValueError('ИНН Физ. лица некорректен')
#                return [False,True,False]
    elif len(strNum) in (13,15):
        if ((int(strNum[:-1]) % (len(strNum)-2)) % 10) == int(strNum[-1]):
            if len(strNum) == 13:
                return [True,False,True]
            else:
                return [True,False,False]
        else:
            if len(strNum) == 13:
                raise ValueError('ОГРН Юр. лица некорректен')
            else:
                raise ValueError('ОГРН Физ. лица некорректен')
            corr = False
            
            
        if len(strNum) == 13:
            return [corr,False,True]
        else:
            return [corr,False,False]
    else:
        return []

def getNameType(strName):
    """
    Ищет паттерны в именах. 
    Возвращает бинарную метку типа имени (Юр. Лицо [True], Физ. Лицо [False])
    """
    strName = strName.upper().strip()
    entityAttrib = ('ИП','ПАО','ООО','ЗАО','ОАО','АО',"'",'"', 'ОБЩЕСТВО',
                    'ПРЕДПРИНИМАТЕЛЬ')
    if any(substring in strName for substring in entityAttrib):
        return True
    else:
        return False
    
def getType(string):
    """
    Преобразует сообщение в список.
    Элементы списка - трехэлеменые массивы, состоящие из:
        
    Возвращает бинарную метку типа имени (Юр. Лицо [True], Физ. Лицо [False])
    """
    # Массив кортежей (ключ: значение функции)
    values = []
    # Первоначальая строка
    origString = string
    for s in string.split():
        if s.isdigit():
            answer = getNumType(s)
            # Проверяем массив на пустоту
            if answer:
                # Записываем в массив исходную строку и результат функции
                values.append([True, s, answer])
                # Удаляем из исходной строки распознанный номер
                origString = origString.replace(s, '')
    values.append([False, origString, getNameType(origString)])
    return values

values = []
for i in range(3):
    values.append([i,[str(i),str(i)]])
print(values)

getNumType('7706267111')
getType("'Прекрасное в далёком' 7706267110")
string = "ООО 'Прекрасное в далёком' 7706267111"
#strName = "'Прекрасное в далёком'"
getNameType("'Прекрасное в далёком'")
getNameType('Ольга Васильевна')

answer=[1,2,3]
if answer:
    print("TRUE")
else:
    print("FALSE")
strName = "7706267111"
getNumType('7706267111')
len(strName)
