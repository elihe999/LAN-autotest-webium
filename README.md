# LAN-autotest-webium

This repo is FORK form Webium [wgnet/webium](https://github.com/wgnet/webium).

Also FORK from Poium [SeldomQA/poium](https://github.com/SeldomQA/wpoium).

Networking part is FORK from Raw-socket.

pip install browsermob-proxy

## Todo

- Test Suite Module
- Screenshot Module
- Request Checking
- Performing
- File Upload / Download
- Error catching

## Configuration

- Preset keyword string
- PO

### preset keyword string

```python
wordlist = cvs_helper.load_custom_loc('preset_elm/my_baidu_example.csv')
```
TODO: 多种后缀

### Page Object (PO)

Using the pytest test suite to run the test case. You can write multiple test cases on one test suite. Todo: Avaliable Module.

## pytest

### pytest ordering

<https://pytest-ordering.readthedocs.io/en/develop/>

## Issue

1. Can not run arp-scan under VPN