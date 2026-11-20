
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

###### Una orden nueva se crea en estado pending.
###### Al crearla, se reserva el stock, pero no se descuenta el stock físico.
###### Una orden pendiente puede modificarse o cancelarse.
###### Al confirmar la venta, pasa a sold, se descuenta el stock físico y se libera la reserva.
###### Una orden vendida no se puede modificar ni eliminar mediante las operaciones normales.
###### Se utiliza un único payment_method_id para toda la orden.
###### El precio de cada producto se obtiene de product_payment.price. No se vuelve a aplicar overload, porque ya está incluido en ese precio.
###### La dirección que se guarda es la dirección de entrega de esa orden, no una referencia a la agenda de domicilios del cliente.

###### El Controller va a coordinar las operaciones y las transacciones. Los modelos siguen siendo responsables exclusivamente de ejecutar SQL.

###### Hay dos transacciones comerciales diferentes:
###### Primera transacción: crear la orden
###### pending Se confirma el COMMIT de SQLite
###### Se guarda la orden y queda reservado el stock.

###### Segunda transacción: confirmar la venta
###### sold Se confirma otro COMMIT de SQLite
###### Se descuenta el stock físico, se libera la reserva y se cambia el estado.

###### Esto es importante: el COMMIT de la creación no significa que la orden ya esté vendida. 
###### La orden permanece pendiente hasta que se ejecuta confirm_order().