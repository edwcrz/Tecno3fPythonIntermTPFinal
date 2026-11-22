Entidad	IDs
Métodos de pago	1 Efectivo, 2 Transferencia, 3 QR, 4 Débito (5%), 5 Crédito (10%)
Productos	1 Crumble cookie (stock 20), 2 Lemon pie (5), 3 Torta de chocolate grande (3), 4 Brownie (10, sin precio)
Clientes	1 Ana (completa), 2 Beto (sin email), 3 Carla (sin dirección)
2. Pruebas felices (en /docs, en este orden)
#	Request	Esperado
1	GET /product_payment/product/1/prices	Base 2500. Efectivo, Transferencia y QR: 2500. Débito: 2625. Crédito: 2750
2	POST /order/ con el cuerpo de abajo	201, state: pending, total: 48950. Ítems: 2750 × 3 = 8250, 9900, 30800. delivery_addresses trae la dirección de Ana
3	GET /product/	Cookie: stock 20, reservado 3, available 17. Lemon pie: 5 / 1 / 4. Torta: 3 / 1 / 2
4	POST /order/1/items con {"product_id": 1, "quantity": 2}	201, 4 líneas. GET /order/1 muestra total: 54450 y cookie reservado 5
5	DELETE /order/1/items/4	Vuelve a 3 líneas. total: 48950, cookie reservado 3
6	PATCH /order/1/state con {"state": "confirmed"}	confirmed. GET /product/: cookie stock 17 / reservado 0; Lemon 4 / 0; Torta 2 / 0
7	POST /order/ con Efectivo (abajo), y luego PATCH /order/2/state con {"state": "cancelled"}	Total 5000. Al cancelar, reservado vuelve a 0 y el stock no cambia (cookie 17)
8	POST /product/1/stock con {"quantity": 10}	Cookie stock 27

Cuerpo del paso 2 (crédito, tu ejemplo de 3 cookies + 1 lemon pie + 1 torta grande):

json
{
  "customer_id": 1,
  "payment_method_id": 5,
  "communication": "pedido para cumpleaños",
  "items": [
    {"product_id": 1, "quantity": 3},
    {"product_id": 2, "quantity": 1},
    {"product_id": 3, "quantity": 1}
  ]
}

Cuerpo del paso 7 (efectivo):

json
{ "customer_id": 1, "payment_method_id": 1, "items": [ {"product_id": 1, "quantity": 2} ] }
3. Pruebas de rechazo (cada una tiene que fallar con el código indicado)
#	Request	Esperado
9	POST /order/ con customer_id: 2 (Beto)	409 "no tiene email registrado"
10	POST /order/ con customer_id: 3 (Carla)	409 "no tiene dirección registrada"
11	POST /order/ con customer_id: 999	404 "Cliente 999 no existe"
12	POST /order/ cliente 1, ítem {"product_id": 1, "quantity": 100}	409 "Stock insuficiente… disponible 27"
13	Todo o nada: cliente 1, ítems [{"product_id": 1, "quantity": 1}, {"product_id": 3, "quantity": 50}]	409. Después, GET /product/1 sigue con reservado 0 y GET /order/ no tiene pedido nuevo
14	POST /order/ cliente 1 con product_id: 4 (Brownie)	409 "no tiene precio base cargado"
15	PATCH /order/1/state con {"state": "cancelled"} (ya confirmado)	409 "No se puede pasar de 'confirmed' a 'cancelled'"
16	POST /order/1/items con {"product_id": 1, "quantity": 1} (confirmado)	409 "solo se modifica si está 'pending'"
17	PATCH /order/2/state con {"state": "pending"}	422 (no es un valor permitido)
18	POST /product/ con Crumble cookie / Individual otra vez	409 "Ya existe…"
19	POST /customer/ con "email": "ANA@mail.com"	409 "Ya existe un cliente con ese email"
20	POST /customer/ con "email": "sin-arroba"	422 formato inválido
21	POST /payment_method/ con "overload": 10	422 (tiene que ser fracción, máx. 1)
22	POST /product_payment/ con product_id: 4, payment_method_id: 5, price: 3000	409 "El precio base se carga con un método sin recargo"
23	POST /product_payment/ con product_id: 1, payment_method_id: 1, price: 3000	409 "El producto ya tiene precio base"
24	DELETE /product/1	409 "tiene pedidos asociados"
25	DELETE /customer/1	409 "tiene pedidos"
26	DELETE /payment_method/1	409 (hay precios y pedidos que lo usan)
27	DELETE /product/4 (Brownie, sin pedidos ni reservas)	200, devuelve el producto eliminado

Los números 13, 15 y 24 son los más importantes: validan que no se vende sin stock, que los estados no retroceden y que no se rompe el historial.

4. Cómo leer un fallo
Síntoma	Causa probable
500 con AttributeError	Falta un método en un modelo (por ejemplo exists_name o count_by_customer)
500 con no such column	La base es vieja: borrá pasteleria.db
500 con ResponseValidationError	Un schema no coincide con lo que devuelve el controller (revisá country, available, total)
422 donde esperabas 409	Falló el schema de Pydantic antes de llegar al controller; mirá el campo en el detalle
ConnectionError en seed.py	Backend apagado o puerto distinto
5. Reiniciar de cero

Parás el backend, borrás pasteleria.db, lo levantás de nuevo y corrés python seed.py. Las pruebas 2 a 27 se pueden repetir tal cual, porque los IDs vuelven a ser los mismos.

Cuando pasen todas, seguimos con el frontend: servicios y formularios de las tres pantallas (Productos con precios, Clientes con direcciones y Pedidos con ítems). Si alguna prueba te falla, pegame el error de la terminal y la respuesta de /docs, y lo resolvemos antes de avanzar.