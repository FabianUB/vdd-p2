import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

### PREPARACIÓN DE DATOS

df = pd.read_csv("owid-energy-data.csv")
df = df[['country','year','greenhouse_gas_emissions','electricity_demand','electricity_generation','fossil_fuel_consumption','fossil_electricity','fossil_share_elec',
        'renewables_consumption','renewables_electricity','renewables_share_elec']]

countryByGDP = ['Germany','France','Italy','Spain','Netherlands','Poland','Sweden','Belgium','Ireland','Austria','Denmark',
               'Romania','Czechia','Finland','Portugal','Greece','Hungary','Slovak Republic','Bulgaria','Luxembourg','Croatia',
               'Croatia','Lithuania','Slovenia','Latvia','Estonia','Cyprus','Malta']
half = len(countryByGDP) // 2
richerHalf = countryByGDP[:half]
poorerHalf = countryByGDP[half:]

# Vamos a comparar la información solo de 2020 en adelante

df = df.loc[df['year'] >= 2000]

# Separamos el dataset según las dos mitades
dfRicherHalf = df.loc[df['country'].isin(richerHalf)]
dfPoorerHalf = df.loc[df['country'].isin(poorerHalf)]

dfRicherHalfProd = dfRicherHalf.groupby(by='year')[['fossil_electricity','renewables_electricity']].sum()
dfPoorerHalfProd = dfPoorerHalf.groupby(by='year')[['fossil_electricity','renewables_electricity']].sum()
dfRicherHalfProd = pd.melt(dfRicherHalfProd, ignore_index=False)
dfPoorerHalfProd = pd.melt(dfPoorerHalfProd, ignore_index=False)

dfRicherHalfNet = dfRicherHalf.groupby(by='year')[['electricity_demand','electricity_generation']].sum()
dfPoorerHalfNet = dfPoorerHalf.groupby(by='year')[['electricity_demand','electricity_generation']].sum()
dfRicherHalfNet = pd.melt(dfRicherHalfNet, ignore_index=False)
dfPoorerHalfNet = pd.melt(dfPoorerHalfNet, ignore_index=False)

dfRicherHalfPer = dfRicherHalf.groupby(by='year')[['fossil_share_elec','renewables_share_elec']].mean()
dfPoorerHalfPer = dfPoorerHalf.groupby(by='year')[['fossil_share_elec','renewables_share_elec']].mean()
dfRicherHalfPer = pd.melt(dfRicherHalfPer, ignore_index=False)
dfPoorerHalfPer = pd.melt(dfPoorerHalfPer, ignore_index=False)

dfRicherHalfCO2 = dfRicherHalf.groupby(by='year')[['greenhouse_gas_emissions']].sum()
dfPoorerHalfCO2 = dfPoorerHalf.groupby(by='year')[['greenhouse_gas_emissions']].sum()



st.title("Comparación de la evolución de energias renovables en Europa 2000 - 2022")

st.header("Comparación Energia Fósil y Energias Renovables (Porcentaje)")

st.write("Vamos a analizar la evolución de las energias renovables y su efecto en el medio ambiente, comparando a la mitad de naciones más ricas de la UE por GDP con la mitad más pobre.")

st.write("Empezamos comparando como ha evolucionado el porcentaje de energias fosiles y renovables respecto al total de energia electrica producida para cada mitad desde el año 2000 al 2022.")

dfRicherHalfPer.rename(columns={'variable':'Tipo de Energia','value':'Porcentaje (%)'},inplace=True)
dfPoorerHalfPer.rename(columns={'variable':'Tipo de Energia','value':'Porcentaje (%)'},inplace=True)

