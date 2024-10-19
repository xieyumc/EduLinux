import os

# 创建共享目录
os.makedirs('./volume/share', exist_ok=True)

# 创建52个学生的独立目录
for i in range(1, 53):
    os.makedirs(f'./volume/student/{i}', exist_ok=True)

print("目录结构创建完成！")