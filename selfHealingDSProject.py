import random
import argparse
import sys

# --- Node Definition ---
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# --- Linked List Implementation ---
class LinkedList:
    def __init__(self):
        self.head = None
        self.backup = []

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.backup.insert(0, data)

    def display(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        print(" -> ".join(nodes) if nodes else "Empty list")

    def corrupt_node(self):
        if self.head is None:
            print("List is empty, cannot corrupt.")
            return
        length = 0
        current = self.head
        while current:
            length += 1
            current = current.next
        corrupt_pos = random.randint(0, length - 1)
        current = self.head
        for _ in range(corrupt_pos):
            current = current.next
        print(f"Corrupting node at position {corrupt_pos} (data: {current.data})")
        current.data = None

    def break_pointer(self):
        if self.head is None or self.head.next is None:
            print("List too short to break pointer.")
            return
        current = self.head
        while current.next and current.next.next:
            current = current.next
        print(f"Breaking pointer after node with data: {current.data}")
        current.next = None

    def self_heal(self):
        if not self.head:
            print("Healing entire linked list from backup...")
            for val in reversed(self.backup):
                self.insert(val)
            print("Linked list reconstruction complete.")
            return
        current = self.head
        index = 0
        healed = False
        while current:
            if current.data is None and index < len(self.backup):
                print(f"Healing corrupted data at node {index} to {self.backup[index]}")
                current.data = self.backup[index]
                healed = True
            if current.next is None and index + 1 < len(self.backup):
                print(f"Healing broken pointer at node {index}, reconnecting to {self.backup[index + 1]}")
                current.next = Node(self.backup[index + 1])
                healed = True
                current = current.next
            else:
                current = current.next
            index += 1
        if healed:
            print("Healing completed.")
        else:
            print("No issues found.")

# --- Binary Tree Implementation ---
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
        self.backup = []

    def insert(self, data):
        self.backup.append(data)
        def _insert_recursive(node, value):
            if not node:
                return TreeNode(value)
            if value < node.data:
                node.left = _insert_recursive(node.left, value)
            else:
                node.right = _insert_recursive(node.right, value)
            return node
        self.root = _insert_recursive(self.root, data)

    def display(self):
        def _inorder(node):
            return _inorder(node.left) + [str(node.data)] + _inorder(node.right) if node else []
        print("Inorder traversal:", " -> ".join(_inorder(self.root)) if self.root else "Empty tree")

    def corrupt_node(self):
        def _corrupt_random(node):
            if not node:
                return False
            if random.choice([True, False]):
                print(f"Corrupting node with value: {node.data}")
                node.data = None
                return True
            return _corrupt_random(node.left) or _corrupt_random(node.right)
        if not _corrupt_random(self.root):
            print("No node was corrupted.")

    def break_pointer(self):
        print("Simulating pointer break (setting root to None)")
        self.root = None

    def self_heal(self):
        def _rebuild_tree(values):
            bt = BinaryTree()
            for val in values:
                bt.insert(val)
            return bt.root

        if not self.root:
            print("Healing binary tree from backup (root was None)...")
            self.root = _rebuild_tree(self.backup)
            print("Tree reconstruction complete.")
            return

        def _heal(node, backup_values):
            if not node:
                return backup_values
            if node.data is None and backup_values:
                node.data = backup_values.pop(0)
                print(f"Healing null node data to {node.data}")
            elif node.data is not None:
                if node.data in backup_values:
                    backup_values.remove(node.data)
            backup_values = _heal(node.left, backup_values)
            backup_values = _heal(node.right, backup_values)
            return backup_values

        remaining = _heal(self.root, self.backup.copy())
        if len(remaining) == len(self.backup):
            print("No issues found.")
        else:
            print("Healing completed.")

# --- Hash Table Implementation ---
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self.backup = []

    def insert(self, data):
        self.backup.append(data)
        index = hash(data) % self.size
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append(data)
        print(f"Inserted {data} at index {index}")

    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"[{i}]: {bucket if bucket else 'Empty'}")

    def corrupt_node(self):
        for i in range(self.size):
            if self.table[i]:
                print(f"Corrupting index {i} bucket")
                self.table[i] = None
                return
        print("Hash table is empty, nothing to corrupt.")

    def break_pointer(self):
        print("Simulating pointer break by reducing hash table size")
        self.size = max(1, self.size // 2)
        self.table = self.table[:self.size]

    def self_heal(self):
        print("Healing hash table...")
        new_table = [None] * self.size
        for item in self.backup:
            index = hash(item) % self.size
            if new_table[index] is None:
                new_table[index] = []
            if item not in new_table[index]:
                new_table[index].append(item)
        self.table = new_table
        print("Hash table healed from backup.")

# --- CLI ---
def interactive_menu():
    print("Welcome to the Self-Healing Data Structure CLI")
    structure = input("Enter the type of data structure to use (linkedlist, binarytree, hashtable): ").strip().lower()

    if structure == 'linkedlist':
        ds = LinkedList()
    elif structure == 'binarytree':
        ds = BinaryTree()
    elif structure == 'hashtable':
        ds = HashTable()
    else:
        print("Unsupported structure.")
        sys.exit(1)

    while True:
        print("\nChoose an action:")
        print("1. Insert node")
        print("2. Display structure")
        print("3. Corrupt a node")
        print("4. Break a pointer")
        print("5. Heal the structure")
        print("6. Exit")

        choice = input("Enter choice (1-6): ")

        if choice == '1':
            val = input("Enter value to insert: ")
            try:
                val = int(val)
            except:
                pass
            ds.insert(val)
        elif choice == '2':
            print("Current structure:")
            ds.display()
        elif choice == '3':
            ds.corrupt_node()
        elif choice == '4':
            ds.break_pointer()
        elif choice == '5':
            ds.self_heal()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    interactive_menu() 