select
c.influencer_id,
--ven.*
round(sum(ven.total)::numeric, 2) total,
count(distinct ven.venta_id)
from ventas ven
inner join visitas vis on vis.user_id = ven.user_id and ven.created_at >= vis.created_at
left join composiciones c on c.composicion_id = vis.composicion_id::integer
group by 1
order by 2 desc;


select
c.influencer_id,
round(sum(total)::numeric, 2)
from comisiones c
group by 1
order by 2 desc



SELECT
 pc.*,
 i.influencer_id,
 i.pct_comision
FROM productos_comp pc
INNER JOIN composiciones c on c.composicion_id = pc.composicion_id
INNER JOIN influencers i on i.influencer_id = c.influencer_id)



with prod_comp as (
	select
	c.composicion_id,
	c.influencer_id,
	cp.producto_id
	from composiciones c
	inner join productos_comp cp on cp.composicion_id = c.composicion_id)
,
com_ventas as (
	select
	sum(ventas.total) as total_ventas,
	sum(comisiones.total) as total_comisiones,
	100.0 * sum(comisiones.total) / sum(ventas.total) as comision_ratio
	from ventas
	inner join visitas on ventas.user_id = visitas.user_id and ventas.created_at > visitas.created_at
	inner join composiciones on visitas.composicion_id = composiciones.composicion_id
	inner join comisiones on comisiones.venta_id = ventas.venta_id
	where visitas.composicion_id > 0
)

,ventas_comp as (
	select
	sum(lv.total * lv.unidades) as total_ventas_composiciones
	from lineas_ventas lv
	inner join prod_comp pc on pc.producto_id = lv.producto_id
	inner join ventas ven on lv.venta_id = ven.venta_id
	inner join visitas vis on ven.user_id = vis.user_id and ven.created_at > vis.created_at and vis.composicion_id > 0
	inner join composiciones c on vis.composicion_id = c.composicion_id and c.composicion_id = pc.composicion_id
)

select
(select total_ventas_composiciones from ventas_comp) as total_ventas_composiciones,
(select total_ventas from com_ventas) as total_ventas,
(select total_comisiones from com_ventas) as total_comisiones,
(select comision_ratio from com_ventas) as comision_ratio_neta,
100.0 * (select total_comisiones from com_ventas) / (select total_ventas_composiciones from ventas_comp) as comision_ratio_composiciones

