# 使用Ubuntu作为基础镜像
FROM ubuntu:20.04

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 更新软件包列表并安装必要的软件
RUN apt-get update && apt-get install -y \
    sudo \
    vim \
    wget \
    curl \
    net-tools \
    openssh-server \
    python3 \
    build-essential \
    git \
    cmake \
    make \
    gcc \
    libjson-c-dev \
    libwebsockets-dev

# 创建学生用户并设置密码，指定UID和主目录，并复制初始配置文件
RUN useradd -m -u 1000 -s /bin/bash student && \
    echo "student:student_password" | chpasswd && \
    adduser student sudo && \
    cp -r /etc/skel/. /home/student/ && \
    chown -R student:student /home/student/

# 设置环境变量
ENV HOME=/home/student
ENV LANG en_US.utf8

# 设置工作目录
WORKDIR /home/student

# 安装ttyd（一个Web终端工具）
RUN git clone https://github.com/tsl0922/ttyd.git /opt/ttyd && \
    cd /opt/ttyd && \
    mkdir build && cd build && \
    cmake .. && make && make install

# 切换到学生用户
USER student

# 暴露ttyd使用的端口
EXPOSE 7681

# 设置容器启动时运行的命令，移除 -u 参数
CMD ["ttyd", "--writable", "-p", "7681", "bash"]
