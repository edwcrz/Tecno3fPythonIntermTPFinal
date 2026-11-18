
##### This file contains the documentation for the models used in the application. 
##### Each model represents a specific entity in the system and defines its attributes, relationships, and behaviors.
##### Los archivos de la carpeta models van a ser los encargados de la persistencia y la lógica del sql
##### interactua de manera directa con nuestra base de datos
##### va a tener la persistencia de la lógica del sql
##### contiene el código sql
##### es el encargado de hacer las consultas y modificar las tablas

##### en el orden de trabajo models va segundo, antes de controllers y routes

##### va a tener un archivo nombre_tabla.py

###### static method to get all customers from the database, it will be used in the GET /customers endpoint
###### static method no necesita una instancia de la clase para ser llamado, se puede llamar directamente desde la clase, no necesita self ni cls
###### static method es una funcion que:
######   pertenece a la clase, no a la instancia de la clase, 
######   se puede llamar directamente desde la clase, 
######   no necesita self ni cls
###### no necesitamos instanciar, necesitamos mantener una conexción con la base de datos abierta, 
###### para eso vamos a pasarle la conexion a la base de datos como parametro, para que no se cierre la conexion y 
###### podamos seguir usando la misma conexion en otros metodos
    
###### con esto traemos todo lo que esta en customer modelo, 
###### y lo devolvemos como una lista de diccionarios, 
###### para que sea mas facil de usar en el endpoint GET /customers

###### para prevenir sql injection, vamos a usar parametros en la consulta,
###### en lugar de concatenar strings, vamos a usar ? como placeholder,
###### y luego pasar los valores como una tupla en el segundo parametro del execute,
###### esto es para que sqlite3 haga el escape de los valores, y no se pueda inyectar codigo malicioso en la consulta,
###### si no hacemos esto, un usuario malicioso podria enviar un valor como "1; DROP TABLE product;" y borrar la tabla product de la base de datos,
###### para prevenir sql injection, vamos a usar parametros en la consulta,

###### borrado físico en la base de datos, no es recomendable, porque se pierde la información,
###### es mejor hacer un borrado lógico, cambiando el estado del cliente a inactivo
###### solo borrar un cliente que no tenga ordenes asociadas, para eso vamos a hacer una consulta a la tabla orders,