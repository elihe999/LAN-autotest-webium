from webium.pipes.loops import dhcp_loop
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

    @dhcp_loop
    def __run_loop(*args, **kwargs):
        try:
            model = importlib.import_module(_g_default_folder_name+"."+_test_result.current_case)
            time.sleep(int(kwargs['sleep']))
            model.testcases(*args, **kwargs)
            return
        except AttributeError:
            print(AttributeError)
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
            print(loop_number)
            # End debug region
            kwargs['loop'] = int(loop_number)
            _test_result.current_case = case_name
            __run_loop(*args, **kwargs)
        # finish
        print("======\tTest Suite finish...\t======")
        func(*args, **kwargs)

    return wrapper

class TestResult:
    total_number = 0
    success_number = 0
    failed_number = 0
    date_string = ""
    current_case = ""
