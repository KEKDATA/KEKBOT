#==============================================================================
# Запросы для получения информации о ЮЛ
#==============================================================================

getLEInfoByFullName = """\
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#>
SELECT ?fullName ?shortName ?grn ?ogrn ?inn ?kpp ?dr ?addr ?le{{
?nameE fts:p16_full_name ?fullName;
a fts:C38_Name_Entity;
fts:p82_refers_to_company ?le.
OPTIONAL{{?nameE fts:p17_short_name ?shortName.}}
OPTIONAL{{
?fe a fts:C54_Founder_Entity;
fts:p82_refers_to_company ?le;
fts:p76_entered_on_registry_with ?rnd.
}}
OPTIONAL{{?rnd fts:p1_state_registration_number ?grn.}}
OPTIONAL{{?rnd fts:p2_date ?dr.}}
OPTIONAL {{
?le fts:p28_le_primary_state_registration_number ?ogrn.
}}
OPTIONAL {{
?tae fts:p82_refers_to_company ?le;
a fts:C44_LE_Tax_Accounting_Entity;
fts:p36_tax_reason_code ?kpp.
?tae a fts:C44_LE_Tax_Accounting_Entity;
fts:p82_refers_to_company ?le;
fts:p35_le_individual_tax_number ?inn.
}}
OPTIONAL {{
?addrE a fts:C39_Address_Entity;
fts:p82_refers_to_company ?le;
rdfs:label ?addr.
}}
BIND("{full_name}" as ?fullName)
}}LIMIT 10
"""


getLEInfoByShortName = """\
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#>
SELECT ?fullName ?shortName ?grn ?ogrn ?inn ?kpp ?dr ?addr ?le{{
?nameE fts:p17_short_name ?shortName;
a fts:C38_Name_Entity;
fts:p82_refers_to_company ?le.
OPTIONAL{{?nameE fts:p16_full_name ?fullName.}}
OPTIONAL{{
?fe a fts:C54_Founder_Entity;
fts:p82_refers_to_company ?le;
fts:p76_entered_on_registry_with ?rnd.
}}
OPTIONAL{{?rnd fts:p1_state_registration_number ?grn.}}
OPTIONAL{{?rnd fts:p2_date ?dr.}}
OPTIONAL {{
?le fts:p28_le_primary_state_registration_number ?ogrn.
}}
OPTIONAL {{
?tae fts:p82_refers_to_company ?le;
a fts:C44_LE_Tax_Accounting_Entity;
fts:p36_tax_reason_code ?kpp.
?tae a fts:C44_LE_Tax_Accounting_Entity;
fts:p82_refers_to_company ?le;
fts:p35_le_individual_tax_number ?inn.
}}
OPTIONAL {{
?addrE a fts:C39_Address_Entity;
fts:p82_refers_to_company ?le;
rdfs:label ?addr.
}}
BIND("{short_name}" as ?shortName)
}}LIMIT 10
"""

getLEInfoByOgrn = """\
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#>
SELECT  ?fullName ?shortName ?grn ?ogrn ?inn ?kpp ?dr ?addr ?le{{
?le fts:p28_le_primary_state_registration_number ?ogrn.

?nameE fts:p82_refers_to_company ?le;
a fts:C38_Name_Entity.
  
OPTIONAL{{?nameE fts:p17_short_name ?shortName.}}
OPTIONAL{{?nameE fts:p16_full_name ?fullName.}}
OPTIONAL{{
?fe a fts:C54_Founder_Entity;
fts:p82_refers_to_company ?le;
fts:p76_entered_on_registry_with ?rnd.
}}
OPTIONAL{{?rnd fts:p1_state_registration_number ?grn.}}
OPTIONAL{{?rnd fts:p2_date ?dr.}}
OPTIONAL {{
?tae fts:p82_refers_to_company ?le;
a fts:C44_LE_Tax_Accounting_Entity;
fts:p36_tax_reason_code ?kpp.
?tae a fts:C44_LE_Tax_Accounting_Entity;
fts:p82_refers_to_company ?le;
fts:p35_le_individual_tax_number ?inn.
}}
OPTIONAL {{
?addrE a fts:C39_Address_Entity;
fts:p82_refers_to_company ?le;
rdfs:label ?addr.
}}
BIND("{ogrn}" as ?ogrn)
}}LIMIT 10
"""


