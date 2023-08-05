import asyncio
import logging

from roborock import (
    CacheableCommands,
    DeviceData,
    HomeDataDevice,
    ROBOROCK_S7_MAXV,
)
from roborock.local_api import RoborockLocalClient

local_key = "nXTBj42ej5WxQopO"

buffer = {0: bytes()}


async def main():
    logging_config = {"level": logging.DEBUG}
    logging.basicConfig(**logging_config)
    device_info = DeviceData(
        device=HomeDataDevice(duid="1r9W0cAmDZ2COuVekgRhKA", local_key=local_key, name="test name", fv="1"),
        model=ROBOROCK_S7_MAXV,
        host="192.168.1.33",
    )
    print(CacheableCommands)
    client1 = RoborockLocalClient(device_info)
    # {
    #     'max_multi_map': 4,
    #     'max_bak_map': 1,
    #     'multi_map_count': 1,
    #     'map_info': [{
    #                      'mapFlag': 0,
    #                      'add_time': 1685652974,
    #                      'length': 11,
    #                      'name': 'Apartamento',
    #                      'bak_maps': [{'mapFlag': 4, 'add_time': 1685552361}]
    #                  }]
    # }
    x = await client1.get_prop()
    print(x)
    await asyncio.sleep(5)

    # capture = pyshark.LiveCapture(interface="rvi0")
    #
    # def on_package(packet: Packet):
    #     if hasattr(packet, "ip"):
    #         if packet.transport_layer == "TCP" and (packet.ip.dst == local_ip or packet.ip.src == local_ip):
    #             if hasattr(packet, "DATA"):
    #                 if hasattr(packet.DATA, "data"):
    #                     if packet.ip.dst == local_ip:
    #                         print("Request")
    #                         try:
    #                             f, buffer[0] = MessageParser.parse(
    #                                 buffer[0] + bytes.fromhex(packet.DATA.data), local_key
    #                             )
    #                             print(f)
    #                         except BaseException as e:
    #                             print(e)
    #                             pass
    #                     elif packet.ip.src == local_ip:
    #                         print("Response")
    #                         try:
    #                             f, buffer[0] = MessageParser.parse(
    #                                 buffer[0] + bytes.fromhex(packet.DATA.data), local_key
    #                             )
    #                             print(f)
    #                         except BaseException as e:
    #                             print(e)
    #                             pass
    #
    # while True:
    #     try:
    #         await capture.packets_from_tshark(on_package, close_tshark=False)
    #     except Exception as e:
    #         print(e)


if __name__ == "__main__":
    asyncio.run(main())
