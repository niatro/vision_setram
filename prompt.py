# prompt.py

prompt_r1 = """

Devuelve un documento JSON con datos despues de analizar la imagen. Sólo devuelve JSON, no otro texto. Actúa como un experto en seguridad vial y tránsito, tu objetivo es hacer un inventario vial describiendo los siguientes campos:  


{
  "Latitud": "Donde el formato tendrá esta forma:  S20 59.5334",
  "Longitud": "Donde el formato tendrá esta forma: W68 50.5161",
  "Altitud": "VALOR",
  "Velocidad": "VALOR",
  "Fecha": "VALOR",
  "Carpeta de Rodado": 
  [
    "Pavimento de hormigón",
    "Pavimento asfáltico",
    "Granular"
],
  "Tipo de Elemento": 
  {
    "Sección_Transversal": "Perfil que muestra la distribución de los distintos componentes del camino a lo ancho.",
    "Semáforo": "Dispositivo de control de tráfico para regular el movimiento de vehículos y peatones.",
    "Señalización_Horizontal": "Marcas viales pintadas sobre la calzada como líneas, símbolos, letras.",
    "Señalización_Vertical": "Señales de tráfico instaladas en postes o paneles a lo largo de las vías.",
    "Servicios_Vial": "Teléfono que está en la carretera.",
    "Sistemas_De_Energía_Eléctrica": "Iluminación y tendido eléctrico presentes en la calzada.",
    "Zonas_De_Actividades_Complementarias": "Áreas o instalaciones que proporcionan servicios adicionales en las vías.",
    "Acceso": "Entrada o salida a una propiedad privada o camino de menor flujo de tránsito.",
    "Alinamiento_Horizontal": "Giro en la carretera.",
    "Aliniamiento_Vertical": "Indica la inclinación de un camino en subida o bajada.",
    "Elementos_De_Contención_Peatonal": "Barreras para impedir que personas entren a la carretera.",
    "Elementos_De_Contención_Vial": "Barreras para contener y redireccionar vehículos sin control.",
    "Intersección": "Cruce de caminos.",
    "Paso_Peatonal": "Zonas para el cruce de personas por la ruta."
},
  "Señalización vial": "VALOR",
  "Eventos en ruta": "VALOR",
  "Estado del camino": "VALOR",
  "Descripción del entorno": "VALOR",
}

#Instrucciones
1.- Debes generar un archivo JSON sin estructuras anidadas, es decir, sin objetos dentro de la estructura.
2.- En el campo "Latitud" deberás usar el siguiente formato  S20 59.5334".
3.- En el campo  "Longitud" deberás usar el siguiente formato W68 50.5161".
4.- En el campo  "Altitud" "debera poner un valor numérico en metros (m)".
5.  En el campo "Velocidad" deberas poner un valor numérico en km/h".
6.  En el campo "Fecha" deberás poner un valor en este formato 2024/01/12 11:20:39".
7.- En el campo "Carpeta de Rodado" debes devolver solo un elemento de la lista.
8.- En el campo "Tipo de Elemento" debes devolver solo un elemento del diccionario, asegurate que sea el que esta mejor descrito en la imagen.
9.- En el campo "Señalización vial" debes describir en detalle los símbolos viales que se observan al costado del camino (Si el símbolo vial esta lejano, más allá de 5 metros no lo describas).
10.- En el campo "Eventos en ruta" debes describir en detalle y paso a paso cualquier acontecimiento anormal dentro del camino, incluye en esta descripción una explicación de por qué estaría ocurriendo el evento en particular (personas trabajando por reparación del camino debido a puente roto, vehículo detenido por choque en la carretera, animales en la ruta por cruce de ganadero por el camino, etc).
11.- En el campo "Estado del camino" "Describe en detalle paso a paso el estado del camino por donde transita el vehículo utiliza (como presencia pavimento, hoyos en el camino, calamina, carpeta rodada, piedras sueltas, irregularidades, etc). 
12.- En el campo "Descripción del entorno" debes describir estructuras hechas por el hombre en el entorno por donde transita el vehículo (Por ejemplo, una caseta de madera abandonada a la izquierda, un pozo en buen estado a la derecha, una torre de alta tensión al fondo, etc) y finalmente el campo.


# Ejemplos formatos de salida JSON validos:


<ejemplo>
{
    "Latitud": "S20 59.4795",
    "Longitud": "W68 50.5439",
    "Altitud": "4355 m",
    "Velocidad": "36 km/h",
    "Fecha": "2024/01/21 13:52:17",
    "Carpeta de Rodado":  "Pavimento asf\u00e1ltico",
    "Tipo de Elemento": "Acceso",
    "Se\u00f1alizaci\u00f3n vial": "Se observa una se\u00f1al de tr\u00e1nsito vertical de color amarillo que indica un aviso de 129 metros, probablemente refiri\u00e9ndose a una condici\u00f3n espec\u00edfica en la carretera a esa distancia.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta en la imagen proporcionada.",
    "Estado del camino": "La carretera tiene una carpeta de rodado de tipo granular, no hay presencia de pavimento y parece estar nivelada sin presencia de hoyos visibles. No hay se\u00f1ales de calaminas, piedras sueltas ni grandes irregularidades en la superficie.",
    "Descripci\u00f3n del entorno": "El entorno muestra una infraestructura de energ\u00eda el\u00e9ctrica con varios postes y l\u00edneas de transmisi\u00f3n distribuidas de manera regular a lo largo del paisaje. No se observan estructuras como casetas o torres diferentes a los postes de energ\u00eda el\u00e9ctrica ni tampoco presencia de agua o pozos visibles."
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
    "Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
    "Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica."
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
    "Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
    "Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
    "Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
    "Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica."
}
</ejemplo>

"""


