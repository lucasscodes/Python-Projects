import random
list = [random.randint(0,50000) for i in range(8923)]
list2 = [random.randint(0,50000) for i in range(67)]
list3 = [random.randint(0,50000) for i in range(49999)]
lists = [None,[],[1],[1,2,3,4],[1,2,3,4,5],[1,2,3,4,5,6],[1,2,3,4,5,6,7],
[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8,9,10,11,12,13,14],list,list2,list3]
tests = []

#Definition for a binary tree node.
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

#Fill the tree with DFS pattern
def fillTree(input: list):
    if input is None or input is []:
        return input
    queue = []
    node = None
    for num in input:
        if node is None: #init 1st node
            root = TreeNode(num)
            node = root
            continue
        if node.left is None: #init 2nd node
            newNode = TreeNode(num)
            node.left = newNode
            queue = queue + [newNode]
            continue
        if node.right is None: 
            newNode = TreeNode(num)
            node.right = newNode
            queue = queue + [newNode]
            continue
        else: #need a new node
            node = queue[0] #always without leaves
            queue = queue[1:]
            newNode = TreeNode(num)
            node.left = newNode
            queue = queue + [newNode]
            continue
    if root is None: return queue
    else: return root

#use all lists to generate a tree and the target ans. for it
for list in lists:
    if list is None: tree = None
    elif list == []: tree = []
    else: tree = fillTree(list)
    if tree == None or tree == []: count = 0
    else: count = len(list)
    tests = tests + [[tree, count]]
print("Compiled testcases!")



#Takes 2*ceil(ld(n))
#Returns MaxHeight and MinHeight from a Node
#Works because a complete tree is garanteed
def heights(root: TreeNode):
    max, min = -1, -1
    root2 = root #save it for the second treeclimb
    while root: #Get maxHeight
        max += 1 #started or reached a Node
        root = root.left
    while root2: #Get minHeight
        min += 1 #started or reached a Node
        root2 = root2.right
    return max, min
#The number of nodes in the tree is in the range [0, 5 * 10^4].
#0 <= Node.val <= 5 * 10^4
#The tree is guaranteed to be complete.
def countNodes(root: TreeNode) -> int:
    #Find the maxDepths left and right in the tree to compare
    maxH, minH = heights(root)
    if maxH == minH: #Check if the last layer is filled
        return 2**(maxH+1)-1 #calc the max nodes for given height
    #Now the last layer must be partially filled

    possible = 2**maxH #how much could fit in the last layer
    n = possible - 1 #start counting all above last layer

    #use a ld(N) search on lowest level to find last elem...
    #but i need also ld(N) steps to get down there => O(ld²(N))
    while root.left != None: #None signals done, there are no more nodes left
        possible = possible>>1 #possibles in subtrees left and right
        #Look at the left subtree to check for heigths
        lmax, lmin = heights(root.left)
        if lmax == 0 and lmin == 0: #Last node found!
            n += possible #should be always 1 here!
            break
        elif lmin == lmax and possible > 1: #left subtree is filled!
            n += possible #add elems found left
            a,b = heights(root.right) #check for more work to do
            if a>b: #if the rest is uneven, there are uncounted nodes
                root = root.right #check the right subtree
                continue
            else: break #this subtree has no uncounted nodes left
        elif lmax > lmin: #!
            root = root.left #go left
            continue
    return n

#Use the compiled testcase list to check for Errors!
m = 1
for tuple in tests:
    verbose = False
    tree, count = tuple[0], tuple[1]
    n = countNodes(tree)
    if n != count: print("Error on {m}! Expected {count}, got {n} instead!")
    elif verbose: print(f"Success on No.{m}! Expected and got:{n}")
    m += 1
print("Tests done!")