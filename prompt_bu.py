# prompt.py

prompt = """
Devuelve un documento JSON con datos despues de analizar la imagen. Sólo devuelve JSON, no otro texto. Actúa como un experto en seguridad vial y tránsito, tu objetivo es hacer un inventario vial describiendo los siguientes campos:  



{
  "Latitud": "Donde el formato tendrá esta forma:  S20 59.5334",
  "Longitud": "Donde el formato tendrá esta forma: W68 50.5161",
  "Altitud": "VALOR",
  "Velocidad": "VALOR",
  "Fecha": "VALOR",
  "Carpeta de Rodado": [
    "Pavimento de hormigón",
    "Pavimento asfáltico",
    "Granular"
  ],
  "Tipo de Elemento": {
    "columna": "Tipo de Elemento",
    "instrucciones": [
      {
        "elemento": "Sección_Transversal",
        "definicion": "Se puede describir como el perfil que muestra la distribución de los distintos componentes del camino a lo ancho. Como ej, realizar un corte en el camino y ver el número de carriles que tiene una calzada"
      },
      {
        "elemento": "Semáforo",
        "definicion": "Dispositivo de control de tráfico utilizado en las calles y carreteras para regular el movimiento de vehículos y peatones"
      },
      {
        "elemento": "Señalización_Horizontal",
        "definicion": "Marcas viales pintadas sobre la calzada tales como líneas, símbolos, letras u otras indicaciones que se pueden complementan con la señalizacion vertical presente"
      },
      {
        "elemento": "Señalización_Vertical",
        "definicion": "Señales de tráfico que se instalan en postes o paneles a lo largo de las vías, existen de tres tipos; las reglamentarias que en su mayoría poseen en color rojo presente ya sea en toda la señal o parte de ella, la preventiva donde predomina el color amarillo y la informativa que predominan dos colores dependiendo del tipo de cia y ez azul o verde"
      },
      {
        "elemento": "Servicios_Vial",
        "definicion": "Teléfono que esta en la carretera"
      },
      {
        "elemento": "Sistemas_De_Energía_Eléctrica",
        "definicion": "Corresponde a todo tipo de iluminación presente en la calzada y tendido eléctrico"
      },
      {
        "elemento": "Zonas_De_Actividades_Complementarias",
        "definicion": "Áreas designadas o instalaciones situadas junto a las vías de tránsito que están destinadas a proporcionar servicios adicionales a los usuarios de la carretera"
      },
      {
        "elemento": "Acceso",
        "definicion": "Pequeña entrada o salida a una propiedad privada o camino de menor flujo de tránsito"
      },
      {
        "elemento": "Alinamiento_Horizontal",
        "definicion": "Simple giro en la carretera"
      },
      {
        "elemento": "Aliniamiento_Vertical",
        "definicion": "Indica cómo de inclinado se encuentra un camino en subida o bajada"
      },
      {
        "elemento": "Elementos_De_Contención_Peatonal",
        "definicion": "Barreras que impiden a las personas entrar a la carretera se encuentran ubicadas a orilla de camino o intersecciones"
      },
      {
        "elemento": "Elementos_De_Contención_Vial",
        "definicion": "Barreras a un costado del camino para contener y/o redireccionar vehículos sin control"
      },
      {
        "elemento": "Intersección",
        "definicion": "Cruce de caminos"
      },
      {
        "elemento": "Paso_Peatonal",
        "definicion": "Zonas donde se facilita el cruce de personas por la rutas como pasarelas y zonas demarcados"
      },
      {
        "elemento": "Carpeta_De_Rodado",
        "definicion": "Capa superior del pavimento"
      }
    ]
  },
  "Estado Físico": "VALOR",
  "Funcionalidad": "VALOR",
  "Señalización vial": "donde se describa en detalle los símbolos viales que se observan al costado del camino (Si el símbolo vial esta lejano, más allá de 5 metros no lo describas)",
  "Eventos en ruta": "Donde se describa en detalle y paso a paso cualquier acontecimiento anormal dentro del camino, incluye en esta descripción una explicación de por qué estaría ocurriendo el evento en particular (personas trabajando por reparación del camino debido a puente roto, vehículo detenido por choque en la carretera, animales en la ruta por cruce de ganadero por el camino, etc)",
  "Estado del camino": "Describe en detalle paso a paso el estado del camino por donde transita el vehículo utiliza (como presencia pavimento, hoyos en el camino, calamina, carpeta rodada, piedras sueltas, irregularidades, etc)",
  "Descripción del entorno": "Donde tendrás que describir estructuras hechas por el hombre en el entorno por donde transita el vehículo (Por ejemplo, una caseta de madera abandonada a la izquierda, un pozo en buen estado a la derecha, una torre de alta tensión al fondo, etc) y finalmente el campo"
}



Para determinar como asignar un valor a al campo "Tipo de Elemento" sigue las siguientes instrucciones:
La clave "columna" identifica el nombre de la columna que se está definiendo.
La clave "instrucciones" contiene un array de objetos, cada uno representando un tipo de elemento que puede ser ingresado en esa columna. Cada objeto tiene dos claves:
"elemento": el nombre del elemento a ingresar en la columna.
"definicion": la descripción o criterio que, si es identificado por el módulo de visión, resultará en que el respectivo "elemento" sea ingresado en la columna.

Se espera que el campo "Tipo de Elemento" y "Carpeta de Rodado" contengan SOLAMENTE UN ELEMENTO de la lista de instrucciones.


Por ejemplo un formato de salida JSON valido sera de esta forma:
<ejemplo>
{
    "Latitud": "S20 59.0798",
    "Longitud": "W68 50.8467",
    "Altitud": "4335 M",
    "Velocidad": "44 km/h",
    "Fecha": "2024/01/21 13:53:40",
    "Carpeta de Rodado": "Pavimento asf\u00e1ltico",
    "Tipo de Elemento":  "Se\u00f1alizaci\u00f3n_Vertical",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "Se observa una se\u00f1al de tr\u00e1nsito de advertencia, indicando una curva hacia la derecha.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "El camino parece ser de grava compactada con algunas irregularidades y piedras sueltas. No hay presencia de pavimento asf\u00e1ltico o de hormig\u00f3n. Se da la sensaci\u00f3n de conducci\u00f3n fuera de carreteras principales o caminos secundarios.",
    "Descripci\u00f3n del entorno": "Hay presencia de una torre de alta tensi\u00f3n al fondo a la izquierda de la carretera, sin estructuras adicionales visibles en el \u00e1rea inmediata. El entorno es monta\u00f1oso y desolado con escasa vegetaci\u00f3n y sin se\u00f1ales de desarrollo humano significativo a excepci\u00f3n de la carretera y se\u00f1alizaci\u00f3n vial."
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 59.4795",
    "Longitud": "W68 50.5439",
    "Altitud": "4355 m",
    "Velocidad": "36 km/h",
    "Fecha": "2024/01/21 13:52:17",
    "Carpeta de Rodado":  "Pavimento asf\u00e1ltico",
    "Tipo de Elemento": "Acceso",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "Se observa una se\u00f1al de tr\u00e1nsito vertical de color amarillo que indica un aviso de 129 metros, probablemente refiri\u00e9ndose a una condici\u00f3n espec\u00edfica en la carretera a esa distancia.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta en la imagen proporcionada.",
    "Estado del camino": "La carretera tiene una carpeta de rodado de tipo granular, no hay presencia de pavimento y parece estar nivelada sin presencia de hoyos visibles. No hay se\u00f1ales de calaminas, piedras sueltas ni grandes irregularidades en la superficie.",
    "Descripci\u00f3n del entorno": "El entorno muestra una infraestructura de energ\u00eda el\u00e9ctrica con varios postes y l\u00edneas de transmisi\u00f3n distribuidas de manera regular a lo largo del paisaje. No se observan estructuras como casetas o torres diferentes a los postes de energ\u00eda el\u00e9ctrica ni tampoco presencia de agua o pozos visibles."
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 59.0798",
    "Longitud": "W68 50.8467",
    "Altitud": "4335 M",
    "Velocidad": "44 km/h",
    "Fecha": "2024/01/21 13:53:40",
    "Carpeta de Rodado": "Granular",
    "Tipo de Elemento": "Se\u00f1alizaci\u00f3n_Vertical",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "Se observa una se\u00f1al de tr\u00e1fico vertical de advertencia, indicando una curva hacia la derecha.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "El camino parece consistir en una superficie de grava compactada con algunas irregularidades menores y piedras sueltas, sin presencia de pavimento asf\u00e1ltico o de hormig\u00f3n. Es t\u00edpico de un camino secundario o rural en zonas monta\u00f1osas.",
    "Descripci\u00f3n del entorno": "Se aprecia una torre de alta tensi\u00f3n a la izquierda de la carretera, sin otras estructuras visibles significativas. El entorno es predominantemente monta\u00f1oso y \u00e1rido con vegetaci\u00f3n escasa y no hay evidencia de desarrollo urbano o edificaciones cercanas a excepci\u00f3n del sistema de energ\u00eda el\u00e9ctrica y la carretera."
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 58.8237",
    "Longitud": "W68 51.0752",
    "Altitud": "4309 M",
    "Velocidad": "43 km/h",
    "Fecha": "2024/01/21 13:54:34",
    "Carpeta de Rodado": "Granular",
    "Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
    "Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica."
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 59.5076",
    "Longitud": "W68 50.5264",
    "Altitud": "4354 M",
    "Velocidad": "37 km/h",
    "Fecha": "2024/01/21 13:52:11",
    "Carpeta de Rodado": "Granular",
    "Tipo de Elemento": "Se\u00f1alizaci\u00f3n_Vertical",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "Se observa una se\u00f1al de tr\u00e1nsito vertical de advertencia, indicando un zigzag o serie de curvas adelante.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino se encuentra despejado sin presencia de trabajos, veh\u00edculos detenidos, o animales.",
    "Estado del camino": "La calzada parece ser de carpeta de rodado tipo granular, en buenas condiciones y sin se\u00f1ales de deterioro significativo como hoyos o grandes irregularidades.",
    "Descripci\u00f3n del entorno": "El entorno consiste en un paisaje \u00e1rido y monta\u00f1oso con muy poca vegetaci\u00f3n. No hay estructuras hechas por el hombre cerca de la carretera, con excepci\u00f3n de las se\u00f1ales de tr\u00e1nsito y los postes de electricidad visibles a lo largo de la ruta."
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 58.8237",
    "Longitud": "W68 51.0752",
    "Altitud": "4309 M",
    "Velocidad": "43 km/h",
    "Fecha": "2024/01/21 13:54:34",
    "Carpeta de Rodado": "Granular",
    "Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
    "Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica."
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 59.5439",
    "Longitud": "W68 50.5439",
    "Altitud": "4355 M",
    "Velocidad": "36 km/h",
    "Fecha": "2024/01/21 13:52:17",
    "Carpeta de Rodado": "Granular",
    "Tipo de Elemento": "Se\u00f1alizaci\u00f3n_Vertical",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "Se observa una se\u00f1al de tr\u00e1nsito vertical de color amarillo que indica un aviso de 129 metros, probablemente refiri\u00e9ndose a una condici\u00f3n espec\u00edfica en la carretera a esa distancia.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta en la imagen proporcionada.",
    "Estado del camino": "La carretera tiene una carpeta de rodado de tipo granular, no hay presencia de pavimento y parece estar nivelada sin presencia de hoyos visibles. No hay se\u00f1ales de calaminas, piedras sueltas ni grandes irregularidades en la superficie.",
}
</ejemplo>

<ejemplo>
{
    "Latitud": "S20 58.8237",
    "Longitud": "W68 51.0752",
    "Altitud": "4309 M",
    "Velocidad": "43 km/h",
    "Fecha": "2024/01/21 13:54:34",
    "Carpeta de Rodado":  "Pavimento asf\u00e1ltico",
    "Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
    "Estado Fisico": "Cumple",
    "Funcionalidad": "Cumple",
    "Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
    "Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica."
}
</ejemplo>
"""