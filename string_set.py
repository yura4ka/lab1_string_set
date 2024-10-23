class ListNode:
    def __init__(self, value: str, next_node=None):
        self.value = value
        self.count = 1
        self.next_node = next_node


class StringSet:
    def __init__(self, capacity=10**6):
        self.__capacity = capacity
        self.__p = 31
        self.__m = 10**9 + 9
        self.__size = 0
        self.__table = [None] * capacity

    def __hash(self, string: str) -> int:
        hash_sum = 0
        p_pow = 1
        for char in string:
            hash_sum = (hash_sum + (ord(char) - ord("a") + 1) * p_pow) % self.__m
            p_pow = (p_pow * self.__p) % self.__m
        return hash_sum % self.__capacity

    def add(self, string: str):
        if len(string) > 15:
            return

        node = self.__get_node(string)
        if node:
            node.count += 1
            return

        index = self.__hash(string)
        new_node = ListNode(string)
        if self.__table[index] is None:
            self.__table[index] = new_node
        else:
            current = self.__table[index]
            new_node.next_node = current
            self.__table[index] = new_node

        self.__size += 1

    def __get_node(self, string: str) -> ListNode | None:
        index = self.__hash(string)
        current = self.__table[index]
        while current:
            if current.value == string:
                return current
            current = current.next_node
        return None

    def __contains__(self, string: str) -> bool:
        return self.__get_node(string) is not None

    def remove(self, string: str):
        index = self.__hash(string)
        current = self.__table[index]
        prev = None

        while current:
            if current.value == string:
                if prev is None:
                    self.__table[index] = current.next_node
                else:
                    prev.next_node = current.next_node
                self.__size -= 1
                return
            prev = current
            current = current.next_node

    def get_groups(self):
        result = {}
        for l in self.__table:
            current = l
            while current:
                if current.count in result:
                    result[current.count].append(current.value)
                else:
                    result[current.count] = [current.value]
                current = current.next_node
        del result[1]
        return result

    def get_z_functions(self):
        result = {}
        for l in self.__table:
            current = l
            while current:
                result[current.value] = self.__z_function(current.value)
                current = current.next_node
        return result

    def __z_function(self, string: str):
        z = [0 for _ in string]
        l, r = 0, 0
        for i in range(1, len(string)):
            if i < r:
                z[i] = min(r - i, z[i - l])
            while i + z[i] < len(string) and string[z[i]] == string[i + z[i]]:
                z[i] += 1
            if i + z[i] > r:
                l = i
                r = i + z[i]
        return z

    def __len__(self):
        return self.__size
