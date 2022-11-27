class ErrorCode:
    SUCC = 0
    ACCOUNT_NOT_EXIST = 1
    ACCOUNT_EXIST = 2
    EMAIL_FORMAT_ERROR = 3
    EMAIL_ACCOUNT_EXIST = 4
    SERVER_ERROR = 5
    DEADLINE_ERROR = 6
    VALUE_NOT_INT = 7
    TARGET_EXIST = 8
    PROBLEM_NUM_OVER = 9
    CODELINE_OVER = 10
    PROBLEM_SUBMIT_OVER = 11
    DATETIME_GAP_SHORT = 12
    RATING_OVER = 13
    RATING_GAP_SMALL = 14
    PK_RATING_OVER = 15
    OPPNENT_NOT_EXIST = 16
    NO_RATING_SCORE = 17
    AVG_PROBLEM_NUM_SMALL = 18
    AVG_CODELINE_NUM_SMALL = 19
    errors = {
        0: "succ",
        1: "leetcode 账号不存在!",
        2: "leetcode 账号已经存在!",
        3: "邮箱格式错误!",
        4: "邮箱或者git账户已经存在，如要更改请联系管理员!",
        5: "服务端错误!",
        6: "目标完成时间设置不合理!",
        7: "目标值必须为整数!",
        8: "你已经有一个同类型未完成的目标了，请先完成它!",
        9: "你当前完成的题目数量已经超过目标值，请重新设置!",
        10: "你当前提交的代码行数已经超过目标值，请重新设置!",
        11: "你当前提交的代码题数已经超过目标值，请重新设置!",
        12: "目标完成时间距离今天太短或者太长，请设置大于等于15天，小于等于365天!",
        13: "你当前的竞赛分数已经超过目标值，请重新设置!",
        14: "你当前的竞赛分数和目标值差距小于50，请重新设置!",
        15: "你当前的竞赛分数已经大于等于对手，请重新设置!",
        16: "你要挑战的人不存在，请重新设置!",
        17: "你还没有参加过周赛，请先参加完一场周赛!",
        18: "日均刷题数量需要大于等于1题",
        19: "日均提交代码量需要大于等于5行"
    }

    @classmethod
    def error_message(cls, err_code):
        if err_code in ErrorCode.errors:
            return ErrorCode.errors[err_code]
        return "未知错误"
