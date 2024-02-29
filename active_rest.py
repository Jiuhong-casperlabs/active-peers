import argparse
import threading
import requests
from pycspr import NodeClient, NodeConnectionInfo

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
        url = f'http://{peer}:8888/status'

        resp = requests.get(url)
        if resp.status_code == 200:
            print(peer)

    except Exception as err:
        pass


def _main(args: argparse.Namespace):
    # Set client.
    client = _get_client(args)

    # Query: get_node_peers.
    node_peers = client.get_node_peers()

    active_peers = [x["address"].split(":")[0] for x in node_peers]

    # creating threads
    threads_list = [threading.Thread(
        target=get_rpc_sse_open, args=(peer,)) for peer in active_peers]

    # starting process 1 - n
    for thread in threads_list:
        thread.start()

    print("\nActive peers with rest port opened.")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(
        host=args.node_host,
        port_rpc=args.node_port_rpc
    ))


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
