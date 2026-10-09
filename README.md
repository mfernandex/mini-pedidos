# mini-pedidos

[![tests](https://github.com/mfernandex/mini-pedidos/actions/workflows/tests.yml/badge.svg)](https://github.com/mfernandex/mini-pedidos/actions/workflows/tests.yml)

Gestión de pedidos en Python: crear pedidos con items, pagarlos y cancelarlos, con persistencia en SQLite.
Solo usa la biblioteca estándar (pytest para los tests).

## Reglas de negocio

1. Un pedido tiene al menos un item; cada item tiene cantidad > 0 y precio >= 0.
2. Estados: `CREADO` -> `PAGADO` | `CANCELADO`.
3. Solo un pedido `CREADO` puede pagarse o cancelarse.
4. `total = suma(cantidad * precio_centavos)`. El dinero siempre va en centavos (`int`), nunca `float`.

La especificación completa está en [`docs/spec.md`](docs/spec.md).

## Arquitectura

Tres capas; cada una depende solo de la inferior:

```
domain  ->  repository  ->  service
```

| Capa | Archivo | Contenido |
|---|---|---|
| Dominio | `src/pedidos/domain.py` | `Pedido`, `Item`, `EstadoPedido`, `PedidoInvalido` |
| Repositorio | `src/pedidos/repository.py` | Contrato `PedidoRepository` (`add`, `get`, `update`) e implementación `SqlitePedidoRepository` |
| Servicio | `src/pedidos/service.py` | `PedidoService` (`crear_pedido`, `pagar`, `cancelar`) y `PedidoNoEncontrado` |

El servicio funciona con cualquier repositorio que cumpla el contrato `PedidoRepository`.

## Uso

```python
from pedidos.domain import Item
from pedidos.repository import SqlitePedidoRepository
from pedidos.service import PedidoService

svc = PedidoService(SqlitePedidoRepository())   # ":memory:" por defecto
p = svc.crear_pedido([Item("A1", 2, 1500)])
p.total            # 3000 centavos
svc.pagar(p.id)    # estado -> PAGADO
```

Para persistir en disco: `SqlitePedidoRepository("pedidos.db")`.

## Instalación y tests

Requiere Python 3.11+ (el proyecto fija 3.11.13 en `.python-version`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
PYTHONPATH=src pytest -q
```

## Contribuir

Las reglas del proyecto están en [`AGENTS.md`](AGENTS.md). En resumen: un cambio toca una sola capa,
los contratos (`docs/spec.md` y el `Protocol` del repositorio) no se cambian sin proponerlo antes,
y cada cambio termina con los tests en verde.
