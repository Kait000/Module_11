import pandas as pd
import requests
import matplotlib.pyplot as plt


def get_inf_ofz(url, par):
    """Возвращает данные по облигациям федерального займа"""
    response = requests.get(url=url, params=par)
    if response.status_code == 200:
        print(f'Статус загрузки: {response}')
        print(f'Ссылка на загруженные данные: {response.url}')
        return response
    else:
        raise ValueError('Не получены данные от сервера')


def rus_colum_name(colums):
    """Русифицирует название колонок"""
    rus = {'SECID': 'Код инструмента', 'SHORTNAME': 'Имя',
           'PREVWAPRICE': 'Средневзвешенная цена предыдущего дня, % к номиналу',
           'YIELDATPREVWAPRICE': 'Доходность*, %', 'COUPONVALUE': 'Купон',
           'NEXTCOUPON': 'Дата купона', 'ACCRUEDINT': 'НКД', 'PREVPRICE': 'Последняя цена пред. дня',
           'LOTSIZE': 'Размер лота', 'FACEVALUE': 'Непог.долг', 'BOARDNAME': 'Режим торгов', 'BOARDID': 'Код режима',
           'STATUS': 'Статус', 'MATDATE': 'Погашение', 'DECIMALS': 'Точность',
           'COUPONPERIOD': 'Длительность купона', 'ISSUESIZE': 'Объем выпуска, штук',
           'PREVLEGALCLOSEPRICE': 'Цена', 'PREVDATE': 'Дата последних торгов',
           'SECNAME': 'Наименование', 'REMARKS': 'Примечание', 'MARKETCODE': 'Рынок', 'INSTRID': 'Группа инструментов',
           'SECTORID': 'Сектор', 'MINSTEP': 'Мин. шаг цены', 'FACEUNIT': 'Валюта номинала',
           'BUYBACKPRICE': 'Цена оферты', 'BUYBACKDATE': 'Дата, к кот.рассч.доходность', 'ISIN': 'ISIN',
           'LATNAME': 'Англ. наименование', 'REGNUMBER': 'Регистрационный номер',
           'CURRENCYID': 'Сопр. валюта инструмента', 'ISSUESIZEPLACED': 'Объем в обращении',
           'LISTLEVEL': 'Уровень листинга', 'SECTYPE': 'Тип ценной бумаги', 'COUPONPERCENT': 'Купон, %',
           'OFFERDATE': 'Дата оферты', 'SETTLEDATE': 'Дата расчетов', 'LOTVALUE': 'Номинал лота',
           'FACEVALUEONSETTLEDATE': 'Номинальная стоимость на дату расчетов'}
    for item in colums:
        if item in rus:
            colums[colums.index(item)] = rus[item]
    return colums


def del_colum(colum):
    """Удаляем колонки которые не потребуются для анализа"""
    del_ = ['Код режима', 'Код инструмента', 'Размер лота', 'Тип ценной бумаги', 'Уровень листинга',
            'Объем в обращении', 'Сопр. валюта инструмента', 'Регистрационный номер', 'Англ. наименование',
            'Дата, к кот.рассч.доходность', 'Цена оферты', 'Валюта номинала', 'Мин. шаг цены', 'Сектор',
            'Группа инструментов', 'Рынок', 'Примечание', 'Дата последних торгов', 'Объем выпуска, штук',
            'Дата оферты', 'Дата расчетов', 'Статус', 'Режим торгов', 'Точность', 'Наименование',
            'Средневзвешенная цена предыдущего дня, % к номиналу', 'Номинальная стоимость на дату расчетов',
            'Последняя цена пред. дня', 'Непог.долг', 'Номинал лота']
    return colum.drop(del_, axis=1)


URL = 'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQOB/securities.json'
param = {'first': 30}  # запрашиваем первые 30 записей
inf_ofz = get_inf_ofz(URL, param)

inf_ofz = inf_ofz.json()    # преобразуем полученные данные в формат json

colum_name = inf_ofz['securities']['columns']   # получаем список названий колонок
colum_name = rus_colum_name(colum_name)         # русифицируем колонки
data_ofz = inf_ofz['securities']['data']        # получаем список списков данных по ОФЗ

table_ofz_pd = pd.DataFrame(data_ofz, columns=colum_name)   # приводим данные к структуре DataFrame ('pandas')
table_ofz_pd = table_ofz_pd.set_index('ISIN')               # в качестве индекса используем 'ISIN'
table_ofz_pd.to_excel('full_info_ofz.xlsx')                 # сохраняем все данные в таблицу (пусть будут...)

table_ofz_pd = table_ofz_pd.loc[table_ofz_pd['Доходность*, %'] > 0]     # убираем ОФЗ с доходностью < 0
table_ofz_pd = table_ofz_pd.loc[table_ofz_pd['Номинал лота'] == 1000]   # убираем ОФЗ с амортизацией долга
table_ofz_pd = table_ofz_pd.dropna(subset=['Цена', 'Купон, %'])         # убираем ОФЗ по которым нет данных (NoN)
table_ofz_pd = del_colum(table_ofz_pd)                                  # убираем лишние колонки

# меняем значение колонки 'Длительность купона' на кол-во выплат за год
table_ofz_pd['Длительность купона'] = table_ofz_pd['Длительность купона'].apply(lambda x_: 365 // x_)
table_ofz_pd.rename(columns={'Длительность купона': 'Кол-во купонов'}, inplace=True)
# переставляем колонки
table_ofz_pd = table_ofz_pd.reindex(columns=['Имя', 'Погашение', 'Доходность*, %', 'Цена', 'НКД', 'Купон',
                                             'Кол-во купонов', 'Купон, %', 'Дата купона'])
table_ofz_pd = table_ofz_pd.sort_values(by='Погашение')     # сортируем строки
table_ofz_pd.to_excel('res_info_ofz.xlsx')                  # сохраняем результат в таблицу
print(f'\n\033[32m{table_ofz_pd}')      # выводим таблицу в терминал

# создаем график доходности ОФЗ
plt.figure(figsize=(16, 6))
plt.scatter(table_ofz_pd['Погашение'], table_ofz_pd['Доходность*, %'])  # строим график на основе DataFrame
plt.grid(True, color='g', linestyle=':', linewidth=0.3)          # добавляем сетку
plt.title('Доходность ОФЗ', fontsize=15)   # добавляем заголовок
plt.xlabel('Дата погашения')                     # добавляем названия осей
plt.ylabel('Оценочная доходность в %')
plt.gcf().autofmt_xdate()   # поворачиваем надписи оси х

# подписываем значения точек на графике
for x_coord, y_coord, label in zip(table_ofz_pd['Погашение'], table_ofz_pd['Доходность*, %'], table_ofz_pd['Имя']):
    plt.text(x_coord, y_coord, label, fontsize=7, ha='left')
plt.show()
