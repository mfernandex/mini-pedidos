# Spec: gestión de pedidos

## Objetivo
Crear pedidos con items, pagarlos y cancelarlos, con persistencia.

## Reglas de negocio
1. Un pedido tiene al menos un item; cada item tiene cantidad > 0 y precio >= 0.
2. Estados: CREADO -> PAGADO | CANCELADO.
3. Solo un pedido CREADO puede pagarse o cancelarse.
4. total = suma(cantidad * precio_centavos).

## Contratos entre capas
- Dominio: `Pedido`, `Item`, `EstadoPedido`, `PedidoInvalido`.
- Repositorio: `add(pedido)`, `get(id) -> Pedido | None`, `update(pedido)`.
- Servicio: `crear_pedido(items) -> Pedido`, `pagar(id)`, `cancelar(id)`; lanza `PedidoNoEncontrado`.

## Criterios de aceptación
- Todas las reglas anteriores cubiertas por tests.
- El servicio funciona con cualquier repositorio que cumpla el contrato.
