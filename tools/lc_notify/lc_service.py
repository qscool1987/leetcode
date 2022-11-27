# coding=utf-8
#!/usr/bin/env python
import json
import requests
import settings
from loghandle import logger
import mysql_service
import sys
import mysql_service
import time
import datetime


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
        url = 'https://leetcode.cn/graphql/'
        data = {
            "query": "\n    query userQuestionProgress($userSlug: String!) {\n  userProfileUserQuestionProgress(userSlug: $userSlug) {\n    numAcceptedQuestions {\n      difficulty\n      count\n    }\n    numFailedQuestions {\n      difficulty\n      count\n    }\n    numUntouchedQuestions {\n      difficulty\n      count\n    }\n  }\n}\n    ",
            "variables": {
                "userSlug": user
            }
        }
        res = requests.post(url, data=json.dumps(
            data), headers=self.headers)
        data = res.json()[
            'data']['userProfileUserQuestionProgress']['numAcceptedQuestions']
        if len(data) == 0:
            return None
        line = [0] * \
            (len(mysql_service.MysqlService.USER_LC_DAILY_INFO_FIELDS) - 1)
        line[0] = user
        problems = 0
        for item in data:
            problems += item['count']
        line[1] = problems
        return line

    def check_user_rand_problem_status(self, user, pid, td):
        data = {
            "query": "\n    query recentAcSubmissions($userSlug: String!) {\n  recentACSubmissions(userSlug: $userSlug) {\n    submissionId\n    submitTime\n    question {\n      translatedTitle\n      titleSlug\n      questionFrontendId\n    }\n  }\n}\n    ",
            "variables": {
                "userSlug": user
            }
        }
        res = requests.post(self.url, data=json.dumps(
            data), headers=self.headers)
        # td = str(datetime.date.today())
        pid = str(pid)
        status = 3
        data = res.json()['data']['recentACSubmissions']
        for item in data:
            t = item['submitTime']
            day = datetime.datetime.fromtimestamp(t)
            day = str(day).split(' ')[0]
            if day < td:
                break
            question = item['question']
            fid = question['questionFrontendId']
            if pid == fid:
                status = 2
                break
        return status


if __name__ == '__main__':
    obj = LeetcodeService()

    user = 'smilecode-2'
    id = 1732
