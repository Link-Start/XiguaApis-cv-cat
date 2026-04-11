import json
import re

import requests
from bs4 import BeautifulSoup

from builder.auth import WatermelonAuth
from builder.header import HeaderBuilder
from builder.params import ParamsBuilder


class WatermelonApi:
    base_url = "https://www.ixigua.com"

    def get_user_info(self, home_url, auth):
        AuthorDetailInfo = None
        msg = '成功'
        try:
            headers = HeaderBuilder.build_common_header(home_url).get()
            params = ParamsBuilder.build_get_user_info_param().get()
            response = requests.get(home_url, headers=headers, cookies=auth.cookie, params=params)
            response.encoding = 'utf-8'
            res_text = response.text
            AuthorDetailInfo = re.findall(r'"AuthorDetailInfo":\{(.*?)},', res_text)[0]
            AuthorDetailInfo = '{' + AuthorDetailInfo + '}'
            AuthorDetailInfo = re.sub(r'undefined', 'null', AuthorDetailInfo)
            AuthorDetailInfo = json.loads(AuthorDetailInfo)
        except Exception as e:
            msg = str(e)
        return AuthorDetailInfo, msg


    def get_work_info(self, work_url, auth):
        WorkDetailInfo = None
        msg = '成功'
        try:
            headers = HeaderBuilder.build_common_header(work_url).get()
            params = ParamsBuilder.build_get_work_info_param().get()
            response = requests.get(work_url, headers=headers, cookies=auth.cookie, params=params)
            response.encoding = 'utf-8'
            res_text = response.text
            soup = BeautifulSoup(res_text, 'html.parser')
            script_element = soup.select('script')
            for script in script_element:
                if script.string is not None and '_SSR_HYDRATED_DATA' in script.string:
                    WorkDetailInfo = script.string
                    WorkDetailInfo = re.sub(r'window\._SSR_HYDRATED_DATA=', '', WorkDetailInfo)
                    WorkDetailInfo = re.sub(r'undefined', 'null', WorkDetailInfo)
                    WorkDetailInfo = json.loads(WorkDetailInfo)
                    break
            else:
                raise Exception('未找到视频信息')
        except Exception as e:
            msg = str(e)
        return WorkDetailInfo, msg
    def get_user_work(self, home_url, offset, auth):
        api = '/api/videov2/author/new_video_list'
        WorkList = None
        msg = '成功'
        try:
            user_id = home_url.split('/')[-1].split('?')[0]
            headers = HeaderBuilder.build_common_header(home_url).get()
            params = ParamsBuilder.build_get_user_work_param(user_id, offset).get()
            response = requests.get(self.base_url + api, headers=headers, cookies=auth.cookie, params=params)
            res_json = response.json()
            WorkList = res_json['data']['videoList']
        except Exception as e:
            msg = str(e)
        return WorkList, msg

    def get_user_all_work(self, home_url, auth):
        WorkList = []
        offset = 0
        msg = '成功'
        while True:
            WorkListTemp, msg = self.get_user_work(home_url, offset, auth)
            if WorkListTemp is None or len(WorkListTemp) == 0:
                break
            WorkList.extend(WorkListTemp)
            offset += 30
        return WorkList, msg

    def get_work_out_comment(self, home_url, offset, auth):
        api = '/tlb/comment/article/v5/tab_comments/'
        CommentList = None
        msg = '成功'
        try:
            user_id = home_url.split('/')[-1].split('?')[0]
            headers = HeaderBuilder.build_work_comment_header(home_url).get()
            params = ParamsBuilder.build_get_work_out_comment_param(user_id, offset).get()
            response = requests.get(self.base_url + api, headers=headers, cookies=auth.cookie, params=params)
            res_json = response.json()
            CommentList = res_json['data']
        except Exception as e:
            msg = str(e)
        return CommentList, msg


    def get_work_all_out_comment(self, home_url, auth):
        CommentList = []
        offset = 0
        msg = '成功'
        while True:
            CommentListTemp, msg = self.get_work_out_comment(home_url, offset, auth)
            if CommentListTemp is None or len(CommentListTemp) == 0:
                break
            CommentList.extend(CommentListTemp)
            offset += 10
        return CommentList, msg


    def get_work_inner_comment(self, comment_id, offset, auth):
        api = '/tlb/comment/2/comment/v5/reply_list/'
        CommentList = None
        msg = '成功'
        try:
            headers = HeaderBuilder.build_work_comment_header().get()
            params = ParamsBuilder.build_get_work_inner_comment_param(comment_id, offset).get()
            response = requests.get(self.base_url + api, headers=headers, cookies=auth.cookie, params=params)
            res_json = response.json()
            CommentList = res_json['data']['data']
        except Exception as e:
            msg = str(e)
        return CommentList, msg

    def get_work_all_inner_comment(self, comment_id, auth):
        CommentList = []
        offset = 0
        msg = '成功'
        while True:
            CommentListTemp, msg = self.get_work_inner_comment(comment_id, offset, auth)
            if CommentListTemp is None or len(CommentListTemp) == 0:
                break
            CommentList.extend(CommentListTemp)
            offset += 10
        return CommentList, msg

    def get_work_all_comment(self, home_url, auth):
        CommentList = []
        msg = '成功'
        try:
            CommentList, msg = self.get_work_all_out_comment(home_url, auth)
            for comment in CommentList:
                comment['comment']['reply_list'] = []
                if comment['comment']['reply_count'] > 0:
                    comment_id = comment['id']
                    reply_list, msg = self.get_work_all_inner_comment(comment_id, auth)
                    comment['comment']['reply_list'] = reply_list
        except Exception as e:
            msg = str(e)
        return CommentList, msg


    def search_some(self, query, offset, auth):
        query = requests.utils.quote(query)
        api = f'/api/searchv2/complex/{query}/{offset}'
        WorkList = None
        msg = '成功'
        try:
            headers = HeaderBuilder.build_search_header().get()
            params = ParamsBuilder.build_get_search_param().get()
            response = requests.get(self.base_url + api, headers=headers, cookies=auth.cookie, params=params)
            res_json = response.json()
            WorkList = res_json['data']['data']
        except Exception as e:
            msg = str(e)
        return WorkList, msg

    def search_some_by_num(self, query, num, auth):
        WorkList = []
        offset = 0
        msg = '成功'
        while True:
            WorkListTemp, msg = self.search_some(query, offset, auth)
            if WorkListTemp is None or len(WorkListTemp) == 0:
                break
            WorkList.extend(WorkListTemp)
            offset += 10
            if len(WorkList) >= num:
                break
        return WorkList, msg

