import requests
import json
import time

class deviceAteConn:
    def __init__(self, ip):
        self.ip = ip
        self.s = requests.session()
        self.r = self.s.get('http://' +  self.ip + '/cgi-bin/ateconn', stream=True)
        self.timeout = 12
    
    def __del__(self):
        self.s.close()

    def get_message(self, message):
        since = time.time()
        for line in self.r.iter_lines():
        # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
            print(time.time() - since)
            if (time.time() - since) > self.timeout:
                break
    
    def set_timeout(self, number):
        try:
            float(number)
            self.timeout = number
            return True
        except ValueError:
            print("Ignore wrong timeout number")
            
if __name__ == "__main__":
    my_conn = deviceAteConn("192.168.92.14")
    my_conn.get_message("1")
    del my_conn
    