dfRicherHalfPer.loc[dfRicherHalfPer['Tipo de Energia'] == 'fossil_share_elec', 'Tipo de Energia'] = 'E. Fosiles (%)'
dfRicherHalfPer.loc[dfRicherHalfPer['Tipo de Energia'] == 'renewables_share_elec', 'Tipo de Energia'] = 'E. Renovables (%)'
dfPoorerHalfPer.loc[dfPoorerHalfPer['Tipo de Energia'] == 'fossil_share_elec', 'Tipo de Energia'] = 'E. Fosiles (%)'
dfPoorerHalfPer.loc[dfPoorerHalfPer['Tipo de Energia'] == 'renewables_share_elec', 'Tipo de Energia'] = 'E. Renovables (%)'
fig1R = px.line(dfRicherHalfPer, x=dfRicherHalfPer.index, y="Porcentaje (%)", color="Tipo de Energia", title="Porcentaje de Energia por Método de Generación (Mitad Más Rica)",color_discrete_map = {'E. Fosiles (%)':'red','E. Renovables (%)':'green'} )
fig1R.update_layout(
    xaxis_title="Año"
)
fig1P = px.line(dfPoorerHalfPer, x=dfPoorerHalfPer.index, y="Porcentaje (%)", color="Tipo de Energia", title="Porcentaje de Energia por Método de Generación (Mitad Más Pobre)",color_discrete_map = {'E. Fosiles (%)':'red','E. Renovables (%)':'green'} )
fig1P.update_layout(
    xaxis_title="Año"
)

cols = st.columns(2)
cols[0].plotly_chart(fig1R, use_container_width=True)
cols[1].plotly_chart(fig1P, use_container_width=True)

st.write("Podemos comprobar que la mitad más rica de la UE consiguió superar su porcentaje de electricidad proveniente de energia renovable respecto a las energias fosiles en 2019, mientras que la mitad más pobre tardó hasta 2022 para conseguirlo.")

st.write("Pero debemos indagar más para poder tener una visión más completa de la situacion, por ejemplo, ¿cual es la diferencia entre la generación y consumo total de energia entre las dos mitades de la UE?")

st.header("Consumo y Generación Total de Energía")

dfRicherHalfNet.rename(columns={'variable':'Neto','value':'GWh'},inplace=True)
dfPoorerHalfNet.rename(columns={'variable':'Neto','value':'GWh'},inplace=True)

dfRicherHalfNet.loc[dfRicherHalfNet['Neto'] == 'electricity_demand', 'Neto'] = 'Demanda de Electricidad (GWh)'
dfRicherHalfNet.loc[dfRicherHalfNet['Neto'] == 'electricity_generation', 'Neto'] = 'Generación de Electricidad (GWh)'
dfPoorerHalfNet.loc[dfPoorerHalfNet['Neto'] == 'electricity_demand', 'Neto'] = 'Demanda de Electricidad (GWh)'
dfPoorerHalfNet.loc[dfPoorerHalfNet['Neto'] == 'electricity_generation', 'Neto'] = 'Generación de Electricidad (GWh)'

cols = st.columns(2)
fig2R = px.bar(dfRicherHalfNet, x=dfRicherHalfNet.index, y='GWh', color='Neto',barmode='overlay', title="Generación y Consumo de Electricidad por Año (Mitad Más Rica)",opacity=1,color_discrete_map = {'Demanda de Electricidad (GWh)':'#F7C0BB','Generación de Electricidad (GWh)':'#ACD0F4'})
fig2R.update_layout(
    xaxis_title="Año"
)
fig2P = px.bar(dfPoorerHalfNet, x=dfPoorerHalfNet.index, y='GWh', color='Neto',barmode='overlay', title="Generación y Consumo de Electricidad por Año (Mitad Más Pobre)",opacity=1,color_discrete_map = {'Demanda de Electricidad (GWh)':'#F7C0BB','Generación de Electricidad (GWh)':'#ACD0F4'})
fig2P.update_layout(
    xaxis_title="Año"
)

cols[0].plotly_chart(fig2R, use_container_width=True)
cols[1].plotly_chart(fig2P, use_container_width=True)

st.write("""Podemos comprobar que mientras la mitad más rica de Europa ha tenido superávit de energía durante todo el siglo 21, la mitad más pobre ha tenido déficit de energia y han tenido que importar energia de otros paises, por lo que aunque hayan aumentado su porcentaje de energias renovables,
         no acaban de suplir su demanda de electricidad.""")

