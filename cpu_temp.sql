USE zabbix;

select
FROM_UNIXTIME(history.clock),
history.itemid,history.value from history where history.itemid=ANY(
SELECT items.itemid FROM items WHERE items.hostid= ANY(SELECT `hosts`.hostid FROM `hosts`WHERE `hosts`.`host` ='hostname_ip' AND items.key_ NOT LIKE 'system.cpu.util[hrProcessorLoad.{%' and items.key_ like 'system.cpu.util[hrProcessorLoad%' ))
and UNIX_TIMESTAMP(now())-history.clock < 180
order by history.itemid,history.clock desc
