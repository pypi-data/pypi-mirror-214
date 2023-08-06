from typing import TypeVar, Generic, Optional, Generator

T = TypeVar('T')


class AVLNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.height: int = 1
        self.left: Optional[AVLNode[T]] = None
        self.right: Optional[AVLNode[T]] = None


class AVLSet(Generic[T]):
    def __init__(self):
        self.root: Optional[AVLNode[T]] = None
        self.min_node: Optional[AVLNode[T]] = None
        self.max_node: Optional[AVLNode[T]] = None
        self.size: int = 0

    def insert(self, value: T):
        if not self.root:
            self.root = AVLNode(value)
            self.min_node = self.root
            self.max_node = self.root
            self.size += 1
        else:
            new_root, inserted = self._insert(self.root, value)
            self.root = new_root
            if inserted:
                self.size += 1

                if value < self.min_node.value:
                    self.min_node = self._find_min(self.root)

                if value > self.max_node.value:
                    self.max_node = self._find_max(self.root)

    def remove(self, value: T):
        if self.root:
            new_root, removed = self._remove(self.root, value)
            self.root = new_root
            if removed:
                self.size -= 1

                if value == self.min_node.value:
                    self.min_node = self._find_min(self.root) if self.root else None

                if value == self.max_node.value:
                    self.max_node = self._find_max(self.root) if self.root else None

    def pop(self) -> T:
        return self.pop_min()

    def pop_min(self) -> T:
        if not self.min_node:
            return None
        min_value = self.min_node.value
        self.remove(min_value)
        return min_value

    def pop_max(self) -> T:
        if not self.max_node:
            return None
        max_value = self.max_node.value
        self.remove(max_value)
        return max_value

    def __contains__(self, value: T) -> bool:
        return self._contains(self.root, value)

    def __iter__(self) -> Generator[T, None, None]:
        return self._inorder_traversal()

    def __reversed__(self) -> Generator[T, None, None]:
        return self._reversed_inorder_traversal()

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return bool(self.root)

    def _insert(self, node: AVLNode[T], value: T) -> (AVLNode[T], bool):
        if not node:
            return AVLNode(value), True

        if value < node.value:
            node.left, inserted = self._insert(node.left, value)
        elif value > node.value:
            node.right, inserted = self._insert(node.right, value)
        else:
            return node, False

        return self._adjust_and_balance(node), inserted

    def _remove(self, node: AVLNode[T], value) -> (AVLNode[T], bool):
        if not node:
            return None, False

        if value < node.value:
            node.left, removed = self._remove(node.left, value)
        elif value > node.value:
            node.right, removed = self._remove(node.right, value)
        else:
            if not node.left:
                temp = node.right
                return temp, True
            elif not node.right:
                temp = node.left
                return temp, True

            temp = self._find_min(node.right)
            node.value = temp.value
            node.right, _ = self._remove(node.right, temp.value)
            return self._adjust_and_balance(node), True

        return self._adjust_and_balance(node), removed

    def _adjust_and_balance(self, node: AVLNode[T]) -> AVLNode[T]:
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def _balance(self, node: AVLNode[T]) -> AVLNode[T]:
        balance_factor = self._get_balance_factor(node)

        if balance_factor > 1:
            if self._get_balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance_factor < -1:
            if self._get_balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _rotate_left(self, z: AVLNode[T]) -> AVLNode[T]:
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, y: AVLNode[T]) -> AVLNode[T]:
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    @staticmethod
    def _get_height(node: AVLNode[T]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance_factor(self, node: AVLNode[T]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    @staticmethod
    def _find_min(node: AVLNode[T]) -> AVLNode[T]:
        current = node
        while current.left:
            current = current.left
        return current

    @staticmethod
    def _find_max(node: AVLNode[T]) -> AVLNode[T]:
        current = node
        while current.right:
            current = current.right
        return current

    def _contains(self, node: AVLNode[T], value: T) -> bool:
        if not node:
            return False
        if value < node.value:
            return self._contains(node.left, value)
        elif value > node.value:
            return self._contains(node.right, value)
        else:
            return True

    def _inorder_traversal(self) -> Generator[T, None, None]:
        stack = []
        current = self.root
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def _reversed_inorder_traversal(self) -> Generator[T, None, None]:
        stack = []
        current = self.root
        while stack or current:
            while current:
                stack.append(current)
                current = current.right
            current = stack.pop()
            yield current.value
            current = current.left
