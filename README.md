# vision_setram

# Descripción General del Repositorio
Este repositorio contiene un proyecto innovador diseñado para realizar inventarios viales mediante el análisis de videos. El proyecto se divide en dos módulos principales: captura de imágenes y análisis de visión por computadora. Utilizando tecnologías avanzadas como la biblioteca de OpenAI, este sistema automatiza la detección y clasificación de señales de tráfico, hallazgos en el camino, y otros elementos relevantes para la gestión y el mantenimiento de infraestructuras viales.
Módulo de Captura de Imágenes
El primer módulo se enfoca en la captura de imágenes directamente desde videos. Mediante una interfaz intuitiva, el usuario puede cargar videos de recorridos viales y, con la ayuda de controles simples, capturar screenshots específicos de señales en el camino y otros hallazgos de interés. Estas imágenes son preparadas para su posterior análisis en el módulo de visión.
Módulo de Análisis de Visión
Utilizando la librería de OpenAI, este módulo procesa las imágenes capturadas para identificar y clasificar elementos visuales relevantes. La entrada a este sistema es un prompt especializado que guía el análisis, asegurando que los resultados se alineen con las necesidades específicas del inventario vial. La salida de este módulo es un archivo Excel detallado que sirve como tabla de inventario, organizando la información recopilada en columnas predefinidas para fácil referencia y análisis.
Objetivo del Proyecto
El objetivo de este proyecto es proporcionar una herramienta automatizada para la realización de inventarios viales, reduciendo el tiempo y el esfuerzo requerido para la recopilación de datos en terreno. Al integrar capacidades de visión por computadora y análisis inteligente, el sistema ofrece un método eficiente y preciso para la identificación de señales de tráfico, condiciones de la carretera, y otros elementos críticos para la gestión de infraestructuras viales.
Cómo Utilizar Este Repositorio
Este repositorio está diseñado para ser accesible tanto para usuarios técnicos como para aquellos con menos experiencia en programación. Las instrucciones detalladas de instalación y ejecución, proporcionadas a continuación, guían al usuario a través de cada paso del proceso, desde la configuración del entorno hasta la ejecución de los módulos de captura y análisis.


Instalación y Ejecución
Antes de comenzar, asegúrate de tener instalado Conda en tu sistema. Conda es un sistema de gestión de paquetes y entornos que nos permite instalar, correr, y actualizar paquetes y sus dependencias de manera fácil. Es ampliamente usado en la comunidad científica y de desarrollo por su flexibilidad y capacidad de manejar múltiples entornos de desarrollo de manera aislada.
1. Instalar Conda
Si aún no tienes Conda, visita la página oficial de Miniconda y sigue las instrucciones para tu sistema operativo. Miniconda es una versión más ligera de Anaconda que incluye solo conda, Python, y los paquetes a los que dependen.
2. Instalar Python
Aunque Conda ya instalará Python por nosotros, es crucial que verifiques la instalación ejecutando:
conda –version
Y luego, para verificar la instalación de Python:
python –version
Esto asegurará que tanto Conda como Python estén correctamente instalados en tu sistema.
3. Descargar VLC
VLC es un reproductor multimedia libre y de código abierto que soporta la mayoría de archivos multimedia, así como DVDs, CDs de audio, VCDs, y varios protocolos de streaming. Para este proyecto, necesitarás VLC para manejar tareas relacionadas con multimedia. Puedes descargar VLC desde su página oficial.
4. Crear Ambientes Conda
Vamos a crear dos ambientes conda separados para organizar mejor las dependencias del proyecto:
•	Ambiente VLC: Dedicado a las tareas de manejo de multimedia.
•	Ambiente VISION: Dedicado al procesamiento de datos y visión por computadora.
Para crear estos ambientes, ejecuta los siguientes comandos en tu terminal:
conda create --name VLC_env python=3.8
conda create --name VISION_env python=3.8
Estos comandos crearán dos nuevos ambientes, ambos basados en Python 3.8. Puedes ajustar la versión de Python según tus necesidades o las del proyecto.
5. Instalar python-vlc en el Ambiente VLC
Activa el ambiente VLC y luego instala python-vlc:
conda activate VLC
pip install python-vlc
Esta librería te permitirá interactuar con el reproductor VLC desde scripts de Python.
6. Ejecutar el archivo app_vlc.py
Asegúrate de que estás en el directorio correcto y que el ambiente VLC está activo. Luego, ejecuta:
python app_vlc.py
Al ejecutar este comando, se abrirá una ventana de aplicación con una interfaz de usuario que contiene tres botones principales. Esta ventana es crucial para la carga y análisis de videos mediante capturas de pantalla específicas.
6.1. Interacción con la Interfaz
1.	Cargar Video: El primer botón te permite cargar el video que deseas analizar. Haz clic en él y selecciona el archivo de video desde tu sistema de archivos. Este video será el que utilices para extraer capturas de pantalla para el análisis.
2.	Sacar Screenshots - Señales en el Camino: Una vez cargado el video, puedes utilizar el segundo botón para capturar screenshots específicos donde se muestren señales en el camino. Estas capturas son importantes para el análisis de señalizaciones viales. Ve presionando este botón en los momentos del video que consideres relevantes.
3.	Sacar Screenshots - Hallazgos en el Camino: De manera similar, el tercer botón te permite capturar momentos del video que contengan hallazgos de interés en el camino, como pueden ser objetos inusuales, condiciones de la carretera, entre otros. Estas capturas también serán analizadas posteriormente.
6.2. Proceso de Captura
•	Reproducción del Video: Utiliza los controles de reproducción de VLC integrados en la ventana para pausar, adelantar o retroceder el video según necesites para capturar los momentos precisos.
•	Captura de Imágenes: Cada vez que presiones los botones de captura, el sistema guarda una imagen del frame actual del video. Estas imágenes son almacenadas en una ubicación predefinida que luego será utilizada por el módulo de visión para su análisis.
Las imágenes capturadas durante este paso serán automáticamente pasadas al módulo de visión para ser analizadas en los pasos siguientes. Asegúrate de realizar las capturas que consideres necesarias para el análisis antes de proceder a desactivar el ambiente VLC y activar el ambiente VISION.
7. Cambiar al Ambiente VISION
Para cambiar entre ambientes, primero desactiva el ambiente actual y luego activa el nuevo:
conda deactivate
conda activate VISION
8. Instalar Dependencias en el Ambiente VISION
Ahora, instala las dependencias necesarias en el ambiente VISION:
pip install openai==0.28 pandas python-dotenv xlswriter
Estas librerías son esenciales para el procesamiento de datos, interactuar con la API de OpenAI, manejar variables de entorno, y escribir archivos Excel, respectivamente.
9. Ejecutar el archivo vision_v2.py
Finalmente, con todas las dependencias instaladas y el ambiente VISION activo, ejecuta:
python vision_v2.py
Este script realizará las tareas de procesamiento de datos y visión por computadora que tu proyecto requiere.

