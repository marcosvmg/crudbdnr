import redis


r = redis.Redis(host='localhost', port=6379, db=0)


r.set('chave', 'valor')


valor = r.get('chave')

print(valor.decode())  
