use msdb

select 
p.name, 
p.id, 
p.description, 
p.folderid, 
p.ownersid, 
convert(varchar(max), convert(varbinary(max), p.packagedata)) as [Data],
f.* 

from sysssispackages p
inner join sysssispackagefolders f on p.folderid = f.folderid
where f.foldername not like '%data collector%' -- not including this as it doesn't yield xml when converted
order by p.name