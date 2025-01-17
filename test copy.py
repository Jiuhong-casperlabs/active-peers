import asyncio
from stress_rpc import choose_node
from stress_rpc import myfunc


async def print_numbers():

    for i in range(10):

        print(f"{i}")

        await asyncio.sleep(1)


async def print_letters():

    for letter in 'abcdefghij':

        print(f"{letter}")

        await asyncio.sleep(1)


async def main():
    COUNT = 100
    node_ip = choose_node()
    task1 = asyncio.create_task(myfunc(node_ip, 1))
    await task1

    # task2 = asyncio.create_task(print_letters())
    # tasks_list = [asyncio.create_task(myfunc(node_ip, x))
    #               for x in range(COUNT)]

    # [await task for task in tasks_list]


asyncio.run(main())
