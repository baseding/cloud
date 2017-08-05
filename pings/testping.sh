for i in {1..10}:
do
curl -X POST \
  http://10.8.60.82:8000/pings/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 89f8109e-a43e-edcf-c345-4c6a9cc1445c' \
  -d '{  
 "json_data": [{
  "type": "ping",
  "dstip": "218.202.227.4",
  "sshhostip": "10.1.60.19",
  "srcip": "218.202.226.119"
  }]
}
'&
curl -X POST \
  http://10.8.60.82:8000/pings/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'postman-token: 89f8109e-a43e-edcf-c345-4c6a9cc1445c' \
  -d '{  
 "json_data": [{
  "type": "ping",
  "dstip": "114.114.114.114",
  "sshhostip": "10.1.60.19",
  "srcip": "218.202.226.119"
  }]
}
'&

done
