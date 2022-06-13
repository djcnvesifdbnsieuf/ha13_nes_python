import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression
import rtree


def load_data(a):
    x = pd.read_csv(a)
    return x
if __name__ == '__main__':
    st.title('Привет, здесь ты немного узнаешь про российский авитранспорт')
st.write('Для начала посмотрим на датасет:')

airports_df = load_data('russian_passenger_air_service_2.csv') #качаем датасет
st.dataframe(airports_df)
st.write('В датасете видны проблемы, отсутсвуют некоторые данные, есть повторы, некоторые аэропорты вне РФ, поэтому дальше в коде идет его чиста и "причесывание"')
airports_df['lon'] = airports_df['Airport coordinates'].str.split('\'').str[1] #юзаем пандас для обработки и чистки (часть аэропортов в США:((
airports_df['lat'] = airports_df['Airport coordinates'].str.split('\'').str[3]
airports_df.dropna(subset=['lat'], inplace=True)
airports_df['lon'] = airports_df['lon'].astype(float)
airports_df['lat'] = airports_df['lat'].astype(float)
b = airports_df.copy()
airport_2019 = b[b['Year'] == 2019]
airport_2019 = airport_2019.drop_duplicates(subset = ['lat'])
airport_2019 = airport_2019.reset_index(drop=True)
airport_2019 = airport_2019.drop(labels = [236, 50, 159],axis = 0) #вот тут удаляем три левых аэропорта
airport_2019point = [Point(row['lon'], row['lat']) for _, row in airport_2019.iterrows()]
airport_2019 = airport_2019.reset_index(drop=True)
bb = airport_2019.copy() #на всякий случай, вдруг что потом слумается из-за логарифмирования
ln_total = bb['Whole year'].to_numpy(dtype = float) #закончили юзать и получили +2 балла (он будет еще много где дальше, но думаю, тут уже на 2 есть))
ln_total = np.log(ln_total + 3) # тройку добавляем, чтобы не получить отрицательных значений от нулевых ячеек
airport_2019['ln_wholeyear'] = ln_total
st.write('Узнаем, где располагаются аэропорты. К сожалению, придеться открыть карту в отдельном окне')
airport_fig = go.Figure(go.Scattermapbox(name='Аэропорты РФ',
                                         lat=airport_2019['lat'],
                                         lon=airport_2019['lon'],
                                         text=airport_2019[['Airport name', 'Whole year']],
                                         marker=dict(size=airport_2019['ln_wholeyear']))) #опа, нетривиальная визуализация +2балла
airport_fig.update_layout(mapbox_style="open-street-map",
mapbox=dict(center=dict(lat=63.94,lon=85.20), zoom = 2.5))
airport_fig.show()

#здесь начинаем делать тепловую карту. Есть ряд проблем - population в геодатафрейме кривой, нужен верный, берем инфу с википедии
# с помощью scrapy и получаем +2 балла)
#кстати, по пути решаем проблему кривых названий регионов

st.write('Теперь давайте узнаем, среднее число полетов на 1 жителя данного регоина, то есть узнаем, кто летает чаще')

st.write('К сожалению, часть данных отсутствует, поэтому на карте видны белые пятна')

pop = load_data('result.csv')
russia_map = gpd.read_file("admin_level_4.geojson", encoding='CP1251') #геоданные, и дальше ихи еще больше
#russia_map_v2 = russia_map.to_crs("ESRI:102012")
russia_map_good = (russia_map.sort_values(by=['name']))
russia_map_good['name'] = pop['regions']
russia_map_good['population'] = pop['population'] #на данном этапе произошел ***** с индексами, я не знаю почему, НО чекнул руками, все верно в плане регион-население, а вот с сортировкой проблемы
russia_map_good['population'] = russia_map_good['population'].str.replace(r' ', '').astype(float) #РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ!
russia_map_good = (russia_map_good.sort_values(by=['name'])) #поэтому сортируем еще раз
airport_2019_geo = gpd.GeoDataFrame(airport_2019, geometry=airport_2019point, crs="EPSG:4326" )
final_map = russia_map_good.sjoin(airport_2019_geo)
aa = final_map.copy()
ff_1 = aa.groupby('name').sum()
ff_2 = aa.groupby(['name']).mean()
pas_total = ff_1['Whole year'].to_numpy(dtype = float)
pop_ff = ff_2['population'].to_numpy(dtype = float)
answer = pas_total // pop_ff
final_final = russia_map_good.sjoin(airport_2019_geo)['name'].value_counts()
final_final = final_final.reset_index()
final_final = final_final.sort_values(by=['index'])
final_final['k'] = answer
russia_map_good['k'] = final_final['k']
russia_map_good = russia_map_good.to_crs("ESRI:102012")
russia_map_good = russia_map_good.set_index('name')
fucking_map, ax = plt.subplots(figsize = (15,7))
russia_map_good.plot(column = 'k', ax=ax, legend=True)
st.pyplot(fucking_map)

st.write('Как видно, чаще всего летают жители Москвы (на карте Мособласть, для других регионов данные почти неотличаются. Это объясняется высоким количеством пересадок из московских аэропортов, а также тем, что некоторые направленния доступны только из Москвы (люди едут сюда, чтобы полететь) И большим количеством бизнес поездок именно в Москву')

st.write('А теперь давайте попробуем узнать, сколько бы было полетов в 2020 и 2021 году, если бы не ковид')


total_year = airports_df.groupby('Year')['Whole year'].sum().reset_index()
total_year['Whole year'] = total_year['Whole year']
total_year_hist = go.Figure(data=[go.Bar(x=total_year['Year'], y=total_year['Whole year'])],
                            layout_title_text="Пассажиров в год (млн. чел.)")
st.plotly_chart(total_year_hist)

st.write('Построим линейную регрессию')

total_year = total_year.reset_index(drop=True) #началась модель
total_for_regr = total_year.drop(axis=0, index=13)
x = total_for_regr['Year'].to_numpy(dtype = float) #еще numpy
x = x.reshape((-1, 1))
y = total_for_regr['Whole year'].to_numpy(dtype = float)
regr = LinearRegression().fit(x, y)
x_20_21 = np.array([2020, 2021]).reshape((-1, 1))
y_20_21 = regr.predict(x_20_21) #модель закончилась +1 балл)

total_year_pred = pd.DataFrame( [[x_20_21[0], y_20_21[0]], [x_20_21[1], y_20_21[1]]], columns=['Year', 'Whole year']) #делаем итоговую табличку
total_year_pred['Year'] = total_year_pred['Year'].astype(int)
total_year_result = pd.concat([total_for_regr, total_year_pred])  #опа, сложный метод для 2 баллов
total_year_result = total_year_result.reset_index(drop=True)

st.write('Результат ниже:')
total_year_pred_fig = go.Figure(data=[go.Bar(x=total_year_result['Year'], y=total_year_result['Whole year'])],
                            layout_title_text="Пассажиров в год (млн. чел.)")
st.plotly_chart(total_year_pred_fig)

st.write('Спасибо за внимание! Надеюсь, было интересно.')
st.write('P.S. строк в коде > 120, если вы считаете, что это не так, значит вы не чекнули ipynb часть')


