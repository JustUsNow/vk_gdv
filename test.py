
# Пример использования модуля
# Запрос к апи и диаграммы

#У столбчатых диаграмм есть изменяемый параметр mode, меняющий детали отображения

#Каждый раз, когда изменяется список груп, у которых нужно достать подписчиков, этот фрагмент нужно перезапустить. 100000 подписчиков грузится в среднем минуту-полторы. Запускать это можно сколько угодно раз.

#Второй фрагмент с подгрузкой количества постов можно грузить ограниченное количество раз: 5000 вызовов в день, это +- 500000 постов в день. Если вылезает ошибка (слишком больше тело ответа или превышен лимит запросов), то в файл всё равно запишутся те посты, которые успели скачаться

#Файлы с участниками имеют префикс m_, с постами - p_


import time
import json
import numpy
from vk_gdv import *

group_ids = ['33538623']

#time - для засечки времени

"""Один из этих фрагментов тоже нужно изменять каждый раз, когда обновляется датасет, чтобы датафрейм подгрузился заново. В первом данные анализируются вместе с NaN, во втором - записи с отсутствующими значениями просто выбрасываются"""

members_dfs = [pd.DataFrame(json.load(open('m_{id}.json'.format(id=group_id), 'r'))) for group_id in group_ids]
posts_dfs = [pd.DataFrame(json.load(open('p_{id}.json'.format(id=group_id), 'r'))) for group_id in group_ids]

members_dfs = [pd.DataFrame(json.load(open('m_{id}.json'.format(id=group_id), 'r'))).dropna() for group_id in group_ids]
posts_dfs = [pd.DataFrame(json.load(open('p_{id}.json'.format(id=group_id), 'r'))).dropna() for group_id in group_ids]

"""Статистика и круговая диаграмма для полового состава"""

print(sex_stats_df(members_dfs[0]))
plot_sex_pie((members_dfs[0]))

"""Статистика и столбчатая диаграмма по возрасту."""

print(age_stats_by_group_df(members_dfs[0]))
plot_age_group_bar(members_dfs[0], mode='size')

"""Статистика и столбчатая диаграмма по городам"""

print(city_stats_df(members_dfs[0]))
plot_city_bar(members_dfs[0], mode='total', count=4)

"""Статистика и столбчатая диаграмма по уровням образования"""

print(education_stats_df(members_dfs[0]))
plot_education_bar(members_dfs[0], mode='total')

"""Портрет типичного подписчика - мода?"""

print(members_dfs[0].mode())

"""Можно вывести 10 самых больших групп. ВСЕ данные в наличии у ~20% подписчиков, поэтому выборка погибает."""

a_m = avg_group_member_df(members_dfs[0], n=5)
print(a_m, end='\n\n')
#n этих групп составляют a_m.fraction.sum() от всего числа подписчиков
print('{:.2f}%'.format(a_m['fraction'].sum() * 100))

print(reactions_by_period_df(posts_dfs[0]), end='\n\n')
plot_reactions_bar(posts_dfs[0], mode='likes', period='M')

print(reactions_top_n_df(posts_dfs[0]))

plt.show()
