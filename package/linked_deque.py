# Add methods don't add None (add_to_front, add_to_back) ### Consider revision for certain purposes
# For future use, consider maintaining a size || length field - 10//2024 [this could slow down some methods that are currently quite lean]
from collections.abc import Iterable


class LinkedDeque:
    def __init__(
        self, initial_data: Iterable | None = None, front_or_back: str = "Back"
    ) -> None:  # required
        self.clear()
        if initial_data is not None:
            if front_or_back.lower() == "back":  # this is default behavior
                for each_datum in initial_data:
                    self.add_to_back(each_datum)
            elif front_or_back.lower() == "front":
                for each_datum in initial_data:
                    self.add_to_front(each_datum)

    def __len__(self) -> int:  # O(N)
        got_length = 0
        current_len_node = self.front  # front (1 node visited)
        while current_len_node is not None:  # unless front is None
            got_length += 1
            current_len_node = current_len_node.get_next_node()
        return got_length

    def __getitem__(
        self, index: int
    ) -> any:  # O(N^2) for accessing all data_portions by index
        items = self._items_data_list()
        return items[index]

    def _items_data_list(self) -> list[any]:
        data_list = []
        current_data_node = self.front  # front (1 node visited)
        while current_data_node is not None:  # unless front is None
            data_list.append(current_data_node.data_portion)  # keep going
            current_data_node = current_data_node.get_next_node()
        return data_list

    def __iter__(self):
        return self

    def __next__(self):
        return self.remove_front()

    def __eq__(self, other) -> bool:
        eq_bool = False
        if isinstance(other, self.__class__):
            if len(self) == len(other):
                front_was = self.get_front()  # -> any
                for e_i in range(len(self)):
                    if e_i != 0:
                        self.front_to_back()
                    eq_bool = True
                    for s_item, o_item in zip(iter(self), iter(other)):
                        if s_item != o_item:
                            eq_bool = False
                            break
                    if eq_bool:
                        break
                while (
                    self.get_front() != front_was
                ):  # relies on __eq__ method of data portions
                    self.front_to_back()
        return eq_bool

    def add_to_back(self, new_entry) -> None:  # required
        if (
            new_entry is not None
        ):  # These handle null entries so that methods in client classes can
            # send null entries w/o adding DLNode(data_portion=None)
            if not isinstance(
                new_entry, LinkedDeque.DLNode
            ):  # These might be slowing down methods that use them, maybe add
                # a private method that moves nodes as nodess
                new_node = LinkedDeque.DLNode(data_portion=new_entry)
            else:
                new_node = new_entry
            if self.back is None:
                self.back = new_node
                self.front = self.back
            else:
                new_node.set_previous_node(self.back)
                self.back.set_next_node(new_node)
                self.back = new_node

    def add_to_front(self, new_entry) -> None:  # required
        if (
            new_entry is not None
        ):  # These handle null entries so that methods in client classes can
            # send null entries w/o adding DLNode(data_portion=None)
            if not isinstance(new_entry, LinkedDeque.DLNode):
                new_node = LinkedDeque.DLNode(data_portion=new_entry)
            else:
                new_node = new_entry
            if self.front is None:
                self.front = new_node
                self.back = self.front
            else:
                new_node.set_next_node(self.front)
                self.front.set_previous_node(new_node)
                self.front = new_node

    def get_back(self) -> any:  # required
        return self.back.get_data_portion()

    def get_front(self) -> any:  # required
        if self.front is not None:
            return self.front.get_data_portion()

    def remove_front(self) -> any:  # required
        """this will result in a crash/exception when called on an empty deque.
        I think this is appropriate, otherwise, is None the data_portion returned?
        Given the way this treats None, No, it's not a data_portion, but, returning None might send one up the wrong path in debugging.
        """
        front_node = self.front
        if self.front.get_next_node() is None:
            self.clear()
        else:
            self.front = self.front.get_next_node()
            self.front.set_previous_node(None)
            front_node.set_next_node(
                None
            )  # Bug fix 10/11/2024  # tabbed in 10/13/2024
        return front_node.get_data_portion()

    def remove_back(self) -> any:  # required
        back_node = (
            self.back
        )
        if self.back.get_previous_node() is None:
            self.clear()
        else:
            self.back = self.back.get_previous_node()
            self.back.set_next_node(None)
            back_node.set_previous_node(
                None
            )  # Bug fix 10/11/2024  # tabbed in 10/13/2024
        return back_node.get_data_portion()

    def clear(self) -> None:  # required
        self.front = None
        self.back = None

    def is_empty(self) -> bool:  # required
        return self.front is None and self.back is None

    def front_to_back(self) -> None:
        self.add_to_back(next(self))

    def back_to_front(self) -> None:
        self.add_to_front(self.remove_back())

    def display(self) -> None:  # required
        display_string = "LinkedDeque: "
        display_string = self._display_recursive(display_string, self.front)
        print(display_string)

    def _display_recursive(self, in_string: str, current_node) -> str:
        if current_node is None:
            return in_string
        else:
            return self._display_recursive(
                in_string
                + (", " if current_node is not self.front else "")
                + str(current_node.data_portion),
                current_node.get_next_node(),
            )

    # def get_lambda_data_portion(self, func):  ### re initial thinking, here, make a method that returns a (parameter-defined) statistic
    #     """returns the data_portion of the first data_portion in the deque that satisfies the expression (func)"""
    #     front_was = self.front
    #     lambdaest = None
    #     if len(self) > 1 and not func(front_was):  # O(N)
    #         current = self.front
    #         for l in range(len(self)):
    #             if not func(self.get_front()):
    #                 self.front_to_back()
    #             else:
    #                 lambdaest = current
    #                 break
    #         while self.front is not front_was:
    #             self.front_to_back()
    #     return lambdaest.get_data_portion()
    # # later, activation function of including stocks  # AD325 Project 1 - Capital Gains Tracker

    def count_eq_data_portion(self, datum: any) -> int:  #
        return sum([1 if datum == item else 0 for item in list(iter(self))])  #
        #   Later, to be subsumed by get_lambda_data_portion

    def count_lt_data_portion(self, datum: any) -> int:  #
        return sum([1 if item < datum else 0 for item in list(iter(self))])  #
        #

    def count_gt_data_portion(self, datum: any) -> int:  #
        return sum([1 if item > datum else 0 for item in list(iter(self))])  #

    class DLNode:
        def __init__(
            self, previous_node=None, data_portion=None, next_node=None
        ) -> None:  # required
            self.data_portion = data_portion
            self.previous = previous_node
            self.next = next_node

        def get_data_portion(self) -> any:  # required
            return self.data_portion

        def set_data_portion(self, data_portion: any) -> None:  # required
            self.data_portion = data_portion

        def get_next_node(self):  # -> DLNode  # required
            return self.next

        def set_next_node(self, next_node) -> None:  # required
            self.next = next_node

        def get_previous_node(self):  # -> DLNode  # required
            return self.previous

        def set_previous_node(self, previous_node) -> None:  # required
            self.previous = previous_node
