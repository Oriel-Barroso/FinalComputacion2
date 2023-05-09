# Decisiones principales de diseño del sistema

    -Tipo de asincronía: Para lograrla se utilizó la librería threads. Se eligió este tipo de asincronía debido a:
        -Memoria: Los procesos tienen su propio espacio de memoria, por lo que requeriria mas memoria y más procesamiento
        -Comunicación simple: La comunicacion es más simple debido a que los hilos comparten el mismo espacio de memoria
        -Poco procesamiento: Esta aplicación requiere poco procesamiento, por lo que la utilización de procesos sería forzar a utilizar más recursos cuando en realidad no se necesita

    -Almacenamiento: Se utilizó la base de datos 'Redis' para simplificar la ejecución del archivo 'cliente.py'. Esto nos simplifica la tarea de volver a agregar argumentos por terminal

    -Comunicación Cliente/Servidor: Se utilizó **socketserver** debido a que nos permite la conexión de múltiples clientes aportando la utilización de hilos y procesos. Además de aportar modularización con la utilización de clases (MyTCPHandler/MyUDPHandler)
