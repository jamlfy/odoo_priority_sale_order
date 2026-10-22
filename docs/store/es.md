# Priority Sale Order

**Gestiona los pedidos de venta prioritarios con un límite configurable por periodo.**

## Descripción

Priority Sale Order añade al formulario del pedido de venta un selector para marcarlo como **Normal** o **Alta**. El módulo permite limitar cuántos pedidos pueden tener prioridad alta durante un periodo configurado, para distribuir la atención prioritaria del equipo comercial.

El módulo nació de una necesidad práctica de las tiendas: algunos pedidos requieren que su envío o reparto se atienda antes que los demás, pero la capacidad para preparar y despachar pedidos es limitada. Sin una forma clara de identificar esas ventas, el equipo puede perder de vista cuáles requieren atención urgente o terminar marcando demasiados pedidos como prioritarios.

Priority Sale Order permite que el equipo de ventas marque los pedidos que necesitan atención prioritaria y que la tienda establezca un límite para distribuir esa capacidad. En los ajustes, los responsables definen cuántos pedidos pueden tener prioridad alta y el periodo que se utiliza para aplicar ese máximo. De esta manera, cada tienda puede adaptar el control a su volumen de trabajo y a la frecuencia con la que organiza sus preparaciones, envíos o repartos.

La prioridad se muestra tanto en los pedidos de venta como en las transferencias relacionadas y sus líneas de operación, de modo que el equipo pueda identificar las entregas prioritarias durante el seguimiento y la preparación. También se puede limitar qué estados de los pedidos participan en el control y qué grupos de usuarios están autorizados para asignar prioridad alta. Así, ventas y operaciones comparten una señal visible y un criterio común para organizar las entregas urgentes.

## Funcionalidades

- Marca cada pedido de venta como normal o de prioridad alta y muestra ese valor en las listas de pedidos, cotizaciones y transferencias vinculadas.
- Muestra la prioridad heredada del pedido en las líneas de operaciones y operaciones detalladas de sus transferencias vinculadas.
- Ordena las listas de pickings y entregas mostrando primero las transferencias prioritarias y, después, por fecha programada.
- Muestra la prioridad en el formulario del pedido y bloquea el cambio cuando el estado no está habilitado, se alcanzó el límite o el pedido está hecho.
- Configura los estados que participan en el control, el máximo de pedidos prioritarios y el desplazamiento de días del periodo.

## Requisitos

- Odoo 17.0, 18.0, 19.0 y 20.0
- Aplicaciones Ventas e Inventario (`sale_stock`)

## Instalación y uso

1. Instala el módulo `priority_sale_order` desde Aplicaciones.
2. Abre un presupuesto o pedido de venta.
3. Usa el selector **Prioridad** para elegir **Normal** o **Alta**, si el control permite modificarlo.

## Configuración

Configura el módulo desde **Ajustes → Prioridad de pedidos de venta**. Todos los parámetros del control se administran en esta sección y se guardan como parámetros del sistema. Solo los usuarios que pertenezcan a los grupos seleccionados pueden asignar prioridad alta; por defecto se autoriza al grupo de administradores de ventas.

| Ajuste | Valor inicial | Uso |
|---|---:|---|
| Estados incluidos | `sale`, `done` | Selecciona uno o varios estados definidos por el modelo `sale.order`. |
| Máximo de prioridad alta | `3` | Máximo de pedidos de prioridad alta en el periodo. |
| Desplazamiento del periodo | `1.0` día | Desplazamiento en días usado para determinar el periodo consultado. |

Los pedidos en estado **Hecho** siempre quedan bloqueados. Los pedidos cuyos estados no estén incluidos en `only_check_states` también quedan bloqueados; con la configuración inicial, los pedidos cancelados no participan en el control.
