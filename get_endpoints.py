#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#@Filename : get_endpoints
#@Date : 2022-03-15-09-53
#@Project: apiEndpointTest
#@AUTHOR : epe
"""
import json
from urllib.request import urlopen
import requests
import pandas as pd


def get_fps_endpoints():
    url_fps = 'http://localhost:9100/api/v2/api-docs'
    r1 = requests.get(url_fps)
    fps_json = r1.json()['paths']
    data = [[]]
    for paths in fps_json:
        for call in fps_json[f'{paths}']:
            #   print(f'call: {call} endpoint: {paths}')
            data.append([call, paths])

    #   print(fps_path_list)
    return data


def get_bps_endpoints():
    url_bps = 'http://localhost:9102/api/v2/api-docs'
    r2 = requests.get(url_bps)
    bps_json = r2.json()['paths']
    data = [[]]
    for paths in bps_json:
        for call in bps_json[f'{paths}']:
            #   print(f'call: {call} endpoint: {paths}')
            data.append([call, paths])

    #   print(fps_path_list)
    return data