prompt_r2 = """

<Objetivo>
Tu OBJETIVO es devolver un elemento JSON valido, solo devuelve JSON, no otro texto.
Para el siguiente elemento JSON:
{$JSON}
</Objetivo>

<Reglas>
Debes agregar el campo "Estado Físico" al elemento JSON de arriba, basándote en el valor del campo "Tipo de Elemento" y la información obtenida de la imagen.

Te dejo una referencia con la descripción de los distintos valores del "Tipo de Elemento" que puedes encontrar arriba en el JSON:

    "Sección_Transversal": "Perfil que muestra la distribución de los distintos componentes del camino a lo ancho."
    "Semáforo": "Dispositivo de control de tráfico para regular el movimiento de vehículos y peatones."
    "Señalización_Horizontal": "Marcas viales pintadas sobre la calzada como líneas, símbolos, letras."
    "Señalización_Vertical": "Señales de tráfico instaladas en postes o paneles a lo largo de las vías."
    "Servicios_Vial": "Teléfono que está en la carretera."
    "Sistemas_De_Energía_Eléctrica": "Iluminación y tendido eléctrico presentes en la calzada."
    "Zonas_De_Actividades_Complementarias": "Áreas o instalaciones que proporcionan servicios adicionales en las vías."
    "Acceso": "Entrada o salida a una propiedad privada o camino de menor flujo de tránsito.",
    "Alinamiento_Horizontal": "Giro en la carretera."
    "Aliniamiento_Vertical": "Indica la inclinación de un camino en subida o bajada."
    "Elementos_De_Contención_Peatonal": "Barreras para impedir que personas entren a la carretera."
    "Elementos_De_Contención_Vial": "Barreras para contener y redireccionar vehículos sin control."
    "Intersección": "Cruce de caminos."
    "Paso_Peatonal": "Zonas para el cruce de personas por la ruta."



Identifica el valor del campo "Tipo de Elemento".
Analiza la imagen adjunta para obtener información adicional que pueda ayudar a determinar el estado físico del elemento. 


Basándote en el valor del campo "Tipo de Elemento", utiliza los siguientes criterios para determinar si el elemento cumple, no cumple o no aplica de acuerdo con los siguientes criterios:

# Si el "Tipo de Elemento" es "Sección_Transversal", "Semáforo", "Servicios_Vial", "Sistema_De_Energía_Eléctrica", "Zonas_de_Actividades_Complementarias", el estado físico siempre se considera como "No aplica".
# Si el "Tipo de Elemento" es "Acceso", "Alineamiento_Horizontal", "Alineamiento_Vertical", "Elementos_de_Contención_Peatonal" o "Intersección", el estado físico siempre se considera como "Cumple".


# Si el "Tipo de Elemento" es "Señalización_Horizontal", evalúa si cumple con los siguientes criterios:
No presenta desgaste, suciedad, agrietamiento en su pintura y su reflectancia es correcta en condiciones de poca luz. En caso de parches, está repintada sin perder la demarcación horizontal. 
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Si el "Tipo de Elemento" es "Señalización_Vertical", evalúa si cumple con los siguientes criterios:
- Está firmemente sujeta a su estructura de soporte y presenta verticalidad perfecta.
- Su leyenda o símbolo no presenta signos de desgaste y la pintura está en buen estado.
- Tiene reflectancia correcta y se mantiene libre de polución o suciedad. 
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Si el "Tipo de Elemento" es "Elementos_de_Contención_Vial", evalúa si cumple con los siguientes criterios:
- La integridad estructural es sólida, sin deformaciones o roturas que afecten su funcionamiento.
- Está correctamente anclada al suelo. 
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Si el "Tipo de Elemento" es "Paso_Peatonal", evalúa si cumple con los siguientes criterios:
- La superficie se encuentra en buenas condiciones, sin grietas, baches o desgaste que provoquen lesiones o caídas.
- Cuenta con buena accesibilidad (rampas, superficies antideslizantes) y buena demarcación (líneas de detención, zig-zag, advertencia de paso de cebra).
- Tiene una sincronización adecuada en sus semáforos. 
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Agrega un nuevo campo llamado "Estado Físico" al elemento JSON.
Asigna el valor "Cumple", "No cumple" o "No aplica" al campo "Estado Físico" según los criterios evaluados y la información obtenida de la imagen.
Genera un nuevo archivo JSON que incluya el elemento original con el campo "Estado Físico" agregado.
</Reglas>

<Ejemplo>
Ejemplo de JSON de entrada:
{
"Latitud": "S20 58.8237",
"Longitud": "W68 51.0752",
"Altitud": "4309 M",
"Velocidad": "43 km/h",
"Fecha": "2024/01/21 13:54:34",
"Carpeta de Rodado": "Pavimento asf\u00e1ltico",
"Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
"Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
"Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
"Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
"Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica."
}
Ejemplo de JSON de salida:
{
"Latitud": "S20 58.8237",
"Longitud": "W68 51.0752",
"Altitud": "4309 M",
"Velocidad": "43 km/h",
"Fecha": "2024/01/21 13:54:34",
"Carpeta de Rodado": "Pavimento asf\u00e1ltico",
"Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
"Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
"Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
"Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
"Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica.",
"Estado F\u00edsico": "Cumple"
}
</Ejemplo>

"""