getLEInfoByInn = """\
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#>
SELECT ?fullName ?shortName ?grn ?ogrn ?inn ?kpp ?dr ?addr ?le{{
?tae fts:p35_le_individual_tax_number ?inn;
     a fts:C44_LE_Tax_Accounting_Entity;
  	 fts:p82_refers_to_company ?le.
OPTIONAL{{?tae fts:p36_tax_reason_code ?kpp.}}
  
OPTIONAL{{ 
?nameE fts:p82_refers_to_company ?le;
a fts:C38_Name_Entity.
OPTIONAL{{?nameE fts:p16_full_name ?fullName.}}
OPTIONAL{{?nameE fts:p17_short_name ?shortName.}}
}}
OPTIONAL{{
?fe a fts:C54_Founder_Entity;
fts:p82_refers_to_company ?le;
fts:p76_entered_on_registry_with ?rnd.
OPTIONAL{{?rnd fts:p1_state_registration_number ?grn.}}
}}
OPTIONAL{{?rnd fts:p2_date ?dr.}}
OPTIONAL {{
?le fts:p28_le_primary_state_registration_number ?ogrn.
}}
OPTIONAL {{
?addrE a fts:C39_Address_Entity;
fts:p82_refers_to_company ?le;
rdfs:label ?addr.
}}
BIND("{inn}" as ?inn)
}}LIMIT 10
"""



getFEListByLE = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#>
SELECT ?name ?inn ?shareNominal ?sharePerc{{
?fe fts:p82_refers_to_company ?le;
a fts:C54_Founder_Entity.
?fe fts:p124_has_share ?hs.  
OPTIONAL{{?hs fts:p51_nominal_share_of_value_in_ruble ?shareNominal.}}
OPTIONAL{{?hs fts:p52_percentage_share ?sharePerc.}}
?fe fts:p101_relates_to_person ?person.
?person foaf:name ?name.
OPTIONAL{{?person fts:p75_ie_individual_tax_number ?inn.}}
BIND(<{le}> as ?le)
}}LIMIT 10
"""

getPAWPOAListByLE = """\
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#>
SELECT ?phone_number ?job_title ?ppa_name ?inn_ppa{{
?ppa fts:p82_refers_to_company ?le;
a fts:C51_Person_Acting_Without_Power_Of_Auttorney_Entity. 
OPTIONAL {{?ppa fts:p41_phone_number ?phone_number.}}
OPTIONAL{{
?ppa fts:p121_holds_position ?je.
?je fts:p47_job_title ?job_title.
}}
?ppa fts:p101_relates_to_person ?person.
?person foaf:name ?ppa_name.
OPTIONAL{{?person fts:p75_ie_individual_tax_number ?inn_ppa.}}
BIND(<{le}> as ?le)
}}LIMIT 10
"""


#==============================================================================
# Запросы для получения информации о человеке
#==============================================================================

getPersonInfo = """\
PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#> 
SELECT DISTINCT ?name ?inn ?person{{ 
?person foaf:name ?name. 
OPTIONAL{{?person fts:p75_ie_individual_tax_number ?inn.}}
BIND ("{name}" AS ?name) 
}}LIMIT 10
"""


getLEListWherePersonIsFE = """\
PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#> 
SELECT ?fullName ?shortName ?inn ?ogrn ?shareNominal ?sharePerc{{ 
?fe fts:p101_relates_to_person ?person;
a fts:C54_Founder_Entity;
fts:p82_refers_to_company ?le.
?le a fts:C9_Legal_Entity.
?nameE fts:p82_refers_to_company ?le;
a fts:C38_Name_Entity.
OPTIONAL{{?nameE fts:p16_full_name ?fullName;}}
OPTIONAL{{?nameE fts:p17_short_name ?shortName.}}     
OPTIONAL{{?le fts:p28_le_primary_state_registration_number ?ogrn.}}
OPTIONAL{{
?tae fts:p82_refers_to_company ?le.
?tae fts:p35_le_individual_tax_number ?inn;
a fts:C44_LE_Tax_Accounting_Entity. 
}}
OPTIONAL{{?fe fts:p124_has_share ?hs.  
OPTIONAL{{?hs fts:p51_nominal_share_of_value_in_ruble ?shareNominal.}}
OPTIONAL{{?hs fts:p52_percentage_share ?sharePerc.}}
}}  
BIND (<{person}> AS ?person) 
}}LIMIT 10
"""

getLeListWherePersonIsPOWPOA = """\
PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
PREFIX fts: <https://w3id.org/datafabric.cc/ontologies/fts#> 
SELECT DISTINCT ?fullName ?shortName ?job_title{{ 
?ppa fts:p101_relates_to_person ?person;
     a fts:C51_Person_Acting_Without_Power_Of_Auttorney_Entity;
     fts:p82_refers_to_company ?le.
OPTIONAL{{?le a fts:C9_Legal_Entity.
?nameE fts:p82_refers_to_company ?le;
a fts:C38_Name_Entity.
OPTIONAL{{?nameE fts:p16_full_name ?fullName;}}
OPTIONAL{{?nameE fts:p17_short_name ?shortName.}}
}}
OPTIONAL{{
?ppa fts:p121_holds_position ?je.
?je fts:p47_job_title ?job_title.
}}
BIND (<{person}> AS ?person) 
}}LIMIT 10
"""
