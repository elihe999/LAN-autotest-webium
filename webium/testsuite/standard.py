from webium.pipes.loops import update_ip
from webium.driver import get_driver
import time
import os
import importlib

_g_default_folder_name = "testcases"
_g_default_suite_list_file = "runsuite.txt"

def report_cache():
    timestamp = time.time()
    cache_name = "result_" + str(timestamp)

def read_suite_list():
    global _g_default_suite_list_file
    suite_list = []
    try:
        f = open(_g_default_suite_list_file, 'r')
        while 1:
            line = f.readline()
            if not line:
                break
            else:
                suite_list.append(line.strip("\n"))
    except:
        pass
    finally:
        return suite_list

def dhcp_testsuite(func):
    _test_result = TestResult()

    def __tick(max, flag):
        _init = 0
        while max > _init and flag == False:
            time.sleep(1)
            _init = _init + 1
        return

    @update_ip
    def __run_loop(*args, **kwargs):
        print("New loop:")
        try:
            model = importlib.import_module(_g_default_folder_name+"."+_test_result.current_case)
            assert 'ip' in kwargs.keys()
            assert 'passwd' in kwargs.keys()
            assert 'sleep' in kwargs.keys()
            assert 'flag' in kwargs.keys()
            if kwargs['flag']:
                print("Stop")
                return
            interal = 0
            print(interal)
            model.testcases(*args, **kwargs)
            while(interal < kwargs['loop']):
                if kwargs['flag']:
                    break
                interal = interal + 1
                # region main
                model.testcases(*args, **kwargs)
                # end region
                # region Sleep
                if kwargs['flag']:
                    break
                if kwargs['sleep'] > 0:
                    __tick(kwargs['sleep'], kwargs['flag'])
                else:
                    print("Default Sleep: 80")
                    __tick(80, kwargs['flag'])
        except BaseException as e:
            print("__run_loop: ", e)
            return None

    def wrapper(*args, **kwargs):
        assert 'ip' in kwargs.keys()
        assert 'passwd' in kwargs.keys()
        assert 'sleep' in kwargs.keys()
        assert 'flag' in kwargs.keys()
        print("======\tTest Suite Begin...\t======")
        global _g_default_folder_name
        testcases = read_suite_list()
        for testr_case_name in testcases:
            case_name, loop_number = testr_case_name.split(",", 1)
            # debug region
            print(case_name)
            # End debug region
            try:
                kwargs['loop'] = int(loop_number)
                print(kwargs['loop'])
                _test_result.current_case = case_name
                print(_test_result.current_case)
                __run_loop(*args, **kwargs)
            except BaseException as e:
                print("webium\testsuite\standard.py: ", repr(e))
        # finish
        print("======\tTest Suite finish...\t======")
        func(*args, **kwargs)
    # RETRUN WARPPER
    return wrapper

class TestResult:
    total_number = 0
    success_number = 0
    failed_number = 0
    date_string = ""
    current_case = ""
