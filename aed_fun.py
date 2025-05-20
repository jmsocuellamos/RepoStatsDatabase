#Función para generar una tabla de frecuencias sin establecer orden

def tfreq(df, varcol):
  '''
  Función para generar una tabla de frecuencias sin establecer orden

  Parámetros de entrada:
    - df: data frame
    - varcol: variable de interés sobre la que se desea obtener la tabla
            de frecuencias

  Resultados:
    Tabla de frecuencias con frecuencias absolutas, frecuencias relativas,
    y porcentajes.
  '''
  # Generamos tabla de frecuencias absolutas
  tabla = (df
          .groupby(varcol)
          .agg(Fa = (varcol, "count")) # frecuencia absoluta
          .reset_index())
  # Total de la tabla
  total = sum(tabla.Fa)
  # Frecuencias relativas
  tabla["fr"] = round(tabla["Fa"]/ total, 4)
  # porcentaje por filas
  tabla["Percent"] = round(100*tabla["fr"],2)
  return(tabla)

# Función para generar una tabla de frecuencias con orden preestablecido de
# las categorías

def tfreq_orden(df, varcol, cats_ordered):
  '''
  Función para generar una tabla de frecuencias estableciendo un orden
  para las categorías

  Parámetros de entrada:
    - df: data frame
    - varcol: variable de interés sobre la que se desea obtener la tabla
            de frecuencias
    - cats_ordered: Orden preestablecido de las categorías

  Resultados:
    Tabla de frecuencias con frecuencias absolutas, frecuencias relativas,
    y porcentajes.
  '''
  # Creamos un vector con el número de categorías
  cat_num = list(range(len(cats_ordered)))
  # Recodificamos a etiquetas numéricas
  for i in cat_num:
    df[varcol].replace({cats_ordered[i]: str(cat_num[i])}, inplace = True)
  # obtenemos la tabla de frecuencias
  tabla = tfreq(df, varcol)
  # Volvemos a las etiquetas originales
  for i in cat_num:
    tabla[varcol].replace({str(cat_num[i]): cats_ordered[i]}, inplace = True)
    df[varcol].replace({str(cat_num[i]): cats_ordered[i]}, inplace = True)
  # Devolvemos la tabla
  return(tabla)

# FUNCIONES PARA OBTENER LAS TABLAS DE FRECUENCIAS DE VARIABLES ORDINALES

def tfreq_ordinal(df, varcol):
  '''
  Función para generar una tabla de frecuencias para variables ordinales donde
  las categorías ya están ordenadas.

  Parámetros de entrada:
    - df: data frame
    - varcol: variable de interés sobre la que se desea obtener la tabla
            de frecuencias

  Resultados:
    Tabla de frecuencias con frecuencias absolutas, frecuencias relativas,
    frecuencias acumuladas y porcentajes.
  '''
  # Tabla de frecuencias
  tabla = (df
          .groupby(varcol)
          .agg(Fa = (varcol, "count"))
          .reset_index())
  # Totales
  total = sum(tabla.Fa)
  # Frecuencias relativas
  tabla["fr"] = round(tabla["Fa"]/ total, 4)
  # Porcentajes
  tabla["Percen"] = round(100*tabla["fr"],2)
  # Frecuencia absoluta acumulada
  tabla["Facum"] = tabla["Fa"].cumsum()
  # Frecuencia relativa acumulada
  tabla["facum"] = round(tabla["Facum"]/ total,4)
  # Porcentajes acumulados
  tabla["Percenacum"] = round(100*tabla["facum"],2)
  return(tabla)

def tfreq_ordinal_ord(df, varcol, cats_ordered):
  '''
  Función para generar una tabla de frecuencias para variables ordinales donde
  se establece el orden de als categorías.

  Parámetros de entrada:
    - df: data frame
    - varcol: variable de interés sobre la que se desea obtener la tabla
            de frecuencias
    - cats_ordered: lista con el orden de las categorías que se desea utilizar

  Resultados:
    Tabla de frecuencias con frecuencias absolutas, frecuencias relativas,
    frecuencias acumuladas y porcentajes.
  '''
  # Codificamos según el orden establecido
  cat_num = list(range(len(cats_ordered)))
  for i in cat_num:
    df[varcol] = df[varcol].replace({cats_ordered[i]: str(cat_num[i])})
  tabla = tfreq_ordinal(df, varcol)
  # Volvemos a las etiquetas oroginales
  for i in cat_num:
    tabla[varcol] = tabla[varcol].replace({str(cat_num[i]): cats_ordered[i]})
    df[varcol] = df[varcol].replace({str(cat_num[i]): cats_ordered[i]})
  # Devolvemos la tabla
  return(tabla)

