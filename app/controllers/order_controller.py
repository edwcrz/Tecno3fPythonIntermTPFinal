import sqlite3
from fastapi import HTTPException

from app.models.orders_models import OrdersModel
from app.models.order_detail_models import OrderDetailModel

class OrderController:

    # CREAR ORDEN
    @staticmethod
    def create_order(conn, order_data, details):

        try:
            conn.execute("BEGIN")

            # 1. Crear cabecera
            order_id = OrdersModel.create(conn, order_data)

            # 2. Crear detalles
            for detail in details:

                detail_data = {
                    "order_id": order_id,
                    "product_id": detail["product_id"],
                    "quantity": detail["quantity"],
                    "unit_price": detail["unit_price"]
                }

                OrderDetailModel.create(conn, detail_data)

            # 3. Confirmar toda la transacción
            conn.commit()

            return order_id

        except Exception as e:
            conn.rollback()

            if isinstance(e, HTTPException):
                raise

            if isinstance(e, sqlite3.IntegrityError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Error de integridad: {str(e)}"
                )

            raise HTTPException(
                status_code=500,
                detail=f"Error creando orden: {str(e)}"
            )

    # CONSULTAR TODAS LAS ORDENES
    @staticmethod
    def get_all_orders(conn):

        orders = OrdersModel.get_all(conn)

        result = []

        for order in orders:

            order_dict = dict(order)

            details = OrderDetailModel.get_by_order_id(
                conn, order_dict["order_id"]
            )

            order_dict["details"] = [
                dict(detail) for detail in details
            ]

            result.append(order_dict)

        return result

    # CONSULTAR ORDEN POR ID
    @staticmethod
    def get_order_by_id(conn, order_id):

        order = OrdersModel.get_by_id(conn, order_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Orden no encontrada"
            )

        order_dict = dict(order)

        details = OrderDetailModel.get_by_order_id(
            conn, order_id
        )

        order_dict["details"] = [
            dict(detail) for detail in details
        ]

        return order_dict

    # MODIFICAR ORDEN
    @staticmethod
    def update_order(conn, order_id, order_data, details):

        try:
            conn.execute("BEGIN")

            # 1. Verificar existencia
            order = OrdersModel.get_by_id(conn, order_id)

            if not order:
                raise HTTPException(
                    status_code=404,
                    detail="Orden no encontrada"
                )

            # 2. Actualizar cabecera
            OrdersModel.update(conn, order_id, order_data)

            # 3. Eliminar detalles anteriores
            OrderDetailModel.delete_by_order_id(
                conn, order_id
            )

            # 4. Insertar nuevos detalles
            for detail in details:

                detail_data = {
                    "order_id": order_id,
                    "product_id": detail["product_id"],
                    "quantity": detail["quantity"],
                    "unit_price": detail["unit_price"]
                }

                OrderDetailModel.create(conn, detail_data)

            # 5. Confirmar transacción
            conn.commit()

            return True

        except Exception as e:
            conn.rollback()

            if isinstance(e, HTTPException):
                raise

            if isinstance(e, sqlite3.IntegrityError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Error de integridad: {str(e)}"
                )

            raise HTTPException(
                status_code=500,
                detail=f"Error actualizando orden: {str(e)}"
            )

    # ELIMINAR ORDEN
    @staticmethod
    def delete_order(conn, order_id):

        try:
            conn.execute("BEGIN")

            # Eliminar cabecera
            deleted = OrdersModel.delete(conn, order_id)

            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Orden no encontrada"
                )

            # SQLite elimina los detalles por ON DELETE CASCADE
            conn.commit()

            return True

        except Exception as e:
            conn.rollback()

            if isinstance(e, HTTPException):
                raise

            if isinstance(e, sqlite3.IntegrityError):
                raise HTTPException(
                    status_code=409,
                    detail=f"No se puede eliminar la orden: {str(e)}"
                )

            raise HTTPException(
                status_code=500,
                detail=f"Error eliminando orden: {str(e)}"
            )