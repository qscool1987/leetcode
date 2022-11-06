# coding=utf-8
#!/usr/bin/env python
import json
import requests
import settings
from loghandle import logger
import mysql_service
import sys


class LeetcodeService(object):

    def __init__(self):
        self.url = 'https://leetcode.cn/graphql/noj-go/'
        self.headers = {
            "content-type": "application/json",
        }

    def get_user_medal_info(self, user):
        """获取用户当前的奖牌信息"""
        data = {
            "query": "\n    query contestBadge($userSlug: String!) {\n  userProfileUserLevelMedal(userSlug: $userSlug) {\n    current {\n      name\n      obtainDate\n      category\n      config {\n        icon\n        iconGif\n        iconGifBackground\n      }\n      id\n      year\n      month\n      hoverText\n    }\n    next {\n      name\n      obtainDate\n      category\n      config {\n        icon\n        iconGif\n        iconGifBackground\n      }\n      id\n      year\n      month\n      hoverText\n      everOwned\n    }\n  }\n}\n    ",
            "variables": {"userSlug": user}
        }
        res = requests.post(self.url, data=json.dumps(data), headers=self.headers).json()[
            'data']['userProfileUserLevelMedal']['current']
        if res:
            if res['name'] == 'Knight':
                return 1
            elif res['name'] == 'Guardian':
                return 2
        return 0

    def get_user_score_info(self, user):
        """获取用户当前的分数信息"""
        data = {
            "query": "query userContestRankingInfo($userSlug: String!) {\n  userContestRanking(userSlug: $userSlug) {\n    attendedContestsCount\n    rating\n    globalRanking\n    localRanking\n    globalTotalParticipants\n    localTotalParticipants\n    topPercentage\n  }\n  userContestRankingHistory(userSlug: $userSlug) {\n    attended\n    totalProblems\n    trendingDirection\n    finishTimeInSeconds\n    rating\n    score\n    ranking\n    contest {\n      title\n      titleCn\n      startTime\n    }\n  }\n}\n    ",
            "variables": {
                "userSlug": user
            }
        }
        res = requests.post(self.url, data=json.dumps(
            data), headers=self.headers)
        data = res.json().get('data')
        if not data:
            return 0
        data = data.get('userContestRanking')
        if not data:
            return 0
        score = data.get('rating')
        if not score:
            return 0
        return int(score)

    def get_user_lc_stat_info(self, user):
        """获取用户当前的刷题信息"""
        data = {
            "query": "\n    query languageStats($userSlug: String!) {\n  userLanguageProblemCount(userSlug: $userSlug) {\n    languageName\n    problemsSolved\n  }\n}\n    ",
            "variables": {
                "userSlug": user
            }
        }
        res = requests.post(self.url, data=json.dumps(
            data), headers=self.headers)
        data = res.json()['data']['userLanguageProblemCount']
        if not data:
            return None
        t_langinfo = {}
        for item in data:
            t_langinfo[item['languageName']] = item['problemsSolved']
        t_total = 0
        line = [0] * \
            (len(mysql_service.MysqlService.USER_LC_DAILY_INFO_FIELDS) - 1)
        line[0] = user
        for lang in settings.languages:
            t_cnt = 0
            if lang in t_langinfo:
                t_cnt = t_langinfo[lang]
            t_total += t_cnt
        line[1] = str(t_total)
        return line


if __name__ == '__main__':
    obj = LeetcodeService()
    user = 'daydayup'
    # res = obj.get_user_medal_info(user)
    # print(res)
