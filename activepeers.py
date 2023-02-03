import argparse
import json
import time
import multiprocessing
import socket
from pycspr import NodeClient
from pycspr import NodeConnection

# CLI argument parser.
_ARGS = argparse.ArgumentParser(
    "Demo illustrating how to find active peers.")

# CLI argument: host address of target node - defaults to testnet node 94.130.10.55.
# testnet
#  3.136.227.9
#  3.23.146.54
# mainnet:
#  3.14.161.135
#  3.12.207.193
#  3.142.224.108
_ARGS.add_argument(
    "--node-host",
    default="94.130.10.55",
    dest="node_host",
    help="Host address of target node.",
    type=str,
)

# CLI argument: Node API JSON-RPC port - defaults to 7777.
_ARGS.add_argument(
    "--node-port-rpc",
    default=7777,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
)


def get_rpc_sse_open(peer):
    try:
        # client = NodeClient(NodeConnection(host=peer, port_rpc=7777))
        # state_root_hash: bytes = client.get_state_root_hash()
        # if isinstance(state_root_hash, bytes):
        #     print("http://" + peer + ":7777")
        # # print(state_root_hash.hex())

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8)
        rpc_result = sock.connect_ex((peer, 7777))  # check rpc port
        if rpc_result == 0:
            sock.connect_ex((peer, 9999))  # check sse port
            if rpc_result == 0:
                port = {
                    "RPC": "http://" + peer + ":7777",
                    "SSE": "http://" + peer + ":9999",
                }
                print(json.dumps(port, indent=2))
        sock.close()

    except Exception as err:
        pass


def _main(args: argparse.Namespace):
    # Set client.
    client = _get_client(args)

    # Query: get_node_peers.
    node_peers = client.get_node_peers()

    active_peers = [x["address"].split(":")[0] for x in node_peers]

    # creating process
    processes_list = [multiprocessing.Process(
        target=get_rpc_sse_open, args=(peer,)) for peer in active_peers]

    print("Active peers:")
    # starting process 1 - n
    for process in processes_list:
        process.start()

    time.sleep(1)
    for process in processes_list:
        process.terminate()

    print("Done!")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc
    ))


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
