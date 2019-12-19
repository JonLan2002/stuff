#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

import sys
import json
from json.decoder import JSONDecodeError

def check_data(data):
    if not "machines" in data:
        error = {"success": False, "error_code": 2,
                 "error_message": "[]machines is missing."}
    elif not isinstance(data["machines"], list):
        error = {"success": False, "error_code": 2,
                 "error_message": "[]machines must be array."}
    elif not 1 <= len(data["machines"]) <= 100:
        error = {"success": False, "error_code": 2,
                 "error_message": "[]machines must contain between 1 and 100 elements."}
    elif not "C" in data:
        error = {"success": False, "error_code": 2,
                 "error_message": "C is missing."}
    elif not isinstance(data["C"], int):
        error = {"success": False, "error_code": 2,
                 "error_message": "C must be int."}
    elif not 1 <= data["C"] <= 999:
        error = {"success": False, "error_code": 2,
                 "error_message": "C must be between 1 and 999."}
    elif not "P" in data:
        error = {"success": False, "error_code": 2,
                 "error_message": "P is missing."}
    elif not isinstance(data["P"], int):
        error = {"success": False, "error_code": 2,
                 "error_message": "P must be int."}
    elif not 1 <= data["P"] <= 1000:
        error = {"success": False, "error_code": 2,
                 "error_message": "P must be between 1 and 1000."}
    else:
        for element in data["machines"]:
            if not isinstance(element, int):
                error = {"success": False, "error_code": 2,
                         "error_message": "Each element in machines must be int."}
                break
            if not 0 <= element <= 1000:
                error = {"success": False, "error_code": 2,
                         "error_message": "Each element in machines must be between 0 and 1000."}
                break
        else:
            return True, {}
    return False, error

def neax(input_json):
    try:
        input_data = json.loads(input_json)
    except JSONDecodeError:
        error = {"success": False, "error_code": 1, "error_message": "Invalid JSON"}
    else:
        check_result = check_data(input_data)
        if not check_result[0]:
            error = check_result[1]
        else:
            possibilities = list()
            for i in range(len(input_data["machines"])):
                sites = list(input_data["machines"])
                sites[i] -= input_data["C"]
                mo_count = 0
                for site in sites:
                    while site > 0:
                        mo_count += 1
                        site -= input_data["P"]
                possibilities.append(mo_count)
            output_data = {"success": True, "machine_operators": min(possibilities)}
            return True, json.dumps(output_data)
    return False, json.dumps(error)

def aiohttp(argv=None):
    from aiohttp import web
    argv = argv or []
    async def aiohttp_hello(request): # pylint: disable=unused-argument
        return web.Response(text="Hello, world")
    async def aiohttp_neax(request):
        result = neax(await request.text())
        if result[0]: # pylint: disable=no-else-return
            return web.Response(text=result[1], content_type='application/json', status=200)
        else:
            return web.Response(text=result[1], content_type='application/json', status=400)
    app = web.Application()
    app.router.add_get('/', aiohttp_hello)
    app.router.add_post('/', aiohttp_neax)
    if __name__ == '__main__':
        web.run_app(app, port=1337)
    return app

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'stdin':
            # pylint: disable=invalid-name
            input_bytes = sys.stdin.buffer.read()
            input_string = input_bytes.decode()
            output_string = neax(input_string)[1]
            output_bytes = output_string.encode()
            sys.stdout.buffer.write(output_bytes)
        elif sys.argv[1] == 'aiohttp':
            aiohttp()
        else:
            print(neax(sys.argv[1])[1])
    else:
        print('Find the number of Machine Operators')
        print()
        print(f'Usage: ./{__file__} [data]')
        print(f'       ./{__file__} [interface]')
        print()
        print('[interface] can be stdin or aiohttp.')
        print()
        print('Example:')
        print(f'./{__file__} ', """'{"machines": [15, 10], "C": 12, "P":5}'""")
