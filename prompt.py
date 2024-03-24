# prompt.py

prompt = """
Devuelve un documento JSON con datos. Sólo devuelve JSON, no otro texto. Actúa como un experto en seguridad vial y tránsito, tu objetivo es hacer un inventario vial describiendo los siguientes campos:  \"Latitud\" (Donde el formato tendrá esta forma:  S20 59.5334),  \"Longitud\" (Donde el formato tendrá esta forma: W68 50.5161), \"Altitud\", \"Velocidad\", \"Fecha\", \"Señalización vial\": donde se describa en detalle los símbolos viales que se observan al costado del camino (Si el símbolo vial esta lejano, más alla de 5 metros no lo describas), \"Eventos en ruta\": Donde se describa en detalle y paso a paso cualquier acontecimiento anormal dentro del camino, incluye en esta descripcíon una explicación de porque estaría ocurriendo el evento en particular (personas trabajando por reparación del camino debido a puente roto, vehículo detenido por choque en la carretera, animales en la ruta por cruce de ganadero por el camino, etc), \"Estado del camino\": Describe en detalle paso a paso el estado del camino por donde transita el vehículo utiliza  (como presencia pavimento, hoyos en el camino, calamina, carpeta rodada, piedras sueltas, irregularidades, etc), \"Tipo de superficie\": Donde señalaras si es camino de ripio, de tierra, asfalto etc., \"Descripción del entorno\": Donde tendrás que describir estructuras hechas por el hombre en el entorno por donde transita el vehículo (Por ejemplo, una caseta de madera abandonada a la izquierda, un pozo en buen estado a la derecha, una torre de alta tensión al fondo, etc) y finalmente el campo \"Curvas\": Donde señalaras si el camino es recto, si tiene curvas cerradas, si tiene curvas abiertas, si tiene curvas en S, etc. Si no hubiese información en los campos que te he descrito  simplemente escribe \"No se observa\").  No agregues campos adicionales a los que te he señalado

Por ejemplo espero que el documento JSON obtenido tenga la siguiente forma:
{
    "Latitud": "S20 59.0798",
    "Longitud": "W68 50.8467",
    "Altitud": "4335 M",
    "Velocidad": "44 km/h",
    "Fecha": "2024/01/21 13:53:40",
    "Se\u00f1alizaci\u00f3n vial": "Se\u00f1al de advertencia de curva hacia la derecha",
    "Eventos en ruta": "No se observa",
    "Estado del camino": "Camino de grava sin pavimentar, con presencia de piedras sueltas y algunas irregularidades",
    "Tipo de superficie": "Camino de ripio",
    "Descripci\u00f3n del entorno": "Torre de alta tensi\u00f3n visible, terreno monta\u00f1oso y despejado, sin estructuras adicionales",
    "Curvas": "Curva hacia la derecha visible"
}

O
{
    "Latitud": "S20 58.8237",
    "Longitud": "W68 51.0752",
    "Altitud": "4309 M",
    "Velocidad": "43 km/h",
    "Fecha": "2024/01/21 13:54:34",
    "Se\u00f1alizaci\u00f3n vial": "No se observa",
    "Eventos en ruta": "No se observa",
    "Estado del camino": "Camino amplio, sin pavimentar, con presencia de piedras sueltas y ligeramente irregular.",
    "Tipo de superficie": "Camino de ripio",
    "Descripci\u00f3n del entorno": "Presencia de barandas de concreto a ambos lados del camino, torres de alta tensi\u00f3n a lo lejos, terreno des\u00e9rtico y monta\u00f1oso.",
    "Curvas": "Camino recto con ligera curvatura"
}

"""