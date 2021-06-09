#-*- coding : utf-8-*-
# coding:unicode_escape

__mac_address = ''
current_network_interface = ''
begin = True

# Update ip by arp
def update_ip(func):
    import time
    from webium.plugins.networking.Scanners.arp_scanner import ArpScan
    from webium.plugins.networking.Utils.base import Base
    __mac_address = ''

    base: Base = Base(admin_only=True, available_platforms=['Linux', 'Darwin', 'Windows'])
    current_network_interface: str = \
        base.network_interface_selection(interface_name=None,
                                    message='Please select a network interface for script' +
                                        'from table: ')

    def __get_mac(orig_ip, stop_flag):
        # region arp scan
        target_ip = orig_ip
        arp_scan: ArpScan = ArpScan(network_interface=current_network_interface)
        results: List[Dict[str, str]] = arp_scan.scan(timeout=30, retry=10,
                        target_ip_address=target_ip,
                        check_vendor=True, exclude_ip_addresses=None,
                        exit_on_failure=False, show_scan_percentage=True)
        # end region
        # region Print results
        assert len(results) != 0, \
            'Could not find devices in local network on interface: ' + base.error_text(current_network_interface)
        if target_ip is None:
            base.print_success('Found ', str(len(results)), ' alive hosts on interface: ', current_network_interface)
            stop_flag = True
        else:
            base.print_success('Found target: ', target_ip)
            base.print_success('Mac: ', results[0]['mac-address'])
            global __mac_address
            __mac_address = results[0]['mac-address']
            return __mac_address
        # end region

    def __arp_scan(stop_flag, ip):
        arp_scan: ArpScan = ArpScan(network_interface=current_network_interface)
        global __mac_address
        if __mac_address != "":
            ip = arp_scan.get_ip_address(__mac_address)
            return True
        else:
            base.print_error("Can not find Device MAC Address!!")
            return False

    def wrapper(*args, **kwargs):
        try:
            assert 'ip' in kwargs.keys()
            assert 'passwd' in kwargs.keys()
            assert 'sleep' in kwargs.keys()
            assert 'flag' in kwargs.keys()
            assert 'suite_info' in kwargs.keys()
            current_ip = kwargs['ip']
            if begin:
                __get_mac(kwargs['ip'], kwargs['flag'])
            __arp_scan(kwargs['flag'], current_ip)
            print(kwargs['suite_info'])
            func(*args, **kwargs)
            print("Finish arp-scan wrapper")
        except BaseException as e:
            print("webium_pipes_loops: ", e)
    return wrapper
