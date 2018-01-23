from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import


# url = 'http://47.90.214.117:8080/smart_value_added/webservice/weather?wsdl'
# imp = Import('http://www.w3.org/2001/XMLSchema',
#              location='http://www.w3.org/2001/XMLSchema.xsd')
# imp.filter.add('http://inter.weather.webservice.secomid.com/')
# client = Client(url, plugins=[ImportDoctor(imp)])
# result = client.service.findWeatherDate(
#     '{city:"guilin",language:"en",longitude:"30.00",latitude:"-29.00"}')
# print(result)


from suds.client import Client
url = "http://192.168.1.110:8002/?wsdl"
client = Client(url)
result = client.service.say_hello("bugmaster", 3)
print(result)
