from pydantic import BaseModel, Field

""""
 basemodel es lo que va a heredar el modelo de producto, es la base para crear otros modelos
 es para que hereden todos los que van a armar los contratos con JSON, 
 es lo que va a validar los datos de entrada y salida
 """

"""
field es una funcion que sirve para definir los campos del modelo, se puede usar para definir el tipo de dato, el valor por defecto, el ejemplo, etc.
sirve para aplicar reglas de validacion a los campos del modelo, como por ejemplo, que un campo sea obligatorio, que tenga un valor por defecto, 
que tenga un ejemplo, etc.
"""

""""
la base va tener la creación, la ediciòn y la respuesta de los productos, 
es la base para crear otros modelos, es para que hereden todos los que van a armar los contratos con JSON,

ejemplo
name: str = Field(..., example="Product Name")
la regla es lo que esta adentro del field, el tipo de dato es lo que esta adentro del str, int, float, etc.
los ... es un dato obligatorio, si no se pone el ... el campo es opcional, y si se pone el ... el campo es obligatorio
min max es la cantidad de caracteres que puede tener el campo, si no se pone el min y max, el campo puede tener cualquier cantidad de caracteres


"""


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Product Name")
    description: str = Field(..., example="Product Description")
    price: float = Field(..., example=9.99)
    quantity: int = Field(..., example=100)

