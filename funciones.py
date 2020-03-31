# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene: mauanaya
# -- repositorio: https://github.com/mauanaya/LAB_2_VMAA
# -- ------------------------------------------------------------------------------------ -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene: mauanaya
# -- repositorio: https://github.com/mauanaya/LAB_2_VMAA
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np
import math as math
from datetime import date, timedelta


#%% FUNCION: leer archivo
def f_leer_archivo(param_archivo):
    """"
    Parameters
    ----------
    param_archivos : str : nombre de archivo a leer

    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido

    Debugging
    ---------
    param_archivo =  'trading_historico.xlsx'

    """
    # Leer archivo de datos y guardarlo en Data Frame
    df_data = pd.read_excel(param_archivo, sheet_name='Hoja1')

    # Convertir a minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower() for i in range(0, len(df_data.columns))]
    
    # Asegurar que ciertas columnas son tipo numerico
    numcols =  ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    return df_data

#%% FUNCION: 
def f_pip_size(param_ins):
    """"
    Parameters
    ----------
    param_ins : str : nombre de instrumento 

    Returns
    -------
    pips_inst : 

    Debugging
    ---------
    param_ins =  'trading_historico.xlsx'

    """
    
    ""
    
    # encontrar y eliminar un guion bajo
    inst = param_ins.replace('_', '')
    inst = param_ins.replace('-2', '')
    
    # transformar a minusculas
    inst = inst.lower()
    
    #lista de pips por instrumento
    pips_inst =  {'audusd' : 10000, 'gbpusd': 10000, 'xauusd': 10, 'eurusd': 10000, 'xaueur': 10,
                  'nas100usd': 10, 'us30usd': 10, 'mbtcusd':100, 'usdmxn': 10000, 'eurjpy':10000, 
                  'gbpjpy':10000, 'usdjpy':10000, 'btcusd':10, 'eurgbp':10000, 'usdcad':10000,}
    
    return pips_inst[param_ins]

#%% FUNCION:
def f_columnas_tiempo(param_data):

#convertir columna de 'closetime' y 'opentime' utilizando pd.to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1*np.exp(9)
    for i in range(0, len(param_data['closetime']))]
    
    return param_data
    
