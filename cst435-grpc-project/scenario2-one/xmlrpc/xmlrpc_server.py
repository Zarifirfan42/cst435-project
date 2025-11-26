from xmlrpc.server import SimpleXMLRPCServer

def sum_squares(numbers):
    return sum(x*x for x in numbers)

server = SimpleXMLRPCServer(("0.0.0.0", 9000))
print("XML-RPC server listening on port 9000...")
server.register_function(sum_squares, "sum_squares")
server.serve_forever()