def coeficiente_contigencia(df,v1,v2):
  '''
  Función que nos porporciona el cieficnete de contigencia para dos
  variables de tipo cualitativo.

  Parámetros entrada:
  - df: dataframe de datos
  - v1: primera variable cualitativa
  - v2: segunda variable cualitativa

  Devuelve el valor del coeficiente de contigencia para una tabla
  de contingencia
  '''
  # tabla de contingencia
  tabla = pd.crosstab(df[v1],df[v2],
                       margins=True, margins_name="Total")
  # Importamos la librería que vamos a utilizar
  import scipy.stats as ss
  # Almacenamos los 4 valores en variables diferentes y aplicamos la función chi2_contingency
  chi2_est, p_valor, gl, frec_esperada = ss.chi2_contingency(tabla)
  # Cálculo del coeficiente de contingencia
  n = tabla.sum().sum()
  # Coeficiente de contingencia
  cc = np.sqrt(chi2_est/(chi2_est+n))
  print("Coeficiente de contingencia: ", round(cc,4))
  # Interpretación
  if cc < 0.1:
    print("Asociación débil")
  elif cc <= 0.3:
    print("Asociación moderada")
  else:
    print("Asociación fuerte")

def coeficiente_phi(df,v1,v2):
  '''
  Función que nos porporciona el coeficiente phi para dos
  variables de tipo cualitativo.

  Parámetros entrada:
  - df: dataframe de datos
  - v1: primera variable cualitativa
  - v2: segunda variable cualitativa

  Devuelve el valor del coeficiente de contigencia para una tabla
  de contingencia
  '''
  # tabla de contingencia
  tabla = pd.crosstab(df[v1],df[v2],
                       margins=True, margins_name="Total")
  # Importamos la librería que vamos a utilizar
  import scipy.stats as ss
  # Almacenamos los 4 valores en variables diferentes y aplicamos la función chi2_contingency
  chi2_est, p_valor, gl, frec_esperada = ss.chi2_contingency(tabla)
  # Cálculo del coeficiente phi
  n = tabla.sum().sum()
  # Fórmula para la V de Cramér: raíz cuadrada de chi-cuadrao entre el tamaño de la muestra por el mínimo entre nº de filas - 1, y nº columnas - 1.
  coef_phi = np.sqrt(chi2_est/n)
  print("Coeficiente phi: ", round(coef_phi,4))
  # Interpretación
  if coef_phi < 0.1:
    print("Asociación débil")
  elif coef_phi <= 0.3:
    print("Asociación moderada")
  else:
    print("Asociación fuerte")

def coeficiente_cramer(df,v1,v2):
  '''
  Función que nos porporciona el coeficiente de cramer para dos
  variables de tipo cualitativo.

  Parámetros entrada:
  - df: dataframe de datos
  - v1: primera variable cualitativa
  - v2: segunda variable cualitativa

  Devuelve el valor del coeficiente de contigencia para una tabla
  de contingencia
  '''
  # tabla de contingencia
  tabla = pd.crosstab(df[v1],df[v2],
                       margins=True, margins_name="Total")
  # Importamos la librería que vamos a utilizar
  import scipy.stats as ss
  # Almacenamos los 4 valores en variables diferentes y aplicamos la función chi2_contingency
  chi2_est, p_valor, gl, frec_esperada = ss.chi2_contingency(tabla)
  # Cálculo del coeficiente cramer
  ncol,nrow = tabla.shape
  n = tabla.sum().sum()
  # Fórmula para la V de Cramér: raíz cuadrada de chi-cuadrao entre el tamaño de la muestra por el mínimo entre nº de filas - 1, y nº columnas - 1.
  coef_cramer = np.sqrt(chi2_est/n*min(ncol-1, nrow-1))
  print("Coeficiente phi: ", round(coef_cramer,4))
  # Interpretación
  if coef_cramer < 0.2:
    print("Asociación débil")
  elif coef_cramer <= 0.6:
    print("Asociación moderada")
  else:
    print("Asociación fuerte")
