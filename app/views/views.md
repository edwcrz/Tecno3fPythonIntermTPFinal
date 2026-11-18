##### son las vistas
##### al ser una api rest no se cuenta con una interface gráfica
##### la vista se encarga de la estructura del JSON
##### Es la forma en que se arma el JSON con los datos
##### se va a usar pydantic para definir los campos que van a entrar, que van a salir y las reglas que van a cumplir cada tipo de datos
##### va a tener los esquemas de validación de datos que son las vista que van a servir los JSON



##### en el orden de trabajo views va primero, frente a models, controllers y routes

##### por cada tabla armo un archivo nombretabla_schema.py
##### armo un archivo __init__.py

##### basemodel es lo que va a heredar el modelo de producto, es la base para crear otros modelos
##### es para que hereden todos los que van a armar los contratos con JSON, 
##### es lo que va a validar los datos de entrada y salida

##### field es una funcion que sirve para definir los campos del modelo, se puede usar para definir el tipo de dato, el valor por defecto, el ejemplo, etc.
##### sirve para aplicar reglas de validacion a los campos del modelo, como por ejemplo, que un campo sea obligatorio, que tenga un valor por defecto, 
##### que tenga un ejemplo, etc.

##### la base va tener la creación, la ediciòn y la respuesta de los productos, 
##### es la base para crear otros modelos, es para que hereden todos los que van a armar los contratos con JSON,

##### ejemplo
##### name: str = Field(..., example="Product Name")
##### la regla es lo que esta adentro del field, el tipo de dato es lo que esta adentro del str, int, float, etc.
##### los ... es un dato obligatorio, si no se pone el ... el campo es opcional, y si se pone el ... el campo es obligatorio
##### min max es la cantidad de caracteres que puede tener el campo, si no se pone el min y max, el campo puede tener cualquier cantidad de caracteres
