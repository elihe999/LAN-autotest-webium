#-*- coding : utf-8-*-
# coding:unicode_escape

# example
# def deco(func):
#     def wrapper():
#         startTime = time.time()
#         func()
#         endTime = time.time()
#         msecs = (endTime - startTime) * 1000
#         print("time is %d ms" %msecs)
#     return wrapper

# simple loop
def dhcp_loop(func):
    import time
    from webium.plugins.networking.Scanners.arp_scanner import ArpScan
    from webium.plugins.networking.Utils.base import Base
    base: Base = Base(admin_only=True, available_platforms=['Linux', 'Darwin', 'Windows'])
    current_network_interface: str = \
        base.network_interface_selection(interface_name=None,
                                        message='Please select a network interface for script' +
                                            'from table: ')
    __mac_address = ''
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
        # end region

    def __arp_scan(stop_flag, ip) -> bool:
        arp_scan: ArpScan = ArpScan(network_interface=current_network_interface)
        global __mac_address
        if __mac_address != "":
            ip = arp_scan.get_ip_address(__mac_address)
            return True
        else:
            base.print_error("Can not find Device MAC Address!!")
            return False

    def __tick(max, flag):
        _init = 0
        while max > _init and flag == False:
            time.sleep(1)
            _init = _init + 1
        return

    def wrapper(*args, **kwargs):
        assert 'ip' in kwargs.keys()
        assert 'passwd' in kwargs.keys()
        assert 'sleep' in kwargs.keys()
        assert 'flag' in kwargs.keys()
        if kwargs['flag']:
            return
        interal = 0
        base: Base = Base(admin_only=True, available_platforms=['Linux', 'Darwin', 'Windows'])
        __get_mac(kwargs['ip'], kwargs['flag'])
        current_ip = kwargs['ip']
        # while region
        while(interal < kwargs['loop']):
            if kwargs['flag']:
                break
            base.print_info("Current Loop is: " + str(interal))
            interal = interal + 1
            # region main
            __arp_scan(kwargs['flag'], current_ip)
            func(*args, **kwargs)
            # end region
            # region Sleep
            if kwargs['flag']:
                break
            if kwargs['sleep'] > 0:
                __tick(kwargs['sleep'], kwargs['flag'])
            else:
                print("Default Sleep: 80")
                __tick(80, kwargs['flag'])
            # end region
        # end while region
        print("Finish dhcploop wrapper")
        return
    return wrapper

# static url
def static_loop(func):
    pass

# todo: ipv6
def ipv6_loop(func):
    pass