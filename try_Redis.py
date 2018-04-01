import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
print(r.get('foo'))
print(r.get('bar'))        # key = 'foo', value = 'bar'

r.sadd('s1', 2, 4, 'a', 'cd')
print(r.scard('s1'))
print(r.smembers('s1'))    # unordered