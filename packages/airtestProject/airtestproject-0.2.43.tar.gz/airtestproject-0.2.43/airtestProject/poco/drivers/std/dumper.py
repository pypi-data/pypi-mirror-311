# coding=utf-8
from airtestProject.poco.freezeui.hierarchy import FrozenUIDumper
from airtestProject.poco.utils.simplerpc.utils import sync_wrapper


class StdDumper(FrozenUIDumper):
    def __init__(self, rpcclient):
        super(StdDumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self, onlyVisibleNode=True):
        return self.rpcclient.call("Dump", onlyVisibleNode)
