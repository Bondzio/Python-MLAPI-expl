#!/usr/bin/env python
# coding: utf-8

# Question 1: 
#     a - /user/rt/courses/
#     b - /user/rt/courses/, cs016/, homeworks/, programs/, cs252/, projects/, papers/, demos/.
#     c - 9
#     d - 1
#     e - grades/ and programs/
#     f - papers/, demos/
#     g - 3
#     h - 5
#     
#   

# Question 2.
# a - 1,2,4,5,3,6,8,9,7,10
# b - 4,5,2,8,9,10,6,7,3.1
# c - 4,2,5,1,8,6,9,3,7,10

# In[2]:


# Question 3.
class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree(object):
    def __init__(self, root):
        self.root = Node(root)
        
    def printtree(self, traversal_type):
        if traversal_type == "preorder":
            return self.preorder_print(tree.root, "")
        elif traversal_type == "inorder":
            return self.inorder_print(tree.root, "")
        elif traversal_type == "postorder":
            return self.postorder_print(tree.root, "")

        else:
            print("traversal type: " + str(traversal_type) + " is not supported.")
            return False

    def inorder_print(self, start, traversal):
        """Left->Root->Right"""
        if start:
            traversal = self.inorder_print(start.left, traversal)
            traversal += (str(start.value) + "-")
            traversal = self.inorder_print(start.right, traversal)
        return traversal

    def preorder_print(self, start, traversal):
        """root -> left -> right"""
        if start:
            traversal += (str(start.value) + "-")
            traversal = self.preorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
        return traversal
       
        traversal = self.inorder_print(start.right, traversal)
        return traversal

    def postorder_print(self, start, traversal):
        """Left->Right->Root"""
        if start:
            traversal = self.postorder_print(start.left, traversal)
            traversal = self.postorder_print(start.right, traversal)
            traversal += (str(start.value) + "-")
        return traversal

 
tree = BinaryTree(1)

tree.root.left = Node(2)
tree.root.left.left = Node(4)
tree.root.left.right = Node(5)
tree.root.right = Node(3)
tree.root.right.left = Node(6)
tree.root.right.right = Node(7)
tree.root.right.left.left = Node(8)
tree.root.right.left.right = Node(9)
tree.root.right.right.right = Node(10)

print("inorder tree: " + (tree.printtree("inorder")))
print("preorder tree: " + (tree.printtree("preorder")))
print("postorder tree: " + (tree.printtree("postorder")))


# In[ ]:




