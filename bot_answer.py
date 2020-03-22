
    
import itertools
from SPARQLWrapper import SPARQLWrapper, JSON

import queries
import bot_answer_templates as templates


class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


def _responseToDict(responseJSON):
    d = HashableDict()
    for key, value in responseJSON.items():
        d.update({key: value["value"]})
    return d

def _listElem(num, text):
    f, *o = text.split("\n")    
    f = (str(num) + ".").ljust(4, " ") + f
    o = [" "*4 + i for i in o]
    return "\n".join([f, *o])  + "\n"



infoStub = "-Нет данных-"
listStub = "-Список пуст-"


#==============================================================================
# Далее идет набор функцие для получения информации о ЮЛ
#==============================================================================

def getAnswerAboutLeByRequisit(sparql, requisit, requisitName):
    """
    Формирует ответ с информацией о ЮЛ по реквизиту.
    Args:
        sparql: ну это понятно
        requisit: значение реквизита - str
        requisitName: имя реквизита(name, ogrn, inn) - str
    Return:
        Строка содержащая ответ по запросу.
    """
    if requisitName == "name":
        results = getLeInfoByFullName(sparql, requisit)
        if results == {}:
            results = getLeInfoByShortName(sparql, requisit)
    elif requisitName == "ogrn":
        results = getLeInfoByOgrn(sparql, requisit)
    elif requisitName == "inn":
        results = getLeInfoByInn(sparql, requisit)
    else:
        raise AttributeError("Invalid requisit value. Requisit value must be in range (name, inn, ogrn)")

    fes = None
    powpoas = None

    if results.get("le") is not None:
        fes = getFeListByLe(sparql, results.get("le"))
        if fes != []:
            fes = [templates.feInListInfo.format(
                    name = fe.get("name", infoStub),
                    inn = fe.get("inn", infoStub),
                    sharePerc = fe.get("sharePerc", infoStub),
                    shareNominal = fe.get("sharePerc", infoStub)
                    ) for fe in fes]
            fes = "\n".join(itertools.starmap(_listElem, enumerate(fes, start=1)))
        
        powpoas = getPawpoaListByLe(sparql, results.get("le"))
        if powpoas != []:
            powpoas = [templates.pawpoaInListInfo.format(
                    name = powpoa.get("ppa_name", infoStub),
                    inn = powpoa.get("inn_ppa", infoStub),
                    job = powpoa.get("job_title", infoStub),
                    phone = powpoa.get("phone_number", infoStub)
                    ) for powpoa in powpoas]

            powpoas = " ".join(itertools.starmap(_listElem, enumerate(powpoas, start=1)))
    answer = templates.leMainInfo.format(
            fullName = results.get("fullName", infoStub),
            shortName = results.get("shortName", infoStub),
            inn = results.get("inn", infoStub),
            ogrn = results.get("ogrn", infoStub),
            grn = results.get("grn", infoStub),
            kpp = results.get("kpp", infoStub),
            dr = results.get("dr", infoStub),
            addr = results.get("addr", infoStub),
            fes = fes if fes != [] and fes is not None else listStub,
            powpoas = powpoas if powpoas != [] and powpoas is not None else listStub
            )
    return answer


def getLeInfoByFullName(sparql, fullName):
    """
    Отправляет sparql запрос для получения инфы о ЮЛ.
    ?fullName -> ?fullName ?shortName ?grn ?ogrn ?kpp ?dr ?addr ?le
    fullName - полное название
    shortName - сокращенное название
    grn -ГРН
    ogrn - ОГРН
    kpp - КПП
    dr - дата региствации
    addr - адрес
    le - экземпляр класса Legal Entity
    
    Args:
        sparql: ну это понятно
        fullName: полное название фирмы - str
    Return:
        dict с ключами fullName, shortName, grn, ogrn, kpp, dr, addr, le
    """
    sparql.setQuery(queries.getLEInfoByFullName.format(full_name=fullName))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results["results"]["bindings"] != []:
        return _responseToDict(results["results"]["bindings"][0])
    else:
        return _responseToDict(dict())

