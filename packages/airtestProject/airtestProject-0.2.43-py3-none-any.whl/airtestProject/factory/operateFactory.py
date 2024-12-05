import threading
from abc import ABC, abstractmethod

from airtestProject.abstractBase.OperateBase import OperateABC
from airtestProject.abstractBase.operateBaseImp.airtestOperate import myAirTest
from airtestProject.abstractBase.operateBaseImp.pocoOperate import myPoco
from airtestProject.commons.UWA import CollectWeakWhitelist, SetPruningEnabled
from airtestProject.poco.drivers.unity3d import UnityPoco
from airtestProject.factory.SingletonFactory import SingletonFactory


class AbstractFactory(ABC):
    def __init__(self):
        self._local = threading.local()

    @abstractmethod
    def create_operate_abc(self, **kwargs) -> OperateABC:
        pass


# 具体工厂
class PocoFactory(AbstractFactory, metaclass=SingletonFactory):
    def __init__(self):
        super().__init__()
        self._UnityPoco = None

    def create_operate_abc(self, uwa_cut=False, **kwargs) -> OperateABC:
        if self._UnityPoco is None:
            self._UnityPoco = UnityPoco()
        if not hasattr(self._local, '_PageInstance'):
            self._local._PocoInstance = myPoco(self._UnityPoco)
        if uwa_cut:
            SetPruningEnabled(self._UnityPoco, True)
            CollectWeakWhitelist(self._UnityPoco)
        return self._local._PocoInstance


# 具体工厂
class AirTestFactory(AbstractFactory, metaclass=SingletonFactory):
    def __init__(self):
        super().__init__()

    def create_operate_abc(self, language=None, ocr_match_type=False, **kwargs) -> OperateABC:
        if not hasattr(self._local, '_AirTestInstance'):
            self._local._AirTestInstance = myAirTest(language, True)
        if language is not None:
            self._local._AirTestInstance.set_language(language)
        if ocr_match_type:
            self._local._AirTestInstance.set_ocr_match_type(True)
        else:
            self._local._AirTestInstance.set_ocr_match_type(False)
        return self._local._AirTestInstance


def operate(factory_name="air", **kwargs) -> OperateABC:
    """

    :param factory_name: 工厂名称，可以是poco或air。
    :param kwargs: 可选参数，
    1、language参数，仅生效于air用于设置orc语言。设置后本次运行都为设置的语言，重置需要重新传入。
    2、ocr_match_type生效于air用于设置orc匹配方式，默认为全匹配。设置后本次运行都为设置的模式，重置需要重新传入。
    :return: 返回具体的工厂实例。
    """
    factories = {
        'poco': PocoFactory,
        'air': AirTestFactory
    }
    factory_class = factories[factory_name]
    factory = factory_class()
    product = factory.create_operate_abc(**kwargs)
    return product

# class operateFactoryOut:
#
#
