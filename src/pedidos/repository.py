from __future__ import annotations
import json
import sqlite3
from typing import Protocol

from .domain import EstadoPedido, Item, Pedido


class PedidoRepository(Protocol):
    """Contrato de persistencia. El servicio solo conoce esto."""
    def add(self, pedido: Pedido) -> None: ...
    def get(self, id: str) -> Pedido | None: ...
    def update(self, pedido: Pedido) -> None: ...


class SqlitePedidoRepository:
    def __init__(self, path: str = ":memory:"):
        self._db = sqlite3.connect(path)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS pedidos "
            "(id TEXT PRIMARY KEY, estado TEXT NOT NULL, items TEXT NOT NULL)"
        )

    @staticmethod
    def _items_json(p: Pedido) -> str:
        return json.dumps([[i.sku, i.cantidad, i.precio_centavos] for i in p.items])

    def add(self, pedido: Pedido) -> None:
        self._db.execute(
            "INSERT INTO pedidos VALUES (?, ?, ?)",
            (pedido.id, pedido.estado.value, self._items_json(pedido)),
        )
        self._db.commit()

    def get(self, id: str) -> Pedido | None:
        row = self._db.execute(
            "SELECT estado, items FROM pedidos WHERE id = ?", (id,)
        ).fetchone()
        if row is None:
            return None
        estado, items = row
        return Pedido(
            id=id,
            estado=EstadoPedido(estado),
            items=[Item(*i) for i in json.loads(items)],
        )

    def update(self, pedido: Pedido) -> None:
        self._db.execute(
            "UPDATE pedidos SET estado = ? WHERE id = ?",
            (pedido.estado.value, pedido.id),
        )
        self._db.commit()
