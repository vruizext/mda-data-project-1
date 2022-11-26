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