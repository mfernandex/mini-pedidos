from __future__ import annotations

from .domain import Item, Pedido
from .repository import PedidoRepository


class PedidoNoEncontrado(LookupError):
    pass


class PedidoService:
    def __init__(self, repo: PedidoRepository):
        self._repo = repo

    def crear_pedido(self, items: list[Item]) -> Pedido:
        pedido = Pedido(items=items)
        self._repo.add(pedido)
        return pedido

    def _cargar(self, id: str) -> Pedido:
        pedido = self._repo.get(id)
        if pedido is None:
            raise PedidoNoEncontrado(id)
        return pedido

    def pagar(self, id: str) -> Pedido:
        pedido = self._cargar(id)
        pedido.pagar()
        self._repo.update(pedido)
        return pedido

    def cancelar(self, id: str) -> Pedido:
        pedido = self._cargar(id)
        pedido.cancelar()
        self._repo.update(pedido)
        return pedido
