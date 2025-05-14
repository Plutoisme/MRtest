# Definition for singly-linked list.

from typing import Optional
class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    # 160 相交链表
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        A, B = headA, headB
        while A != B:
            A = A.next if A else headB
            B = B.next if B else headA
        return A
    

    # 206 反转链表
    def reverseList(self, head: ListNode) -> ListNode:
        # 1 -> 2 -> 3
        # image that: None -> 1 -> 2 -> 3
        cur, pre = head, None
        while cur:
            tmp = cur.next # 暂存后继节点 cur.next
            cur.next = pre # 修改 next 引用指向
            pre = cur      # pre 暂存 cur
            cur = tmp      # cur 访问下一节点
        return pre

    
    def reverseList_recur(self, head: ListNode) -> ListNode:
        def recur(cur, pre):
            if not cur: return pre     # 终止条件
            res = recur(cur.next, cur) # 递归后继节点
            cur.next = pre             # 修改节点引用指向
            return res                 # 返回反转链表的头节点
        
        return recur(head, None)       # 调用递归并返回


    # 234 回文链表
    def isPalindrome(self, head: ListNode) -> bool:
        if not head or not head.next:
            return True  # 空链表或只有一个节点的链表是回文链表

        # Step 1: 使用快慢指针找到链表的中间节点
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: 反转链表的后半部分
        reversed_second_half = self.reverseList(slow)

        # Step 3: 比较前半部分和反转后的后半部分
        first_half, second_half = head, reversed_second_half
        while second_half:  # 注意：后半部分可能比前半部分短
            if first_half.val != second_half.val:
                return False
            first_half = first_half.next
            second_half = second_half.next

        return True

    # 141 环形链表
    def hasCycle(self, head:ListNode) -> bool:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if fast == None : return False
            if slow.val == fast.val and slow.next == fast.next:
                return True
        return False

    # 142 环形链表II
    def detectCycle(self, head: ListNode) -> ListNode:
        if not head or not head.next: return None

        fast, slow = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if fast == slow:
                break
        else:
            return None
        
        slow = head
        while slow:
            if slow == fast:
                return slow
            slow = slow.next
            fast = fast.next

    # 21 合并两个有序列表
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        dummy = ListNode(-1)  # 哨兵节点
        current = dummy

        while list1 or list2:
            if list1 is None:  # 如果 list1 已经为空
                current.next = list2
                break
            elif list2 is None:  # 如果 list2 已经为空
                current.next = list1
                break
            else:
                if list1.val <= list2.val:
                    current.next = list1
                    list1 = list1.next
                else:
                    current.next = list2
                    list2 = list2.next

            current = current.next

        return dummy.next

    # 2 两数相加
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        node1, node2 = l1, l2
        carry = 0  # 初始化进位
        prev = None  # 用于记录最后一个非空节点

        # 遍历两个链表直到两者都为空
        while node1 or node2:
            # 获取当前节点的值（如果链表为空，则值为 0）
            val1 = node1.val if node1 else 0
            val2 = node2.val if node2 else 0

            # 计算当前位的总和
            total = val1 + val2 + carry
            carry = total // 10  # 更新进位
            if node1:  # 如果 node1 不为空，直接更新其值
                node1.val = total % 10
                prev = node1  # 更新最后一个非空节点
                node1 = node1.next
                if node2:
                    node2 = node2.next
            else:  # 如果 node1 已经为空，将结果存储到 node2 中
                prev.next = node2  # 将剩余部分加入到结果链表
                node2.val = total % 10
                prev = node2
                node2 = node2.next

        # 如果还有进位，需要在链表末尾添加一个新节点
        if carry:
            prev.next = ListNode(carry)
        return l1  # 返回结果链表

    # 19 删除链表的倒数第N个结点
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # 哨兵节点
        dummy = ListNode(0)
        dummy.next = head
        
        # 初始化快慢指针
        fast = dummy
        slow = dummy
        
        """
        1 - 2 - 3 - 4 - 5
        1 - 2 - 3 - 5
        """
        # 将 fast 向前移动 n+1 步
        for _ in range(n + 1):
            fast = fast.next
        
        # 同时移动 fast 和 slow，直到 fast 指向链表末尾
        while fast:
            fast = fast.next
            slow = slow.next
        
        # 删除目标节点
        slow.next = slow.next.next
        
        # 返回新的链表头节点
        return dummy.next

    # 24 两两交换链表中的节点
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(-1)
        dummy.next = head
        cur, pre = head, dummy
        while cur:
            if cur.next:
                tmp = cur.next 
                pre.next = tmp
                cur.next = tmp.next    
                tmp.next = cur   
                pre = cur
                cur = cur.next
            else:
                break
        return dummy.next

    # 25 K个一组翻转链表
    def reverseKGroup(self, head, k):
        def reverse_linked_list(start: ListNode, end: ListNode):
            prev = None
            current = start
            while current != end:
                next_node = current.next
                current.next = prev
                prev = current
                current = next_node
            return prev
        
        dummy = ListNode(0)
        dummy.next = head
        prev_group_end = dummy
        
        while True:
            # 尝试找到当前组的第k个节点
            group_start = prev_group_end.next
            group_end = prev_group_end
            for _ in range(k):
                group_end = group_end.next
                if not group_end:
                    return dummy.next
            
            # 保存下一组的起始节点
            next_group_start = group_end.next

            # 翻转当前组
            reverse_linked_list(group_start, group_end.next)
            
            # 连接翻转后的部分
            prev_group_end.next = group_end
            group_start.next = next_group_start

            # 更新 prev_group_end 指针
            prev_group_end = group_start

    # 138 随机链表的复制
    def copyRandomList(self, head):
        if not head:
            return None

        current = head
        # node1 -> node1_copy -> node2 -> node2_copy ......
        while current:
            clone = Node(current.val)
            clone.next = current.next
            current.next = clone
            current = clone.next

        current = head
        # 构建copy的random节点, 注意直接使用current.random.next, 这里的next就直接指向copy的那一部分的节点了。
        while current:
            if current.random:
                current.next.random = current.random.next
            current = current.next.next

        current=head
        clone_head = head.next
        # 将node1 -> node1_copy -> node2 -> node2_copy ...... 拆分成两个链表。
        while current:
            clone = current.next
            current.next = clone.next
            current = current.next
            if clone.next:
                clone.next = clone.next.next

        return clone_head
    
    # 148 排序链表， 归并排序：
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        mid = slow.next
        slow.next = None
        left = self.sortList(head)
        right = self.sortList(mid)

        return self.mergeTwoLists(left, right)

    def mergeTwoLists(self, l1, l2):
        dummy = ListNode(0)
        tail = dummy
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 if l1 else l2
        return dummy.next




if __name__ == "__main__":
    sol = Solution()
    a = ListNode(1)
    b = ListNode(2)
    c = ListNode(4)
    a1 = ListNode(1)
    b1 = ListNode(3)
    c1 = ListNode(4)
    a.next = b
    b.next = c
    a1.next = b1
    b1.next = c1
    
    print(sol.mergeTwoLists(a,a1))
                


    
        