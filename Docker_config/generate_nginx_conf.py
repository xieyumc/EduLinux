with open("nginx.conf", "w") as f:
    # 写入 Nginx 配置头部
    f.write("""user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

""")

    # 写入 server 配置头部
    f.write("""    server {
        listen       80;
        server_name  localhost;
""")

    # 自动生成 location 配置
    for i in range(0, 128):
        # 为 manage 路径生成配置，转发到 localhost:8000
        f.write(f"""
        # student{i} manage
        location /student{i}/manage {{
            proxy_pass http://localhost:8000/student{i}/manage;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }}
""")
        # 为 student 常规路径生成配置，转发到对应的端口
        f.write(f"""
        # student{i}
        location /student{i}/ {{
            proxy_pass http://localhost:{30000 + i}/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }}
""")

    # 写入 Nginx 配置尾部
    f.write("    }\n}\n")