st.write("Aparte del porcentaje, vamos a observar los valores absolutos de generación de energía fosiles y renovables en las dos mitades para ver porque puede producirse esta diferencia en el abastecimiento de energia entre las dos mitades.")

st.header("Comparación Energia Fósil y Energias Renovables (Valor Absoluto)")

dfRicherHalfProd.rename(columns={'variable':'Tipo','value':'GWh'},inplace=True)
dfPoorerHalfProd.rename(columns={'variable':'Tipo','value':'GWh'},inplace=True)

dfRicherHalfProd.loc[dfRicherHalfProd['Tipo'] == 'fossil_electricity', 'Tipo'] = 'Electricidad por Combustible Fosil (GWh)'
dfRicherHalfProd.loc[dfRicherHalfProd['Tipo'] == 'renewables_electricity', 'Tipo'] = 'Electricidad por Energia Renovable (GWh)'
dfPoorerHalfProd.loc[dfPoorerHalfProd['Tipo'] == 'fossil_electricity', 'Tipo'] = 'Electricidad por Combustible Fosil (GWh)'
dfPoorerHalfProd.loc[dfPoorerHalfProd['Tipo'] == 'renewables_electricity', 'Tipo'] = 'Electricidad por Energia Renovable (GWh)'


fig3R = px.bar(dfRicherHalfProd, x=dfRicherHalfProd.index, y='GWh', color='Tipo', title="Generación de Electricidad por Método (Mitad Más Rica)",opacity=1,color_discrete_map = {'Electricidad por Combustible Fosil (GWh)':'red','Electricidad por Energia Renovable (GWh)':'green'})
fig3R.update_layout(
    xaxis_title="Año"
)
fig3P = px.bar(dfPoorerHalfProd, x=dfPoorerHalfProd.index, y='GWh', color='Tipo', title="Generación de Electricidad por Método (Mitad Más Pobre)",opacity=1,color_discrete_map = {'Electricidad por Combustible Fosil (GWh)':'red','Electricidad por Energia Renovable (GWh)':'green'})
fig3P.update_layout(
    xaxis_title="Año"
)
cols = st.columns(2)
cols[0].plotly_chart(fig3R, use_container_width=True)
cols[1].plotly_chart(fig3P, use_container_width=True)

st.write("""Podemos comprobar que la energía generada por combustibles fosiles y renovables de la mitad más rica ha pegado un aumento significativo, de 1500 GWh a 2000GWh en 22 años, mientras que en la mitad más pobre solo ha pasado de 150 GWh a 200GWh,
         por lo que tiene sentido los datos que vemos en el gráfico anterior de que sean deficitarios de energía.""")

st.header("Evolución de los Gases de Efecto Hivernadero Emitidos")

fig4R = px.line(dfRicherHalfCO2, x=dfRicherHalfCO2.index, y='greenhouse_gas_emissions')
fig4R.update_layout(
    xaxis_title="Año",
    yaxis_title="Toneladas de CO2",
    title="Emisiones de CO2 (Mitad Más Rica)"
)

fig4P = px.line(dfPoorerHalfCO2, x=dfPoorerHalfCO2.index, y='greenhouse_gas_emissions')
fig4P.update_layout(
    xaxis_title="Año",
    yaxis_title="Toneladas de CO2",
    title="Emisiones de CO2 (Mitad Más Pobre)"
)

cols = st.columns(2)
cols[0].plotly_chart(fig4R, use_container_width=True)
cols[1].plotly_chart(fig4P, use_container_width=True)

st.write("Podemos ver que en ambos casos, tanto en la mitad más rica como en la mitad más pobre, ha habido progresos en reducir la cantidad de gases de efecto hivernadero, teniendo en cuenta incluso las diferencias en la adopción de energias renovables entre las dos mitades.")
st.write("""Es interesante destacar, que incluso en el nivel más bajo de emisiones de la mitad más rica en 2020, sus emisiones son 6 veces más altas que el pico de emisiones de la mitad más pobre, por lo que incluso aunque la mitad más pobre no sea tan rápida en la adopcion
         de las energías renovables, sus emisiones son mucho más bajas que las de la mitad más rica. """)