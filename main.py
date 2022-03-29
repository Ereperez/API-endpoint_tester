import api_tester as at
import sys

# https://github.com/camchambers/api-tester
from get_endpoints import get_fps_endpoints, get_bps_endpoints


def main():
    host = 'https://az-bps-rcms.nsqa.se'  # 'https://eu-fps-rcms.nsqa.se/api/browser/index.html#/api/'#"http://localhost:9100/api"
    #   200ok, 204nocontent, 301movedPerm, 400badReq, 401unauth, 403forbidden, 404notfound, 500internalserverr
    code = 401

    headers = {
        'content-type': 'application/json',
        'Accept-Charset': 'UTF-8',
        'X-API-Key': "<api-key-here>"
    }

    #  fps endpoints
    apiTests = set()
    # print("FPS LIST:")
    fps_list = get_fps_endpoints()
    for i in range(len(fps_list)):
        for j in range(len(fps_list[i])):
            if fps_list[i][j] == 'get':
                apiTests.add(at.GetTest(code, fps_list[i][j + 1]))
                #  print(fps_list[i][j] + fps_list[i][j+1])
            elif fps_list[i][j] == 'post':
                #  print(fps_list[i][j] + fps_list[i][j + 1])
                apiTests.add(at.PostTest(code, fps_list[i][j + 1]))

    # print("------------------------------------------------------------------------------------------")
    #  bps endpoints
    # print("BPS LIST:")
    # bps_list = get_bps_endpoints()
    # for i in range(len(bps_list)):
    #     for j in range(len(bps_list[i])):
    #         print(bps_list[i][j])

    print("FPS TEST:")

    apiTester = at.ApiTester(host, apiTests, headers)

    if "-v" in sys.argv:
        apiTester.show_request_responses = True

    if "-vv" in sys.argv:
        apiTester.show_request_responses = True
        apiTester.show_post_data = True

    apiTester.run_tests()


if __name__ == "__main__":
    main()