#%% FUNCION:
def f_columnas_pips(param_data):
    param_data['pips'] = np.zeros(len(param_data['type']))
    for i in range(0,len(param_data['type'])):
        if param_data['type'][i] == 'buy':
            param_data['pips'][i] = (param_data.closeprice[i] - param_data.openprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
        else:
            param_data['pips'][i] = (param_data.openprice[i] - param_data.closeprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
    
    param_data['pips_acm'] = np.zeros(len(param_data['type']))
    param_data['profit_acm'] = np.zeros(len(param_data['type']))    
    param_data['pips_acm'][0] = param_data['pips'][0]
    param_data['profit_acm'][0] = param_data['profit'][0]
            
    for i in range(1,len(param_data['pips'])):
         param_data['pips_acm'][i] = param_data['pips_acm'][i-1] + param_data['pips'][i]
         param_data['profit_acm'][i] = param_data['profit_acm'][i-1] + param_data['profit'][i]
        
    return param_data
    

    
#%% FUNCION:
def f_estadisticas_ba(param_data):
    
    medida = ['Ops totales', 'Ganadoras', 'Ganadoras_c', 'Ganadoras_v', 'Perdedoras', 'Perdedoras_c', 'Perdedoras_v', 
              'Media(profit)','Media(pips)', 'r_efectividad', 'r_proporcion', 'r_efectividad_c','r_efectividad_v']
    descripcion = ['Operaciones Totales', 'Operaciones Ganadoras', 'Operaciones Ganadoras de Compra', 'Operaciones Ganadoras de Venta',
                   'Operaciones Perdedoras', 'Operaciones Perdedoras de Compra', 'Operaciones Perdedoras de Venta', 'Mediana de Profit de Operaciones', 
                   'Media de Pips de Operaciones', 'Ganadoras Totales / Operaciones Totales', 'Perdedoras Totales / Ganadoras Totales',
                   'Ganadoras Compras / Operaciones Totales', 'Ganadoras Ventas / Operaciones Totales']
   
    zero_data = np.zeros(shape=(len(descripcion),3))
    df_1_tabla = pd.DataFrame(zero_data, columns = ['medida', 'valor', 'descripcion'])
    
    df_1_tabla['valor'][0] = len(param_data['profit'])
    df_1_tabla['valor'][1] = param_data['profit'].gt(0).sum()
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'buy' and param_data['profit'][i] > 0 :
            x = x+1
    df_1_tabla['valor'][2] = x
    
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'sell' and param_data['profit'][i] > 0 :
            x = x+1
    df_1_tabla['valor'][3] = x
    df_1_tabla['valor'][4] = df_1_tabla['valor'][0] - df_1_tabla['valor'][1]
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'buy' and param_data['profit'][i] < 0 :
            x = x+1
    df_1_tabla['valor'][5] = x
    
    x = 0
    for i in range(0,len(param_data['type'])): 
        if param_data['type'][i] == 'sell' and param_data['profit'][i] < 0 :
            x = x+1
    df_1_tabla['valor'][6] = x
    df_1_tabla['valor'][7] = param_data.profit.median()
    df_1_tabla['valor'][8] = param_data.pips.median()
    df_1_tabla['valor'][9] = df_1_tabla['valor'][0] / df_1_tabla['valor'][1]
    df_1_tabla['valor'][10] = df_1_tabla['valor'][1] / df_1_tabla['valor'][4]
    df_1_tabla['valor'][11] = df_1_tabla['valor'][0] / df_1_tabla['valor'][2] 
    df_1_tabla['valor'][12] = df_1_tabla['valor'][0] / df_1_tabla['valor'][3] 
    
    for i in range(0,len(medida)):
        df_1_tabla['medida'][i] = medida[i]
        df_1_tabla['descripcion'][i] = descripcion[i]
    
    #%%
    symbols = param_data["symbol"].unique().tolist()
    zero_data = np.zeros(shape=(len(symbols),2))
    df_1_ranking = pd.DataFrame(zero_data, columns = ['Symbol', 'Rank'])
     
    for i in range (0,len(symbols)):
        df_1_ranking['Symbol'][i] = symbols[i]
        
    for i in range (0,len(df_1_ranking["Symbol"])):
        ganadoras = 0
        totales = 0
        for j in range (0,len(param_data["symbol"])):
            if df_1_ranking["Symbol"][i] == param_data["symbol"][j]:
                totales = totales + 1 
                if param_data['profit'][j] > 0:
                    ganadoras = ganadoras+1
                
        df_1_ranking['Rank'][i] = ganadoras/totales
    
    diccionario = {"df_1_ranking":df_1_ranking ,"df_1_tabla":df_1_tabla}
        
    return diccionario


        
#%% FUNCIÓN:

def f_columnas_capital_acum(param_data):
    param_data['capital_acm'] = np.zeros(len(param_data['type']))
    param_data['capital_acm'][0] = 5000+param_data['profit'][0]
            
    for i in range(1,len(param_data['pips'])):
         param_data['capital_acm'][i] = param_data['capital_acm'][i-1] + param_data['profit'][i]

    return param_data  

#%%
    
def f_profit_diario(param_data):
    
    sdate = param_data["closetime"][0].date()   # start date
    edate = param_data["closetime"][len(param_data["closetime"])-1].date()  # end date

    delta = edate - sdate       # as timedelta
    
    zero_data = np.zeros(shape=(delta.days+1,4))
    df_profit_d = pd.DataFrame(zero_data, columns = ['Fecha','Profit Diario',
                                                     'Capital Acumulado', 'Rend Log'])
    df_profit_d_c = pd.DataFrame(zero_data, columns = ['Fecha','Profit Diario',
                                                     'Capital Acumulado', 'Rend Log'])
    df_profit_d_v = pd.DataFrame(zero_data, columns = ['Fecha','Profit Diario',
                                                     'Capital Acumulado', 'Rend Log'])
    
    
    for i in range(0,delta.days+1):
        df_profit_d["Fecha"][i]= sdate + timedelta(days=i)
        df_profit_d_c["Fecha"][i]= sdate + timedelta(days=i)
        df_profit_d_v["Fecha"][i]= sdate + timedelta(days=i)
        
        
    for i in range (0,len(df_profit_d["Fecha"])):
        a = 0
        b = 0
        c = 0
        
        for j in range (0,len(param_data["closetime"])):
            if df_profit_d["Fecha"][i] == param_data["closetime"][j].date():
                a = a + param_data["profit"][j]
                
                if param_data['type'][j] == 'buy':
                    b = b + param_data["profit"][j]
                    
                elif param_data['type'][j] == 'sell':
                    c = c + param_data["profit"][j]
                
                
        df_profit_d["Profit Diario"][i] = a
        df_profit_d_c["Profit Diario"][i] = b
        df_profit_d_v["Profit Diario"][i] = c
        
    df_profit_d = df_profit_d.sort_values(by=['Fecha'])
    df_profit_d = df_profit_d.reset_index(drop=True)
    
    df_profit_d_c = df_profit_d_c.sort_values(by=['Fecha'])
    df_profit_d_c = df_profit_d_c.reset_index(drop=True)
    
    df_profit_d_v = df_profit_d_v.sort_values(by=['Fecha'])
    df_profit_d_v = df_profit_d_v.reset_index(drop=True)
    
    df_profit_d['Capital Acumulado'][0] = 5000+df_profit_d['Profit Diario'][0]
    df_profit_d['Rend Log'][0] = np.log(df_profit_d['Capital Acumulado'][0]/5000)
    
    df_profit_d_c['Capital Acumulado'][0] = 5000+df_profit_d_c['Profit Diario'][0]
    df_profit_d_c['Rend Log'][0] = np.log(df_profit_d_c['Capital Acumulado'][0]/5000)
    
    df_profit_d_v['Capital Acumulado'][0] = 5000+df_profit_d_v['Profit Diario'][0]
    df_profit_d_v['Rend Log'][0] = np.log(df_profit_d_v['Capital Acumulado'][0]/5000)
            
    for i in range(1,len(df_profit_d["Profit Diario"])):
         df_profit_d['Capital Acumulado'][i] = df_profit_d['Capital Acumulado'][i-1] + df_profit_d['Profit Diario'][i]
         df_profit_d['Rend Log'][i] = np.log(df_profit_d['Capital Acumulado'][i]/df_profit_d['Capital Acumulado'][i-1])
         
         df_profit_d_c['Capital Acumulado'][i] = df_profit_d_c['Capital Acumulado'][i-1] + df_profit_d_c['Profit Diario'][i]
         df_profit_d_c['Rend Log'][i] = np.log(df_profit_d_c['Capital Acumulado'][i]/df_profit_d_c['Capital Acumulado'][i-1])
         
         df_profit_d_v['Capital Acumulado'][i] = df_profit_d_v['Capital Acumulado'][i-1] + df_profit_d_v['Profit Diario'][i]
         df_profit_d_v['Rend Log'][i] = np.log(df_profit_d_v['Capital Acumulado'][i]/df_profit_d_v['Capital Acumulado'][i-1])
         
    n = 0
    cont = 0
     
    while n != 5:
        n = df_profit_d["Fecha"][cont].weekday()
        cont = cont + 1
    
    for i in range (cont-1,len(df_profit_d["Fecha"]+1),6):
        df_profit_d = df_profit_d.drop(df_profit_d.index[i])
        df_profit_d_c = df_profit_d_c.drop(df_profit_d_c.index[i])
        df_profit_d_v = df_profit_d_v.drop(df_profit_d_v.index[i])
         
         
                  
    diccionario = {"df":df_profit_d ,"df_c":df_profit_d_c,"df_v":df_profit_d_v}
        
    return diccionario     
            


#%%
def f_estadisticas_mad(param_data,param_data1,param_data2):
    rf = .08/300
    mar = .30/300
    metrica = ['sharpe', 'sortino_c','sortino_v','drawdown_capi',
               'drawup_capi','information_r']
    descripcion = ['Sharpe Ratio', 'Sortino Ratio para Posiciones de Compra',
                   'Sortino Ratio para Posiciones de Venta','DrawUp de Capital',
                   'DrawDown de Capital','Information Ratio']
   
    zero_data = np.zeros(shape=(len(descripcion),3))
    df_estadisticas = pd.DataFrame(zero_data, columns = ['metrica', 'valor', 'descripcion'])
    
    for i in range(0,len(metrica)):
        df_estadisticas['metrica'][i] = metrica[i]
        df_estadisticas['descripcion'][i] = descripcion[i]

    df_estadisticas['valor'][0] = (param_data['Rend Log'].mean()-rf)/ param_data['Rend Log'].std()
    df_estadisticas['valor'][1] = (param_data['Rend Log'].mean()-mar)/param_data1['Rend Log'].lt(0).std()
    df_estadisticas['valor'][2] = (param_data['Rend Log'].mean()-mar)/param_data2['Rend Log'].lt(0).std()
    df_estadisticas['valor'][3] = 0
    df_estadisticas['valor'][4] = 0
    df_estadisticas['valor'][5] = 0
    

    
    return df_estadisticas 
    
