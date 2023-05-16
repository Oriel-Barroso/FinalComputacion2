# Decisiones principales de diseño del sistema

    -Tipo de asincronía: Para lograrla se utilizó la librería threads y la libreria multiprocessing. 
        Se utilizo estas librerias debido a:
        -Facil uso: Ambas librerias utilizan las mismas funciones, por lo que se hace facil la implementacion
        -Funciones integradas: Las funciones que traen integras ambas librerias son de gran uso y facilitan la escritura de codigo

    -Almacenamiento: Se utilizó la base de datos 'Redis' para simplificar la ejecución del archivo 'cliente.py'. Esto nos simplifica la tarea de volver a agregar argumentos por terminal

    -Comunicación Cliente/Servidor: Se utilizó socketserver debido a que nos permite la conexión de múltiples clientes aportando la utilización de hilos y procesos. Además de aportar modularización con la utilización de clases (MyTCPHandler/MyUDPHandler)
