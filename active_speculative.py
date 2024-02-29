import argparse
import json
import socket
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

payload = {
    "id": -573285493134384228,
    "jsonrpc": "2.0",
    "method": "speculative_exec",
    "params": {"deploy": {
        "hash": "72ddc7b2537405753699e2fc38c90a72af8b42b39dbc982fd3ce5cf0835a468f",
        "header": {
            "ttl": "30m",
            "account": "01341bfb101714eab96ad91b443a5c9be53b6bb4f3ed8c173cb9e409686e6c800d",
            "body_hash": "4ef01f17abcaccd4143ba731ab4b23fb661e1ee30f1ba4e6cf2bfdc9cf1293b8",
            "gas_price": 1,
            "timestamp": "2023-11-09T02:31:36.351Z",
            "chain_name": "casper-test",
            "dependencies": []
        },
        "payment": {
            "ModuleBytes": {
                "args": [
                    [
                        "amount",
                        {
                            "bytes": "0400e1f505",
                            "parsed": "100000000",
                            "cl_type": "U512"
                        }
                    ]
                ],
                "module_bytes": ""
            }
        },
        "session": {
            "Transfer": {
                "args": [
                    [
                        "amount",
                        {
                            "bytes": "050088526a74",
                            "parsed": "500000000000",
                            "cl_type": "U512"
                        }
                    ],
                    [
                        "target",
                        {
                            "bytes": "013afe9dd45a16ffc9847ab21c3f969da71e62bebde3d597fcabbbf01477d5fdb2",
                            "parsed": "013afe9dd45a16ffc9847ab21c3f969da71e62bebde3d597fcabbbf01477d5fdb2",
                            "cl_type": "PublicKey"
                        }
                    ],
                    [
                        "id",
                        {
                            "bytes": "00",
                            "parsed": "null",
                            "cl_type": {
                                "Option": "U64"
                            }
                        }
                    ]
                ]
            }
        },
        "approvals": [
            {
                "signer": "01341bfb101714eab96ad91b443a5c9be53b6bb4f3ed8c173cb9e409686e6c800d",
                "signature": "0147e73bbb4260320dff28dab7167628655aecc0490744a5127ce75e0f39f1f6fc92ebb17bf10f9277d3cf4f4510f73174bba7f4253ef2cccbb2ca328f4b853307"
            }
        ]
    }

    }}


def get_rpc_sse_open(peer):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8)
        rpc_result = sock.connect_ex((peer, 7778))  # check 7778 port
        if rpc_result == 0:
            rpc_result = requests.post(f'http://{peer}:7778/rpc', json=payload)

        if rpc_result.status_code == 200:
            print(f'http://{peer}:7778')

    except Exception as err:
        # print(peer, err)
        pass


def _main(args: argparse.Namespace):
    # Set client.
    client = _get_client(args)

    # Query: get_node_peers.
    node_peers = client.get_node_peers()

    active_peers = [x["address"].split(":")[0] for x in node_peers]

    # creating process
    threads_list = [threading.Thread(
        target=get_rpc_sse_open, args=(peer,)) for peer in active_peers]

    # starting process 1 - n
    for thread in threads_list:
        thread.start()

    print("\nActive peers with speculative_exec opened.")

    for thread in threads_list:
        thread.join()

    print("All tasks has been finished")


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
