# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 20:41:07 2020

@author: juanm
"""
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py
# -- mantiene: Juan Manuel ACC
# -- repositorio: https://github.com/juanmaalv/LAB_2_JMACC
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd

#%% Función leer archivo

def f_leer_archivo(param_archivo):
    """""
    Parameters
    ----------------
    param_arhivo : str : nombre de archivo a leer

    Returns
    ---------
    df_data : pd.DataFrame: con informacion contenida en archivo leido

    Debugging
    -----------
    para_archivo = 'archivo_tradeview_1.xlsx'

    """
    #leer archivo y guardarlo en un dataframe

    df_data = pd.read_excel(param_archivo, sheet_name='Hoja1')

    #convertir en minusculas el nmbre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]


    #asegurar que ciertas columnas son del tipo numerico

    #cambiar tupo de dato en columnas a numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
               'taxes', 'order']

    df_data[numcols]= df_data[numcols].apply(pd.to_numeric)
    
    return df_data


def f_pip_size(param_ins):

    """""
    Parameters
    ----------------
    param_arhivo : str : nombre de archivo a leer

    Returns
    ---------
    df_data : pd.DataFrame: con informacion contenida en archivo leido

    Debugging
    -----------
    para_archivo = 'archivo_tradeview_1.xlsx'

    """
    
    inst = param_ins.lower()
    
    pips_inst = {'audusd':10000 , 'usdmxn':10000}
    
    return pips_inst

    

    
    
    
    