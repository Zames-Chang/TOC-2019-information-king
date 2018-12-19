class a(object):
    def __init__(self):
        self.z = 1

j = [a()]

def foo():
    return j[0]

x = foo()

x.z = 0

print(j[0].z)

