"""
A Python library to parse and return various attributes from the CPU string
"""
import re
import argparse
from cpuinfo import get_cpu_info
from .intel import parse_intel_cpu
from .amd import parse_amd_cpu

def map_vendor(vendor):
    """
    Rewrite vendor name
    """
    if vendor == 'GenuineIntel':
        returnval = 'Intel'
    elif vendor == 'AuthenticAMD':
        returnval = 'AMD'
    else:
        returnval = vendor
    return returnval

def guess_vendor(cpustring):
    """
    Attempt to guess a CPU vendor from its string
    """
    if 'Intel' in cpustring:
        vendor = 'Intel'
    elif 'AMD' in cpustring:
        vendor = 'AMD'
    return vendor

def clean_cpu_string(brand):
    """
    Rewrite CPU string more neatly.
    
    This:
        Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
    Becomes:
        Intel Core i5-6300U
    """
    # Strip annoying chars
    brand = brand.replace('(R)', '')
    brand = brand.replace('(TM)', '')
    brand = brand.replace('(tm)', '')
    brand = brand.replace('CPU', '')
    brand = brand.replace('Processor', '')

    # Drop the '@ 2.40GHz' suffix
    brand = brand.split('@')[0]

    # Drop the 'with Radeon Graphics' suffix
    brand = brand.split('with')[0]

    # Drop '64-Core'
    brand = re.sub(r"\d+-Core", '', brand)

    # Delete multiple spaces
    brand = brand.strip()
    brand = re.sub(r'\s+', ' ', brand)

    return brand


def drop_nones_inplace(d: dict) -> dict:
    """Recursively drop Nones in dict d in-place and return original dict"""
    dd = drop_nones(d)
    d.clear()
    d.update(dd)
    return d


def drop_nones(d: dict) -> dict:
    """Recursively drop Nones in dict d and return a new dict"""
    dd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            dd[k] = drop_nones(v)
        elif isinstance(v, (list, set, tuple)):
            # note: Nones in lists are not dropped
            # simply add "if vv is not None" at the end if required
            dd[k] = type(v)(drop_nones(vv) if isinstance(vv, dict) else vv
                            for vv in v)
        elif v is not None:
            dd[k] = v
    return dd


def get_cpu_model(cpustring):
    """
    Get info about the CPU model and return it as a dict
    """

    if cpustring:
        # Use supplied CPU string
        cpuinfo = {}
        cpuinfo['vendor_id_raw'] = guess_vendor(cpustring)
        cpuinfo['brand_raw'] = cpustring
    else:
        # Fetch CPU info from system
        cpuinfo = get_cpu_info()

    # Generate basic labels
    labels = {}
    labels['cpuVendor'] = map_vendor(cpuinfo['vendor_id_raw'])
    labels['cpuString'] = clean_cpu_string(cpuinfo['brand_raw'])

    # Calculate some extra labels
    if labels['cpuVendor'] == 'Intel':
        labels.update(parse_intel_cpu(labels['cpuString']))
    elif labels['cpuVendor'] == 'AMD':
        labels.update(parse_amd_cpu(labels['cpuString']))

    # Drop None elements
    labels = drop_nones_inplace(labels)

    return labels

def main():
    """
    Display CPU model info to a human user
    """

    # Read in args
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help="Supply a CPU string rather than obtaining it from the system", type=str)
    args = parser.parse_args()

    labels = get_cpu_model(args.test)
    print(labels)

if __name__ == '__main__':
    main()
