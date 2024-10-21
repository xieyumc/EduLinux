with open("docker-compose.yml", "w") as f:
    f.write(
        """version: '3'
services:
  nginx:
    image: nginx:latest
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    network_mode: host
    depends_on:"""
    )

    # 生成 52 个学生容器
    for i in range(1, 53):
        f.write(f"\n      - student{i}")

    f.write("\n\n")

    for i in range(1, 53):
        f.write(
            f"""  student{i}:
    image: student-linux-env
    container_name: student{i}
    ports:
      - "{30000 + i}:7681"
    volumes:
      - ./volume/share:/home/student/share:ro
      - ./volume/student/{i}:/home/student/{i}
    deploy:
      resources:
        limits:
          cpus: '0.1'
          memory: 128M

"""
        )

    f.write("networks:\n  webnet:\n")