from fake_headers import Headers

cookie = {
    'market': '0dfbe938-8fbe-48d1-8de6-5a5c799d0458',
    'userType': '',
    '_ym_uid': '1655575683295712603',
    '_userGUID': '0:l4k70kjc:S86HFHD6TGW0qbL7nxsU7k06YfA98Ykt',
    'scarab.visitor': '%22181FABBB7FF785BF%22',
    'BITRIX_SM_CITY_ID': '80',
    'BX_USER_ID': '1db8e80bb776c10c20a3ce360c94e415',
    'city': '66',
    'digi_uc': 'W1sidiIsIjY3MjU4NzgiLDE2NjcxMTU3NTIxOThdLFsidiIsIjY5OTAzMjgiLDE2NjcxMTU1MDcyMDBdLFsidiIsIjkxOTE2OTciLDE2NjcxMTU0OTE5NjRdLFsidiIsIjU0MDEzMTQiLDE2NjcwNzUwODQzMzldLFsidiIsIjk3MTYxNzQiLDE2NjcwNzQ5OTY2NDhdLFsidiIsIjcwOTE2OTEiLDE2NjcwNzQ5NTM5NTldLFsidiIsIjc0NjExMDEiLDE2NjcwNzQxNjk5MTJdLFsidiIsIjExMjc4OTciLDE2NjcwNzQwNDI4MzRdLFsidiIsIjk0MTExMjgiLDE2NjcwNzM4OTMwMTldLFsidiIsIjIzODYxMDEiLDE2NjcwNzM4NzQ1MzBdLFsidiIsIjExMzAwODUiLDE2NjY2MDA4NTgxNzBdLFsidiIsIjk5MTczOSIsMTY2NjYwMDYzMzAyM10sWyJ2IiwiODg2Njg0OSIsMTY2NjYwMDI4NDAyMl0sWyJ2IiwiMTA1OTg4NSIsMTY2NzExNjgxMzc2Ml1d',
    'modeCat': 'true',
    '_ym_d': '1671472755',
    'scarab.profile': '%229725991%7C1676217873%7C4934124%7C1675876252%7C2200874%7C1675876221%7C7441379%7C1675090820%7C1181003%7C1674984209%7C3842128%7C1673806498%22',
    '_ga_9L8NF5QCN5': 'GS1.1.1677847235.2.0.1677847237.58.0.0',
    '__ddg1_': 'sJUr5PG2PbMbUokXQATL',
    '_ga_TG23RC4SZ6': 'GS1.1.1681147573.2.0.1681147573.0.0.0',
    '_ga': 'GA1.2.940607187.1655575683',
    'mindboxDeviceUUID': 'b61f1aac-2ddb-4d1b-a6a8-53523293fca4',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b61f1aac-2ddb-4d1b-a6a8-53523293fca4%22%7D',
    'digi_uc': 'W1sidiIsIjk4NjYzMTYiLDE2ODQzMzg3NTg2MDNdXQ==',
    '_gid': 'GA1.2.539348335.1684950238',
    '_ym_isad': '1',
    'dSesn': 'ba98365c-19dd-ce69-897e-26e7057a7fb1',
    '_dvs': '0:li39z8yx:~oMiduFFSQM38AdYaWoXCYFWlWti6vA7',
    '_gat': '1',
    '_ym_visorc': 'b',
}
# Создаем фейковый заголовок при запросе доступа на сайт
header_fake = Headers()
header = header_fake.generate()

