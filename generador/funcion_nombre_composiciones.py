from faker import Faker
import random



faker=Faker()

a= faker.text()
b=a.split()
print (b)    

j= (b[0:3])

print(j)

nombrecom=" "
nombrecom= nombrecom.join(j)
print(nombrecom)