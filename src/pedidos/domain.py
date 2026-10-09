from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import uuid


class PedidoInvalido(ValueError):
    pass


class EstadoPedido(str, Enum):
    CREADO = "CREADO"
    PAGADO = "PAGADO"
    CANCELADO = "CANCELADO"


@dataclass(frozen=True)
class Item:
    sku: str
    cantidad: int
    precio_centavos: int

    def __post_init__(self):
        if self.cantidad <= 0:
            raise PedidoInvalido("cantidad debe ser > 0")
        if self.precio_centavos < 0:
            raise PedidoInvalido("precio no puede ser negativo")


@dataclass
class Pedido:
    items: list[Item]
    estado: EstadoPedido = EstadoPedido.CREADO
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        if not self.items:
            raise PedidoInvalido("un pedido necesita al menos un item")

    @property
    def total(self) -> int:
        return sum(i.cantidad * i.precio_centavos for i in self.items)

    def _exigir_creado(self, accion: str):
        if self.estado is not EstadoPedido.CREADO:
            raise PedidoInvalido(f"no se puede {accion} un pedido {self.estado.value}")

    def pagar(self):
        self._exigir_creado("pagar")
        self.estado = EstadoPedido.PAGADO

    def cancelar(self):
        self._exigir_creado("cancelar")
        self.estado = EstadoPedido.CANCELADO
