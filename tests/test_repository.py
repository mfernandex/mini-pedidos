from pedidos.domain import EstadoPedido, Item, Pedido
from pedidos.repository import SqlitePedidoRepository


def test_roundtrip_y_update():
    repo = SqlitePedidoRepository()
    p = Pedido([Item("A", 2, 500)])
    repo.add(p)
    assert repo.get(p.id) == p
    p.pagar()
    repo.update(p)
    assert repo.get(p.id).estado is EstadoPedido.PAGADO

def test_get_inexistente():
    assert SqlitePedidoRepository().get("nope") is None
