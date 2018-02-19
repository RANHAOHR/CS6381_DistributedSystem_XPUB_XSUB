import zmq
import time
import sys
import random
# from  multiprocessing import Process

def main():
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("ipc://frontend.ipc")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")


    # # Start background tasks
    # def start(task, *args):
    #     process = multiprocessing.Process(target=task, args=args)
    #     process.daemon = True
    #     process.start()
    # for i in range(NBR_CLIENTS):
    #     start(client_task, i)
    # for i in range(NBR_WORKERS):
    #     start(worker_task, i)

    # Initialize main loop state
    # count = NBR_CLIENTS
    workers = []
    owershipe_vec = []
    history = []
    poller = zmq.Poller()
    # Only poll for requests from backend until workers are available
    poller.register(backend, zmq.POLLIN)

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            worker, empty, client, ownership_strength, history = request[:5]
            workers.append(worker)
            ranked_workers = [workers for _,workers in sorted(zip(ownership_strength,workers))]
            if not ranked_workers:
                # Poll for clients now that a worker is available
                poller.register(frontend, zmq.POLLIN)
            if client != b"READY" and len(request) > 3:
                # If client reply, send rest back to frontend
                # empty, reply = request[3:]
                # frontend.send_multipart([client, b"", reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            client, empty, request = frontend.recv_multipart()
            ranked_workers = ranked_workers.pop(0)
            backend.send_multipart([ranked_workers, b"", client, b"", request])
            if not workers:
                # Don't poll clients if no workers are available
                poller.unregister(frontend)

    # Clean up
    backend.close()
    frontend.close()
    context.term()

if __name__ == "__main__":
    main()
