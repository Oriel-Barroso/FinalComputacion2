# Final Computación 2

## Cómo utilizar la aplicación

    Para correr la aplicación debemos correr los siguientes archivos:

```
python seteoDatos.py -id [NOMBRE DE USUARIO] -ip [PROTOCOLO DE IP (4/6)] -i [HOST] -ps [PUERTO] -t [PROTOCOLO. TCP/UDP] -thp [MÉTODO DE PROCESAMIENTO. THREAD/PROCESSING]
```

        Todos los argumentos son guardados en redis excepto el método de procesamiento, ya que en el cliente no es necesario.
        Luego, tanto en el cliente como en el servidor: solo nos 'logueamos' (en el cliente/servidor, fallara la ejecución en caso de que el usuario no exista, abortando la ejecución):

```
python server.py -id [NOMBRE DE USUARIO]
```
```
python cliente.py -id [NOMBRE DE USUARIO]
```
        Se cargarán los argumentos del servidor en el cliente, se nos pedirá el tamaño de la matriz y el tipo de ejecucion (hilos/procesos) una cantidad infinita de veces. Podemos salir del bucle con CTRL+C

**NOTA: Necesitamos correr si o si primero el archivo seteoDatos.py, independientemente del protocolo. Ya que este guarda un argumento clave, que es el protocolo, y como es sabido, cuando utilizamos el protocolo UDP no es necesario tener el servidor arriba para conectarnos, pero en esta arquitectura propuesta (ver doc/doc_ Propósito y Arquitectura) si hacemos conexión con el cliente y queremos hacer uso del protocolo UDP, puede que en nuestra base de datos tengamos guardado el protocolo TCP como argumento, haciendo que nunca podamos comunicarnos con UDP. Por lo tanto, reitero, es necesario correr primero el archivo seteoDatos.py**