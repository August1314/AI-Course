# 生成父句引用标识符（用于步骤显示）
def get_parent_reference(clause_id, clause_length, pos):
    # 若子句长度>1，则用字母标记文字位置（如1a,1b），否则直接用子句ID
    if clause_length > 1:
        return f"{clause_id}{chr(97 + pos)}"  # 使用ASCII码生成a,b,c后缀
    else:
        return str(clause_id)

# 判断两个文字是否互补（如A与¬A）
def is_complement(lit1, lit2):
    # 处理两种互补情况：lit1是¬lit2 或 lit2是¬lit1
    if lit1.startswith('～'):
        return lit1[1:] == lit2  # 检查去否定后是否相等
    elif lit2.startswith('～'):
        return lit2[1:] == lit1
    else:
        return False

# 对两个子句执行归结操作，返回所有可能的归结结果
def resolve(c1, c2):
    resolved_clauses = []
    c1_id = c1['id']
    c2_id = c2['id']
    # 遍历两个子句的所有文字组合
    for i, lit1 in enumerate(c1['clause']):
        for j, lit2 in enumerate(c2['clause']):
            if is_complement(lit1, lit2):
                new_clause = []
                # 合并两个子句的非互补文字（并去重）
                # 处理第一个子句的文字
                for lit in c1['clause']:
                    if lit != lit1:  # 排除互补文字
                        if lit not in new_clause:  # 去重
                            new_clause.append(lit)
                # 处理第二个子句的文字
                for lit in c2['clause']:
                    if lit != lit2:  # 排除互补文字
                        if lit not in new_clause:  # 去重
                            new_clause.append(lit)
                # 生成父句引用标识符（如R[1a,2b]）
                ref1 = get_parent_reference(c1_id, len(c1['clause']), i)
                ref2 = get_parent_reference(c2_id, len(c2['clause']), j)
                # 按子句ID排序确保引用顺序一致
                if c1_id < c2_id:
                    step_ref = f"{ref1}, {ref2}"
                else:
                    step_ref = f"{ref2}, {ref1}"
                step_str = f"R[{step_ref}]"
                # 存储归结结果
                resolved_clauses.append({
                    'clause': new_clause,
                    'step_str': step_str
                })
    return resolved_clauses

# 命题逻辑归结算法主函数
def ResolutionProp(KB):
    # 初始化子句库
    clauses = []
    current_id = 1  # 子句唯一ID生成器
    # 转换输入为规范格式（去重且保留顺序）
    for clause in KB:
        unique_clause = list(dict.fromkeys(clause))  # 利用字典键去重保留顺序
        clauses.append({
            'id': current_id,
            'clause': unique_clause,
            'parents': None  # 初始子句无父节点
        })
        current_id += 1
    
    # 使用集合记录已存在的子句（用于快速查重）
    existing_clauses = set()
    for clause in clauses:
        clause_tuple = tuple(clause['clause'])  # 列表不可哈希，转为元组
        existing_clauses.add(clause_tuple)
    
    steps = []    # 记录推导步骤
    queue = clauses.copy()  # 使用队列实现广度优先搜索
    
    # 主循环：处理所有可能的归结组合
    while queue:
        c1 = queue.pop(0)  # 取出队列首个子句
        # 与所有已知子句进行归结尝试
        for c2 in clauses:
            if c1['id'] == c2['id']:  # 跳过自身
                continue
            # 执行归结操作
            resolved_list = resolve(c1, c2)
            # 处理每个归结结果
            for resolved in resolved_list:
                new_clause = resolved['clause']
                step_str = resolved['step_str']
                # 检查是否得到空子句（矛盾）
                if not new_clause:
                    step = f"{step_str} = ()"  # 空子句标记
                    steps.append(step)
                    return steps  # 发现矛盾立即返回
                # 检查是否为新子句
                new_tuple = tuple(new_clause)
                if new_tuple not in existing_clauses:
                    # 创建新子句条目
                    new_clause_entry = {
                        'id': current_id,
                        'clause': new_clause,
                        'parents': (c1, c2)  # 记录父节点
                    }
                    current_id += 1
                    # 更新数据存储
                    clauses.append(new_clause_entry)
                    existing_clauses.add(new_tuple)
                    queue.append(new_clause_entry)  # 新子句加入处理队列
                    # 生成可读步骤字符串
                    clause_str = ", ".join(new_clause) if new_clause else ""
                    step = f"{step_str} = ({clause_str})"
                    steps.append(step)
    
    return steps  # 未发现矛盾时返回所有步骤

# 示例：验证三段论
# 已知：1.是一年级学生 2.如果是一年级学生则是儿童 3.不是儿童
# 预期推导出矛盾
KB = [
    ['FirstGrade'],
    ['～FirstGrade', 'Child'],
    ['～Child']
]

result = ResolutionProp(KB)
for step in result:
    print(step)