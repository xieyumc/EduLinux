#!/usr/bin/env python3

# 先创建一个简单的 my.cnf 文件，用于禁用 Native AIO
with open("my.cnf", "w", encoding="utf-8") as config_file:
    config_file.write(
"""[mysqld]
innodb_use_native_aio = 0
""")

with open("docker-compose.yml", "w", encoding="utf-8") as f:
    # 写头部信息：版本、nginx服务
    f.write(
        """version: '3'
services:
  nginx:
    image: nginx:latest
    container_name: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    network_mode: host
    depends_on:"""
    )

    # 让 nginx depends_on 所有 student{i} 容器
    for i in range(0, 63):
        f.write(f"\n      - student{i}")

    f.write("\n\n")

    # 在循环里，先写 student{i}-mysql，再写 student{i} 容器
    for i in range(0, 63):
        # 第一个容器：student{i}-mysql
        f.write(
f"""  student{i}-mysql:
    image: mysql:latest
    container_name: student{i}-mysql
    environment:
      - MYSQL_ROOT_PASSWORD={i}
      - MYSQL_DATABASE=mydatabase
      - MYSQL_USER=student
      - MYSQL_PASSWORD={i}
    ports:
      - "{31000 + i}:3306"
    volumes:
      - ./my.cnf:/etc/mysql/conf.d/my.cnf:ro
    deploy:
      resources:
        limits:
          cpus: '0.1'
          memory: 512M

"""
        )

        # 第二个容器：student{i}
        f.write(
f"""  student{i}:
    image: student-linux-env
    container_name: student{i}
    ports:
      - "{30000 + i}:7681"
    volumes:
      - ./volume/share:/home/student/share:ro
      - ./volume/student/{i}:/home/student/{i}
    depends_on:
      - student{i}-mysql
    deploy:
      resources:
        limits:
          cpus: '0.1'
          memory: 512M

"""
        )

    # 最后定义 networks
    f.write("networks:\n  webnet:\n")