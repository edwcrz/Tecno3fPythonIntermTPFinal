from app.views.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.views.product_payment_schema import ProductPaymentCreate, ProductPaymentUpdate, ProductPaymentResponse
from app.views.payment_method_schema import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse
from app.views.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from app.views.customer_address_schema import CustomerAddressCreate, CustomerAddressUpdate, CustomerAddressResponse
from app.views.orders_schema import OrderCreate, OrderUpdate, OrderResponse
from app.views.order_detail_schema import OrderDetailCreate, OrderDetailUpdate, OrderDetailResponse

__all__ = [
    "ProductCreate","ProductUpdate", "ProductResponse",
    "ProductPaymentCreate","ProductPaymentUpdate","ProductPaymentResponse",
    "PaymentMethodCreate","PaymentMethodUpdate","PaymentMethodResponse",
    "CustomerCreate","CustomerUpdate","CustomerResponse",
    "CustomerAddressCreate","CustomerAddressUpdate","CustomerAddressResponse",
    "OrderCreate","OrderUpdate","OrderResponse",
    "OrderDetailCreate","OrderDetailUpdate","OrderDetailResponse"]