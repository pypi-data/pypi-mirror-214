# 计算机登录用户: jk
# 系统日期: 2023/6/16 15:09
# 项目名称: chipeak_cv_data_tool
# 开发者: zhanyong
"""
使用扫描线算法和线段树判断矩形框是否相交了
"""


class SegmentTree:
    def __init__(self, n):
        self.tree = [0] * (4 * n)

    def update(self, i, l, r, ql, qr, v):
        if ql <= l and r <= qr:
            self.tree[i] = max(self.tree[i], v)
        elif l <= qr and ql <= r:
            mid = (l + r) // 2
            self.update(i * 2, l, mid, ql, qr, v)
            self.update(i * 2 + 1, mid + 1, r, ql, qr, v)
            self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])

    def query(self, i, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.tree[i]
        elif l <= qr and ql <= r:
            mid = (l + r) // 2
            return max(self.query(i * 2, l, mid, ql, qr),
                       self.query(i * 2 + 1, mid + 1, r, ql, qr))
        else:
            return 0