def getLeInfoByShortName(sparql, shortName):
    """
    Отправляет sparql запрос для получения инфы о ЮЛ.
    ?shortName -> ?fullName ?shortName ?grn ?ogrn ?kpp ?dr ?addr ?le
    fullName - полное название
    shortName - сокращенное название
    grn -ГРН
    ogrn - ОГРН
    kpp - КПП
    dr - дата региствации
    addr - адрес
    le - экземпляр класса Legal Entity
    
    Args:
        sparql: ну это понятно
        fullName: полное название фирмы - str
    Return:
        dict с ключами fullName, shortName, grn, ogrn, kpp, dr, addr, le
    """
    sparql.setQuery(queries.getLEInfoByShortName.format(short_name=shortName))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results["results"]["bindings"] == []:
        return dict()
    else:
        return _responseToDict(results["results"]["bindings"][0])


def getLeInfoByOgrn(sparql, ogrn):
    """
    Отправляет sparql запрос для получения инфы о ЮЛ.
    ?ogrn -> ?fullName ?shortName ?grn ?ogrn ?kpp ?dr ?addr ?le
    fullName - полное название
    shortName - сокращенное название
    grn -ГРН
    ogrn - ОГРН
    kpp - КПП
    dr - дата региствации
    addr - адрес
    le - экземпляр класса Legal Entity
    
    Args:
        sparql: ну это понятно
        fullName: полное название фирмы - str
    Return:
        dict с ключами fullName, shortName, grn, ogrn, kpp, dr, addr, le
    """
    sparql.setQuery(queries.getLEInfoByOgrn.format(ogrn=ogrn))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results["results"]["bindings"] == []:
        return dict()
    else:
        return _responseToDict(results["results"]["bindings"][0])


def getLeInfoByInn(sparql, inn):
    """
    Отправляет sparql запрос для получения инфы о ЮЛ.
    ?inn -> ?fullName ?shortName ?grn ?ogrn ?kpp ?dr ?addr ?le
    fullName - полное название
    shortName - сокращенное название
    grn -ГРН
    ogrn - ОГРН
    kpp - КПП
    dr - дата региствации
    addr - адрес
    le - экземпляр класса Legal Entity
    
    Args:
        sparql: ну это понятно
        fullName: полное название фирмы - str
    Return:
        dict with key (fullName, shortName, grn, ogrn, kpp, dr, addr, le)
    """
    sparql.setQuery(queries.getLEInfoByInn.format(inn=inn))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results["results"]["bindings"] == []:
        return dict()
    else:
        return _responseToDict(results["results"]["bindings"][0])
   



def getFeListByLe(sparql, le):
    """
    Возврацает список Founder Entity для экземпляра Legal Entity
    ?le -> ?name ?inn ?shareNominal ?sharePerc
    name - имя учередителя
    inn - инн учередителя
    shareNominal - номинал суммы в уставном капитале
    sharePerc - доля в уставном капитале
    
    Args:
        sparql: без комментариев
        le: URI экземпляра Legal Entity
    Return:
        list of dict with keys (name, inn, shareNominal, harePerc)
    """
    sparql.setQuery(queries.getFEListByLE.format(le=le))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return list(set(map(_responseToDict, results["results"]["bindings"])))

def getPawpoaListByLe(sparql, le):
    """
    Возврацает список Person Acting Without Power Of Auttorney Entity для экземпляра Legal Entity
    ?le -> ?phone_number ?job_title ?ppa_name ?inn_ppa
    phone_number - номер телефона
    job_title - должность
    ppa_name - имя
    inn_ppa - инн
    
    Args:
        sparql: без комментариев
        le: URI экземпляра Legal Entity
    Return:
        list of dict with keys (ppa_name, inn_ppa, job_title, phone_number)
    """
    sparql.setQuery(queries.getPAWPOAListByLE.format(le=le))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return list(set(map(_responseToDict, results["results"]["bindings"])))






#==============================================================================
# Далее идет набор функцие для получения информации о человеке
#==============================================================================

