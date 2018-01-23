from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class HelloWorldService(ServiceBase):

    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, ctx, name):
        for i in range(0, 3):
            yield u'Hello, %s %d' % (name, i)


application = Application([HelloWorldService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.info("listening to http://192.168.1.110:8002")
    logging.info("wsdl is at: http://192.168.1.110:8002/?wsdl")
    server = make_server('192.168.1.110', 8002, wsgi_application)
    server.serve_forever()
