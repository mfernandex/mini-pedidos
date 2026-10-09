import pytest
from pedidos.domain import EstadoPedido, Item, Pedido, PedidoInvalido


def test_total_suma_items():
    p = Pedido([Item("A", 2, 500), Item("B", 1, 250)])
    assert p.total == 1250

def test_pedido_vacio_invalido():
    with pytest.raises(PedidoInvalido):
        Pedido([])

@pytest.mark.parametrize("cant,precio", [(0, 100), (-1, 100), (1, -5)])
def test_item_invalido(cant, precio):
    with pytest.raises(PedidoInvalido):
        Item("A", cant, precio)

def test_pagar_y_no_cancelar_despues():
    p = Pedido([Item("A", 1, 100)])
    p.pagar()
    assert p.estado is EstadoPedido.PAGADO
    with pytest.raises(PedidoInvalido):
        p.cancelar()

def test_cancelado_no_se_paga():
    p = Pedido([Item("A", 1, 100)])
    p.cancelar()
    with pytest.raises(PedidoInvalido):
        p.pagar()
