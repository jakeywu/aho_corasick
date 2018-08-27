import os
import pickle
import codecs


class TrieNode:
    def __init__(self):
        self.success = dict()  # 转移表
        self.failure = None  # 错误表
        self.emits = set()  # 输出表


class CreateAcAutomaton(object):

    def __init__(self, patterns, save_path="  "):
        """
        :param patterns:  模式串列表
        :param save_path:   AC自动机持久化位置
        """
        self._savePath = save_path.strip()
        assert isinstance(self._savePath, str) and self._savePath != ""
        self._patterns = patterns
        if os.path.exists(self._savePath):
            self._root = self.__load_corasick()
        else:
            self._root = TrieNode()
            self.__insert_node()
            self.__create_fail_path()
            self.__save_corasick()

    def __insert_node(self):
        """
        Create Trie
        """
        for pattern in self._patterns:
            line = self._root
            for character in pattern:
                line = line.success.setdefault(character, TrieNode())
            line.emits.add(pattern)

    def __create_fail_path(self):
        """
        Create Fail Path
        """
        my_queue = list()
        for node in self._root.success.values():
            node.failure = self._root
            my_queue.append(node)
        while len(my_queue) > 0:
            gone_node = my_queue.pop(0)
            for k, v in gone_node.success.items():
                my_queue.append(v)
                parent_failure = gone_node.failure

                while parent_failure and k not in parent_failure.success.keys():
                    parent_failure = parent_failure.failure
                v.failure = parent_failure.success[k] if parent_failure else self._root
                if v.failure.emits:
                    v.emits = v.emits.union(v.failure.emits)

    def __save_corasick(self):
        with codecs.open(self._savePath, "wb") as f:
            pickle.dump(self._root, f)

    def __load_corasick(self):
        with codecs.open(self._savePath, "rb") as f:
            return pickle.load(f)

    def search(self, context):
        """"""
        search_result = list()
        search_node = self._root
        for char in context:
            while search_node and char not in search_node.success.keys():
                search_node = search_node.failure
            if not search_node:
                search_node = self._root
                continue
            search_node = search_node.success[char]
            if search_node.emits:
                search_result += search_node.emits
        return search_result


if __name__ == "__main__":
    data = ['誉存', '誉存', '誉存科技', '重庆誉存', "重庆誉存大数据"]
    s = "重庆誉存大数据科技有限公司誉誉存"
    ct = CreateAcAutomaton(data, "model.pkl")
    print(ct.search(s))

