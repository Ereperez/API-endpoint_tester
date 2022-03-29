#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#@Filename : api-tester
#@Date : 2022-03-14-15-27
#@Project: apiEndpointTest
#@AUTHOR : epe
"""

import requests
import json
import pandas as pd


class ApiTest:
    path = ''
    expected_status_code = ''

    def __init__(self, expected_status_code, path):
        self.path = path
        self.expected_status_code = expected_status_code


class GetTest(ApiTest):
    request_type = 'GET '

    def __init__(self, expected_status_code, path):
        super().__init__(expected_status_code, path)


class PostTest(ApiTest):
    request_type = 'POST'
    data = {}

    def __init__(self, expected_status_code, path, data={}):
        super().__init__(expected_status_code, path)
        self.data = json.dumps(data)


class ApiTester:
    headers = {}
    api_tests = {}
    show_post_data = False
    show_request_responses = False
    passed = 'pass'
    failed = 'fail'
    df = pd.DataFrame(columns=['result', 'expected_code', 'actual_code', 'request_type', 'endpoint', 'url'])
    # Pandas settings
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    def __init__(self, host, api_tests, headers):
        self.host = host
        self.api_tests = api_tests
        self.headers = headers

    def run_tests(self):
        print("Running tests...")
        # print("Result\t\tExpected\tActual\tType\t\tEndpoint") # enable if printing each result
        # df = pd.DataFrame(columns=['result', 'expected_code', 'actual_code', 'request_type', 'endpoint'])
        # passed = 'pass'
        # failed = 'fail'

        for test in self.api_tests:

            #  url = self.host + "/" + test.path
            url = self.host + test.path

            if isinstance(test, GetTest):
                result = requests.get(url, headers=self.headers)
            elif isinstance(test, PostTest):
                result = requests.post(url, headers=self.headers, data=test.data)
                if self.show_post_data == True:
                    post_data = json.loads(test.data)
                    print("POST data:")
                    print(json.dumps(post_data, indent=4) + "\n")

            if test.expected_status_code == result.status_code:
                self.df.loc[len(self.df.index)] = [self.passed, test.expected_status_code, result.status_code,
                                                   test.request_type, test.path, url]
                # print("[PASS]\t\t{}\t\t{}\t\t{}".format(test.expected_status_code, result.status_code,
                #                                         test.request_type + " " + url))
            else:
                self.df.loc[len(self.df.index)] = [self.failed, test.expected_status_code, result.status_code,
                                                   test.request_type, test.path, url]
                # print("[FAIL]\t\t{}\t\t{}\t\t{}".format(test.expected_status_code, result.status_code,
                #                                         test.request_type + " " + url))

            if isinstance(test, PostTest):
                if self.show_post_data == True:
                    post_data = json.loads(test.data)
                    print("POST data:")
                    print(json.dumps(post_data, indent=4) + "\n")

            if self.show_request_responses == True:
                if result.status_code == 200:
                    print("Response:")
                    parsed = json.loads(result.content)
                    print(json.dumps(parsed, indent=4) + "\n")

        ApiTester.print_df(self)

    def print_df(self):
        print("------------------------------------------------------------------------------------------")
        print("Failed endpoints: ")
        print(self.df[self.df['result'] == self.failed])
        #   print(self.df.loc[self.df['result'] == self.failed])
        print("------------------------------------------------------------------------------------------")
        print("Passed endpoints: ")
        print(self.df[self.df['result'] == self.passed])
        #   print(self.df.loc[self.df['result'] == self.failed])
        print("------------------------------------------------------------------------------------------")
        print("Failed amount: ", len(self.df['result'][self.df['result'] == self.failed]))
        print("Passed amount: ", len(self.df['result'][self.df['result'] == self.passed]))