if __name__ == '__main__':
    watermelonApi = WatermelonApi()
    watermelonAuth = WatermelonAuth()
    cookie_str = ''
    watermelonAuth.perepare_auth(cookie_str)

    user_url = 'https://www.ixigua.com/home/253336705311643'
    # AuthorDetailInfo, msg = watermelonApi.get_user_info(user_url, watermelonAuth)
    # print(AuthorDetailInfo, msg)

    # WorkList, msg = watermelonApi.get_user_all_work(user_url, watermelonAuth)
    # print(WorkList, msg)

    work_url = 'https://www.ixigua.com/7388479154070487571'
    # WorkDetailInfo, msg = watermelonApi.get_work_info(work_url, watermelonAuth)
    # print(WorkDetailInfo, msg)
    # print(WorkDetailInfo, msg)
    # videoResource = WorkDetailInfo['anyVideo']['gidInformation']['packerData']['video']['videoResource']
    # videoDash = videoResource['dash']
    # if not videoDash is None:
    #     ptk = videoDash['ptk']
    #     main_url = videoDash['dynamic_video']['main_url']
    #     print(aes_decrypt(main_url, ptk))
    #     for video in videoDash['dynamic_video']['dynamic_video_list']:
    #         main_url = video['main_url']
    #         print(aes_decrypt(main_url, ptk))
    # videoNormal = videoResource['normal']
    # if not videoNormal is None:
    #     ptk = videoNormal['ptk']
    #     for k, video in videoNormal['video_list'].items():
    #         print(aes_decrypt(video['main_url'], ptk))

    # work_url = 'https://www.ixigua.com/7387380613373755967'
    # CommentList, msg = watermelonApi.get_work_all_comment(work_url, watermelonAuth)
    # for comment in CommentList:
    #     print(f"{comment['comment']['user_name']}说了{comment['comment']['text']}")
    #     for reply in comment['comment']['reply_list']:
    #         print(f"{reply['user']['name']}回复{reply['content']}")
    #     print('--------------------------')


    # query = '拜登'
    # WorkList, msg = watermelonApi.search_some_by_num(query, 20, watermelonAuth)
    # print(WorkList, msg)
    # print(len(WorkList))