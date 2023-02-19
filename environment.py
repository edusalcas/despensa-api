from despensa.singleton_meta import SingletonMeta
from definitions import MAIN_DIR, TEST_DIR


class Environment(metaclass=SingletonMeta):
    __DEV: int = 0
    __TEST: int = 1

    def __init__(self):
        self.__current_env = self.__DEV

    def get_current_env(self):
        return self.__current_env

    def working_is_dev(self):
        self.__current_env = self.__DEV

    def working_is_test(self):
        self.__current_env = self.__TEST

    def get_working_dir(self):
        if self.__current_env == self.__DEV:
            return MAIN_DIR
        else:
            return TEST_DIR
