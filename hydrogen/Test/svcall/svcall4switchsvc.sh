curl -i -X POST http://192.168.0.13:8091/v1/svs/$1 -H "X-Auth-Token:$tokens" -H "Content-Type:application/json" -d '{"ckey":"sv_3","scatdataline":"0;0;1"}'
