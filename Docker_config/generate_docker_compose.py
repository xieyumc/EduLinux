#!/usr/bin/env python3

with open("docker-compose.yml", "w") as f:
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

    # 让 nginx depends_on 所有 student{i} 容器（如有需要，你也可以改成 depends_on student{i}-mysql）
    for i in range(0, 3):
        f.write(f"\n      - student{i}")

    f.write("\n\n")

    # 在循环里，先写 student{i}-mysql，再写 student{i} 容器
    for i in range(0, 3):
        # 第一个容器：student{i}-mysql
        f.write(
f"""  student{i}-mysql:
    image: mysql:5.7
    container_name: student{i}-mysql
    environment:
      - MYSQL_ROOT_PASSWORD=student_password
      - MYSQL_DATABASE=mydatabase
      - MYSQL_USER=student
      - MYSQL_PASSWORD=student_password
    ports:
      - "{31000 + i}:3306"
    volumes:
      - ./volume/mysql/{i}:/var/lib/mysql
    deploy:
      resources:
        limits:
          cpus: '0.1'
          memory: 128M

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
          memory: 128M

"""
        )

    # 最后定义 networks
    f.write("networks:\n  webnet:\n")