prompt_r3 = """

<Objetivo>
Tu OBJETIVO es devolver un elemento JSON valido, solo devuelve JSON, no otro texto.
Para el siguiente elemento JSON:
{$JSON}
</Objetivo>

<Reglas>
Debes agregar el campo "Funcionalidad" al elemento JSON de arriba, basándote en el valor del campo "Tipo de Elemento" y la información obtenida de la imagen.

Te dejo una referencia con la descripción de los distintos valores del "Tipo de Elemento" que puedes encontrar arriba en el JSON:

    "Sección_Transversal": "Perfil que muestra la distribución de los distintos componentes del camino a lo ancho."
    "Semáforo": "Dispositivo de control de tráfico para regular el movimiento de vehículos y peatones."
    "Señalización_Horizontal": "Marcas viales pintadas sobre la calzada como líneas, símbolos, letras."
    "Señalización_Vertical": "Señales de tráfico instaladas en postes o paneles a lo largo de las vías."
    "Servicios_Vial": "Teléfono que está en la carretera."
    "Sistemas_De_Energía_Eléctrica": "Iluminación y tendido eléctrico presentes en la calzada."
    "Zonas_De_Actividades_Complementarias": "Áreas o instalaciones que proporcionan servicios adicionales en las vías."
    "Acceso": "Entrada o salida a una propiedad privada o camino de menor flujo de tránsito.",
    "Alinamiento_Horizontal": "Giro en la carretera."
    "Aliniamiento_Vertical": "Indica la inclinación de un camino en subida o bajada."
    "Elementos_De_Contención_Peatonal": "Barreras para impedir que personas entren a la carretera."
    "Elementos_De_Contención_Vial": "Barreras para contener y redireccionar vehículos sin control."
    "Intersección": "Cruce de caminos."
    "Paso_Peatonal": "Zonas para el cruce de personas por la ruta."

Identifica el valor del campo "Tipo de Elemento".
Analiza la imagen adjunta para obtener información adicional que pueda ayudar a determinar la Funcionalidad del elemento. 


Basándote en el valor del campo "Tipo de Elemento", utiliza los siguientes criterios para determinar si el elemento cumple, no cumple, no aplica o por definir de acuerdo con los siguientes criterios:

# Si el "Tipo de Elemento" es "Sección_Transversal", "Semáforo", "Servicios_Vial", "Zonas_de_Actividades_Complementarias", la funcionalidad siempre se considera como "No aplica".
# Si el "Tipo de Elemento" es "Acceso", "Alineamiento_Horizontal", "Alineamiento_Vertical", "Elementos_de_Contención_Peatonal" o "Intersección", la funcionalidad siempre se considera como "Cumple".

# Si el "Tipo de Elemento" es "Sistema_De_Energía_Eléctrica", evalúa si cumple con los siguientes criterios:
- Existe tendido electrico que cruza el camino y esta señalizado correctamente.
- Existe tendido electrico que no cruza el camino paralelo al mismo, sin o con señalización.
- El tendido electrico no presenta cables sueltos o en mal estado.
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Si el "Tipo de Elemento" es "Señalización_Horizontal", evalúa si cumple con los siguientes criterios:
Asigna siempre "Por definir".

# Si el "Tipo de Elemento" es "Señalización_Vertical", evalúa si cumple con los siguientes criterios:
Asigna siempre "Por definir".

# Si el "Tipo de Elemento" es "Elementos_de_Contención_Vial", evalúa si cumple con los siguientes criterios:
- No tiene daños por impacto de vehículos.
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Si el "Tipo de Elemento" es "Paso_Peatonal", evalúa si cumple con los siguientes criterios:
- La superficie se encuentra en buenas condiciones, sin grietas, baches o desgaste que provoquen lesiones o caídas.
- Cuenta con buena accesibilidad (rampas, superficies antideslizantes) y buena demarcación (líneas de detención, zig-zag, advertencia de paso de cebra).
- Tiene una sincronización adecuada en sus semáforos. 
Si cumple con estos criterios de arriba, asigna "Cumple"; de lo contrario, asigna "No cumple".

# Agrega un nuevo campo llamado "Funcionalidad" al elemento JSON.
Asigna el valor "Cumple", "No cumple", "No aplica"co "Por definir" al campo "Funcionalidad" según los criterios evaluados y la información obtenida de la imagen.
Genera un nuevo archivo JSON que incluya el elemento original con el campo "Funcionalidad" agregado.
</Reglas>


<Ejemplo>

Ejemplo de JSON de entrada:
{
"Latitud": "S20 58.8237",
"Longitud": "W68 51.0752",
"Altitud": "4309 M",
"Velocidad": "43 km/h",
"Fecha": "2024/01/21 13:54:34",
"Carpeta de Rodado": "Pavimento asf\u00e1ltico",
"Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
"Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
"Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
"Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
"Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica.",
"Estado F\u00edsico": "Cumple"
}

Ejemplo de JSON de salida:

{
"Latitud": "S20 58.8237",
"Longitud": "W68 51.0752",
"Altitud": "4309 M",
"Velocidad": "43 km/h",
"Fecha": "2024/01/21 13:54:34",
"Carpeta de Rodado": "Pavimento asf\u00e1ltico",
"Tipo de Elemento": "Elementos_De_Contenci\u00f3n_Vial",
"Se\u00f1alizaci\u00f3n vial": "No se observan s\u00edmbolos viales cercanos dentro de los 5 metros al costado del camino.",
"Eventos en ruta": "No se observan eventos anormales en la ruta; el camino est\u00e1 despejado y no hay presencia de personal de trabajo, veh\u00edculos detenidos, ni animales en la ruta.",
"Estado del camino": "Se observa una carretera con una carpeta de rodado granular, sin pavimento asf\u00e1ltico ni de hormig\u00f3n. Hay algunas irregularidades leves en la superficie y presencia de barreras de contenci\u00f3n a ambos lados del camino.",
"Descripci\u00f3n del entorno": "El entorno comprende un paisaje \u00e1rido con vegetaci\u00f3n escasa, monta\u00f1as en la distancia y presencia de l\u00edneas de transmisi\u00f3n el\u00e9ctrica que siguen un trazado paralelo al camino, lo que sugiere una infraestructura de energ\u00eda el\u00e9ctrica.",
"Estado F\u00edsico": "Cumple",
"Funcionalidad": "Cumple"
}

</Ejemplo>

"""