# neoDNS

Lightweight "DNS" that operates by returning http page

## Operation

user sends the auth data to server through https, like this:

```json
{
    "operation": "get",
    "name": "media server",
    "password": "12345"
},
{
    "operation": "set",
    "name": "game server",
    "password": "abcde",
    "address": "8.8.8.8"
}
```

server receives the message and respond to the message:
```json
{
    "1.1.1.1"
},
{
    "OK"
}
```
