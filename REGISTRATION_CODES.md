# 注册码功能说明

## 功能概述

本系统新增了注册码功能，用于控制系统的使用权限。每个注册码只能使用一次，使用后会自动标记为已使用状态，防止用户分享注册码。

## 主要特性

- ✅ **唯一性**：每个注册码只能使用一次
- ✅ **安全性**：使用后自动失效，防止分享
- ✅ **易管理**：支持批量生成和统计查看
- ✅ **用户友好**：简洁的验证界面

## 注册码格式

### 普通注册码
- 长度：12位
- 字符集：大写字母和数字
- 避免混淆字符：不包含 0、O、1、I、L
- 示例：`F2N6G8KUQWGN`

### 特殊测试注册码
- **`GODBLESSYOU`** - 永久有效的测试注册码
- 特点：
  - 永远不会失效
  - 大小写不敏感
  - 不会被写入数据库
  - 可以无限次使用
  - 专为开发和测试设计

## 使用流程

### 1. 生成注册码（管理员）

```bash
# 生成5个注册码
python3 generate_codes.py 5

# 查看统计信息
python3 generate_codes.py --stats

# 生成并导出到文件
python3 generate_codes.py 10 --export codes.txt

# 交互式生成
python3 generate_codes.py
```

### 2. 用户使用

1. 打开Streamlit应用：`uv run streamlit run streamlit_app.py`
2. 输入登录后的URL（包含userid参数）
3. 输入有效的注册码（可以使用 `GODBLESSYOU` 进行测试）
4. 点击"开始自动完成"按钮
5. 系统会先验证注册码，然后执行任务
6. **只有任务成功完成后，注册码才会被标记为已使用**

#### 快速测试
- 使用测试注册码：`GODBLESSYOU`
- 此注册码永远有效，可以无限次使用
- 适合开发、测试和演示使用

### 3. 管理和监控

```bash
# 查看所有注册码状态
python3 demo_registration_codes.py

# 查看数据库中的注册码
sqlite3 database.db "SELECT * FROM registration_codes;"
```

## 数据库结构

注册码存储在 `registration_codes` 表中：

```sql
CREATE TABLE registration_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,           -- 注册码
    status TEXT DEFAULT 'unused',        -- 状态：unused/used
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    used_at DATETIME NULL,               -- 使用时间
    used_by TEXT NULL                    -- 使用者标识
);
```

## API 函数

### `generate_registration_code(length=12)`
生成单个注册码

### `create_registration_codes(count)`
批量生成注册码并保存到数据库

### `validate_registration_code(code)`
验证注册码是否有效且未使用

### `mark_registration_code_used(code, used_by=None)`
标记注册码为已使用

### `get_registration_code_stats()`
获取注册码统计信息

## 核心逻辑

### 注册码使用流程

1. **验证阶段**：用户输入注册码和URL后，系统首先验证注册码是否有效且未使用
2. **执行阶段**：验证通过后开始执行自动完成任务
3. **标记阶段**：**只有任务成功完成后**，注册码才会被标记为已使用
4. **失败保护**：如果任务执行失败，注册码保持可用状态，用户可以重新尝试

### 优势

- ✅ **防止无效消耗**：任务失败时注册码不会被浪费
- ✅ **用户友好**：网络问题或其他错误不会导致注册码丢失
- ✅ **公平使用**：只有真正完成任务才消耗注册码
- ✅ **重试机制**：失败后可以使用同一注册码重新尝试

## 安全考虑

1. **防重复使用**：每个注册码成功使用后立即标记为已使用
2. **防暴力破解**：12位随机字符，理论上有 28^12 种组合
3. **使用追踪**：记录使用时间和使用者信息
4. **输入验证**：自动转换为大写并验证格式
5. **任务关联**：注册码只有在任务成功完成后才被消耗

## 故障排除

### 常见问题

1. **注册码无效**
   - 检查注册码是否正确输入
   - 确认注册码未被使用
   - 联系管理员获取新的注册码

2. **数据库错误**
   - 确保 `database.db` 文件存在
   - 检查数据库权限
   - 重新创建数据库表

3. **生成失败**
   - 检查磁盘空间
   - 确认数据库连接正常

### 重置数据库（谨慎操作）

```bash
# 删除所有注册码（谨慎！）
sqlite3 database.db "DELETE FROM registration_codes;"

# 重置自增ID
sqlite3 database.db "DELETE FROM sqlite_sequence WHERE name='registration_codes';"
```

## 示例用法

```python
from utils import create_registration_codes, validate_registration_code, mark_registration_code_used

# 生成10个注册码
codes = create_registration_codes(10)
print(f"生成了 {len(codes)} 个注册码")

# 验证注册码
code = "F2N6G8KUQWGN"
if validate_registration_code(code):
    print("注册码有效")
    # 标记为已使用
    if mark_registration_code_used(code, "user123"):
        print("注册码已使用")
else:
    print("注册码无效或已被使用")
```
