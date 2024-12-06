
from multiprocessing.connection import Listener
from multiprocessing.connection import Client

import grpc
import logging
from concurrent import futures
from threading import Event
import logging
import os
logging.basicConfig()
LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.ERROR)

def default_callback(command):
    return {'action':'default', 'status':False}

def service(listner_parms, output_connparms, callback=default_callback, *callback_args, **kwargs):
    with Listener(listner_parms, authkey=b'secret') as listener:
        stop_signal = kwargs.get('stop_signal', None)
        while stop_signal is None or not stop_signal.is_set():
            with listener.accept() as input_conn:
                try:
                    cmd = input_conn.recv()
                except EOFError:
                    input_conn.close()
                    continue
                
                print('Get an request.')
                payload = callback(cmd, *callback_args)
                print('End request.')
                
            if payload.pop('to_output', False):
                override_output = payload.pop('override_output', False)
                with Client(output_connparms if not override_output else override_output, authkey=b'secret') as output_conn:
                    output_conn.send(payload)

def serve(servicer_to_server_adder, servicer, logger, signal = Event(), server_port='50051'):
    logger.setLevel(LOG_LEVEL)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer_to_server_adder(servicer, server)
    server.add_insecure_port(f"[::]:{server_port}")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
    signal.set()


if __name__ == "__main__":
    serve()