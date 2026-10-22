# Priority Sale Order

**Gerencie pedidos de venda prioritários com um limite configurável por período.**

## Visão geral

Priority Sale Order adiciona ao formulário do pedido de venda um seletor para marcá-lo como **Normal** ou **Alta**. O módulo permite limitar quantos pedidos podem receber prioridade alta durante um período configurado, ajudando a equipe comercial a distribuir o atendimento prioritário.

O módulo surgiu de uma necessidade prática das lojas: alguns pedidos precisam ter seus envios ou entregas atendidos antes dos demais, mas a capacidade de preparar e despachar pedidos é limitada. Sem uma forma clara de identificar essas vendas, a equipe pode perder de vista quais entregas são urgentes ou acabar tratando pedidos demais como prioritários.

O Priority Sale Order permite que a equipe de vendas sinalize os pedidos que precisam de atendimento prioritário e ajuda cada loja a administrar essa capacidade. Nos ajustes, os responsáveis definem quantos pedidos podem receber prioridade alta e qual período será usado para aplicar esse limite. Assim, cada loja pode adaptar o controle ao seu volume de trabalho e à frequência com que organiza a preparação, os envios ou as entregas.

A prioridade fica visível nos pedidos de venda, nas transferências relacionadas e nas linhas de operação, ajudando as equipes a identificar entregas urgentes durante o acompanhamento e a preparação. Também é possível escolher quais estados dos pedidos participam da verificação do limite e quais grupos de usuários podem atribuir prioridade alta. Dessa forma, vendas e operações compartilham um indicador visível e critérios comuns para organizar as entregas urgentes.

## Recursos

- Marque cada pedido de venda como normal ou de prioridade alta e exiba esse valor nas listas de pedidos, cotações e transferências vinculadas.
- Exiba a prioridade herdada do pedido nas linhas de operações e nas operações detalhadas de suas transferências vinculadas.
- Ordene as listas de transferências e entregas mostrando primeiro as prioritárias e, em seguida, por data programada.
- Exiba a prioridade no formulário do pedido e bloqueie alterações quando o estado não estiver habilitado, o limite tiver sido atingido ou o pedido estiver concluído.
- Configure os estados considerados, o número máximo de pedidos prioritários e o deslocamento de dias do período.

## Requisitos

- Odoo 17.0, 18.0, 19.0 e 20.0
- Aplicativos Vendas e Inventário (`sale_stock`)

## Instalação e uso

1. Instale `priority_sale_order` em Aplicativos.
2. Abra uma cotação ou um pedido de venda.
3. Use o seletor **Prioridade** para escolher **Normal** ou **Alta**, quando a alteração estiver habilitada.

## Configuração

Configure o módulo em **Configurações → Prioridade de pedidos de venda**. Todos os parâmetros de controle são gerenciados nessa seção e armazenados como parâmetros do sistema. Somente usuários dos grupos selecionados podem atribuir prioridade alta; por padrão, o grupo de administradores de vendas está autorizado.

| Configuração | Valor padrão | Finalidade |
|---|---:|---|
| Estados incluídos | `sale`, `done` | Selecione um ou mais estados definidos pelo modelo `sale.order`. |
| Limite de prioridade alta | `3` | Número máximo de pedidos de prioridade alta no período. |
| Deslocamento do período | `1.0` dia | Deslocamento em dias usado para determinar o período verificado. |

Pedidos no estado **Concluído** ficam sempre bloqueados. Pedidos cujos estados não estejam em `only_check_states` também ficam bloqueados; na configuração padrão, pedidos cancelados não participam da verificação.
