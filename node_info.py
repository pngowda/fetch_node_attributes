#!/usr/bin/env python3


"""
Python script to fetch node attributes.

Requirements:
    Python3 and psutil python module available on the host machine.
"""


import json
import logging
import platform
import psutil


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def initialize_logger():
    """
    Initialize the loggers and set log levels.
    :return: None
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_os_info():
    """
    Getting OS information.
    :return: None
    """
    uname = platform.uname()
    logging.info("Release: %s", uname.release)
    logging.info("Version: %s", uname.version)
    data["OS"] = []
    data["OS"].append(
        {
            "Operating System": uname.system,
            "Release": uname.release,
            "Version": uname.version,
        }
    )


def get_cpu_info():
    """
    Getting CPU information.
    :return: None
    """
    logging.info("Physical cores: %d", psutil.cpu_count(logical=False))
    logging.info("Total cores: %d", psutil.cpu_count(logical=True))
    data["CPU"] = []
    data["CPU"].append(
        {
            "Physical cores": psutil.cpu_count(logical=False),
            "Total cores": psutil.cpu_count(logical=True),
        }
    )


def get_memory_info():
    """
    Getting memory information.
    :return: None
    """
    # Get virtual memory details.
    svmem = psutil.virtual_memory()
    logging.info("Total: %s", get_size(svmem.total))
    logging.info("Available: %s", get_size(svmem.available))
    logging.info("Used: %s", get_size(svmem.used))
    logging.info("Percentage: %s", svmem.percent)
    data["MEMORY"] = []
    data["MEMORY"].append(
        {
            "VIRTUAL_MEMORY": {
                "Total": get_size(svmem.total),
                "Available": get_size(svmem.available),
                "Used": get_size(svmem.used),
                "Percentage": svmem.percent,
            }
        }
    )
    # Get the swap memory details
    swap = psutil.swap_memory()
    logging.info("Total: %s", get_size(swap.total))
    logging.info("Free: %s", get_size(swap.free))
    logging.info("Used: %s", get_size(swap.used))
    logging.info("Percentage: %s", swap.percent)
    data["MEMORY"].append(
        {
            "SWAP_MEMORY": {
                "Total": get_size(swap.total),
                "Free": get_size(swap.free),
                "Used": get_size(swap.used),
                "Percentage": swap.percent,
            }
        }
    )


def get_disk_info():
    """
    Getting disk partition information.
    :return: None
    """
    logging.info("Partitions and Usage:")
    data["DISK_PARTITIONS"] = []
    partitions = psutil.disk_partitions()

    for partition in partitions:
        try:
            logging.info("Device: %s", partition.device)
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be cought when the disk isn't ready
            continue
        logging.info("  Total Size: %s", get_size(partition_usage.total))
        logging.info("  Used: %s", get_size(partition_usage.used))
        logging.info("  Free: %s", get_size(partition_usage.free))
        logging.info("  Percentage: %s", partition_usage.percent)
        data["DISK_PARTITIONS"].append(
            {
                partition.device: {
                    "Mount Point": partition.mountpoint,
                    "Total Size": get_size(partition_usage.total),
                    "Used": get_size(partition_usage.used),
                    "Free": get_size(partition_usage.free),
                    "Percentage": partition_usage.percent,
                }
            }
        )


if __name__ == "__main__":
    initialize_logger()
    data = {}
    get_os_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()

    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing to node_attribute_information.json
    with open("node_attribute_information.json", "w") as outfile:
        outfile.write(json_object)