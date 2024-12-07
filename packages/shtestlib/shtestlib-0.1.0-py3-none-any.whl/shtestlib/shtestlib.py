class Shtestlib:
    def __init__(self, tenant_key=""):
        # 변수 은닉화
        self.__TEST_MSG = "ai lab is best"

    def test(self, input: str):
        return "Hello {}. {}".format(input, self.__TEST_MSG)