def getAnswerAboutPersonByName(sparql, name):
    """
    Формирует ответ с информацией о человеке по имени.
    Args:
        sparql: ну это понятно
        name: имя человека - str
    Return:
        Строка содержащая ответ по запросу.
    """
    results = getPersonInfoByName(sparql, name)
    if results != []:
        results = results[0]
    else:
        results = dict()
        
    lesFE = None
    lesPOWPOA = None
    
    if results.get("person") is not None:
        person = results.get("person")
        lesFE = getLeListWherePersonIsFe(sparql, person)
        if lesFE != []:
            lesFE = [templates.leByFeInListInfo.format(
                    fullName = leFE.get("fullName", infoStub),
                    shortName = leFE.get("shortName", infoStub),
                    inn = leFE.get("inn", infoStub),
                    ogrn = leFE.get("ogrn", infoStub),
                    sharePerc = leFE.get("sharePerc", infoStub),
                    shareNominal = leFE.get("shareNominal", infoStub)
                    ) for leFE in lesFE]
            lesFE = "\n".join(itertools.starmap(_listElem, enumerate(lesFE, start=1)))
            
        lesPOWPOA = getLeListWherePersonIsPowpoa(sparql, person)
        if  lesPOWPOA != []:
            lesPOWPOA = [templates.leByPowpoaInListInfo.format(
                    fullName = lePOWPOA.get("fullName", infoStub),
                    shortName = lePOWPOA.get("shortName", infoStub),
                    job = lePOWPOA.get("joib_title", infoStub)
                    ) for lePOWPOA in lesPOWPOA]
            lesPOWPOA = "\n".join(itertools.starmap(_listElem, enumerate(lesPOWPOA, start=1)))
            
    answer = templates.personMainInfo.format(
            name = results.get("name", infoStub),
            inn = results.get("inn", infoStub),
            lesFeList = lesFE if lesFE != [] and lesFE is not None else listStub,
            lePowpoaList = lesPOWPOA if lesPOWPOA != [] and lesPOWPOA is not None else listStub
            )
        
    return answer



def getPersonInfoByName(sparql, name):
    """
    Отправляет sparql запрос для получения инфы о человеке.
    ?name -> ?name ?inn ?person
    name - имя
    inn - инн
    person - экземпляр класса Person
    
    Args:
        sparql: ну это понятно
        name: имя человека - str
    Return:
        dict with keys (name, inn, person)
    """
    sparql.setQuery(queries.getPersonInfo.format(name=name))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results["results"]["bindings"] == []:
        return []
    else:
        return list(set(map(_responseToDict, results["results"]["bindings"])))


def getLeListWherePersonIsFe(sparql, person):
    """
    Отправляет sparql запрос для получения списка компаний,
    в которых человек является учередителем.
    ?person -> ?fullName ?shortName ?inn ?ogrn ?shareNominal ?sharePerc
    person - экземпляр класса Person
    fullName - полное название
    shortName - сокращенное название
    ogrn - ОГРН
    shareNominal - номинал суммы в уставном капитале
    sharePerc - доля в уставном капитале
    
    Args:
        sparql: ну это понятно
        person: экземпляр класса Person
    Return:
        dict with keys (fullName, shortName, inn, ogrn, shareNominal, sharePerc)
    """
    sparql.setQuery(queries.getLEListWherePersonIsFE.format(person=person))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return list(set(map(_responseToDict, results["results"]["bindings"])))


def getLeListWherePersonIsPowpoa(sparql, person):
    """
    Отправляет sparql запрос для получения списка компаний,
    в которых человек является  лицом, имеющем право без
    доверенности действовать от имени юридического лица.
    ?person -> ?fullName ?shortName ?job_title
    person - экземпляр класса Person
    fullName - полное название
    shortName - сокращенное название
    job_title - должность
    
    Args:
        sparql: ну это понятно
        person: экземпляр класса Person
    Return:
        dict with keys (fullName, shortName, job_title)
    """
    sparql.setQuery(queries.getLeListWherePersonIsPOWPOA.format(person=person))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return list(set(map(_responseToDict, results["results"]["bindings"])))
    

if __name__ == "__main__":
    sparql = SPARQLWrapper("http://hackaton.datafabric.cc/blazegraph/namespace/kb/sparql")
    FULL_NAME = "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \\\"СЕПТА\\\""
    SHORT_NAME = "ООО \\\"СЕПТА\\\""
    OGRN = "1047796401003"
    INN = "7701541233"
    NAME1 = "Соболева Елена Анатольевна"
    LE = "http://example.com/legalentity/e7ee35f6-8056-51e9-ae7c-7dca42abfece"
    PERSON = "http://example.com/person/ab879410-c0ad-5662-bdc0-54e0317648c2"
    res1 = getAnswerAboutLeByRequisit(sparql, INN, "inn")
    res2 = getAnswerAboutPersonByName(sparql, NAME1)












