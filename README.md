# GopherUnderground
Este software consiste en un prototipo de simulación para transporte de minerales en minería panel caving.

Al ser un prototipo, este software fue hecho con el propósito de comprobar el concepto y su potencial. Como resultado, tiene numerosas falencias (requerimiento de la consola de Python para algunas funciones, implementación de la GUI puede ser algo engorrosa, y falta de opciones como la de exportar, guardar y diseñar mallas de paneles).

Futuras modificaciones de este proyecto se harán en un branch privado en lugar de ser expuestas al público.

Funciones de la interface:


File

-Guardar: Guarda un archivo incluyendo los datos de túneles diseñados y simulación

-Limpiar: Limpia el lienzo


Brush size

-1 px.: Cambia el pincel a un tamaño de 1 pixel

-3 px.: Cambia el pincel a un tamaño de 3 pixeles.

-5 px.: Cambia el pincel a un tamaño de 5 pixeles.

-7 px.: Cambia el pincel a un tamaño de 7 pixeles.

-9 px.: Cambia el pincel a un tamaño de 9 pixeles.


Brush color

-Black: Cambia el pincel a un color negro. Representa túneles en el lienzo.

-Green: Cambia el pincel a un color verde. Representa puntos de extracción en el lienzo.

-Blue: Cambia el pincel a un color azul. Representa puntos de descarga en el lienzo.

-White: Cambia el pincel a un color blanco. Permite borrar o separar túneles.


Start Simulation

-Demostración: Hace una demostración entre los últimos puntos de extracción y descarga situados; genera una línea roja entre ambos.

-Crear rutas: Genera las rutas más cortas entre los puntos de extracción y descarga y los muestra (mediante líneas rojas) como paso previo a la 
simulación

-Simulación LHD: Solicita al usuario input de cuantos vehículos quiere usar, y entre cuales puntos de descarga y extracción hacen el ciclo de extracción, para poder generar los cálculos de la simulación y arrojar los gráficos

-Revisar rutas: Permite observar un registro (en la consola de Python) de los vehículos y sus puntos de ciclo.


Panel Builder

-Teniente: Crea un modelo de malla teniente


Charts (nota: los gráficos están vacíos hasta que se genera una simulación)

-Cambiar tiempo de simulación: Permite reducir o aumentar el tiempo de simulación representado en los gráficos

-Prod. Min. Total: Genera un grafico de producción mineral total (toneladas de mineral transportado y depositado) respecto al tiempo de simulación con la suma de todo lo producido por todos los LHD.

-Prod. Min. LHD: Genera un gráfico de producción mineral total (toneladas de mineral transportado y depositado) respecto al tiempo de simulación para cada LHD por separado.

-Prod. Cu Total: Genera un gráfico de producción mineral de cobre (toneladas de cobre transportado y depositado acorde a la ley de los puntos de extracción) respecto al tiempo de simulación con la suma de todo lo producido por todos los LHD

-Prod. Cu LHD: Genera un gráfico de producción mineral total cobre (toneladas de cobre transportado y depositado acorde a la ley de los puntos de extracción) respecto al tiempo de simulación para cada LHD por separado.

-Puntos de extracción: Genera un gráfico de cuanto mineral es extraído en cada punto de extracción respecto al tiempo de simulación

-Combustible: Genera un grafico con el consumo y carga de combustible de cada LHD respecto al tiempo de simulación.


Config.

-LHD Vel. Max.: Permite configurar la velocidad máxima de un LHD

-LHD Acel.: Permite configurar la aceleración máxima de un LHD

-LHD Desacel.: Permite configurar la desaceleración máxima de un LHD

-LHD T. Esp. PE: Permite configurar el tiempo de espera de un LHD en puntos de extracción de mineral.

-LHD T. Esp. PV: Permite configurar el tiempo de espera de un LHD en puntos de vaciado (descarga) de mineral.

-LHD Fuel Max.: Permite configurar la capacidad de combustible máximo de un LHD

-LHD Fuel Dist.: Permite configurar la distancia hacia el cargamento de combustible para un LHD.

-LHD Fuel T. Espera: Permite configurar el tiempo de espera que un LHD tarda para cargar combustible.

-PE Material: Permite definir el mineral total en un punto de extracción.

-PE Ley Cu: Permite definir la ley de cobre en un punto de extracción. 

-Todos los LHD: Cambia una configuración a elección del usuario para todos los LHDs.

-Todos los PE: Cambia una configuración a elección del usuario para todos los puntos de extracción.
