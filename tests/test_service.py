import pytest
from pedidos.domain import EstadoPedido, Item, PedidoInvalido
from pedidos.repository import SqlitePedidoRepository
from pedidos.service import PedidoNoEncontrado, PedidoService


class RepoEnMemoria:  # prueba que el servicio solo depende del contrato
    def __init__(self): self.d = {}
    def add(self, p): self.d[p.id] = p
    def get(self, id): return self.d.get(id)
    def update(self, p): self.d[p.id] = p


@pytest.fixture(params=[RepoEnMemoria, SqlitePedidoRepository])
def svc(request):
    return PedidoService(request.param())

def test_flujo_crear_y_pagar(svc):
    p = svc.crear_pedido([Item("A", 1, 100)])
    assert svc.pagar(p.id).estado is EstadoPedido.PAGADO

def test_flujo_crear_y_cancelar(svc):
    p = svc.crear_pedido([Item("A", 1, 100)])
    assert svc.cancelar(p.id).estado is EstadoPedido.CANCELADO
    with pytest.raises(PedidoInvalido):  # el estado CANCELADO quedó persistido
        svc.pagar(p.id)

def test_no_cancelar_pagado(svc):
    p = svc.crear_pedido([Item("A", 1, 100)])
    svc.pagar(p.id)
    with pytest.raises(PedidoInvalido):
        svc.cancelar(p.id)

def test_id_inexistente(svc):
    with pytest.raises(PedidoNoEncontrado):
        svc.pagar("nope")
