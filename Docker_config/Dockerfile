# 使用Ubuntu作为基础镜像
FROM ubuntu:22.04

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 更新软件包列表并安装必要的软件，包括gdb
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
    gdb \
    libjson-c-dev \
    libwebsockets-dev \
    locales \
    tzdata \
    fonts-wqy-zenhei \
    fonts-wqy-microhei

# 生成并设置UTF-8和中文支持的locale
RUN locale-gen en_US.UTF-8 zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8

# 设置时区为东八区（Asia/Shanghai）
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# 设置环境变量以支持中文显示
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8

# 创建普通用户student和拥有sudo权限的studentroot用户，并设置密码
RUN useradd -m -u 1000 -s /bin/bash student && \
    echo "student:student_password" | chpasswd && \
    useradd -m -u 1001 -s /bin/bash studentroot && \
    echo "studentroot:student_password" | chpasswd && \
    adduser studentroot sudo && \
    cp -r /etc/skel/. /home/student/ && \
    chown -R student:student /home/student/

# 设置环境变量
ENV HOME=/home/student

# 设置工作目录
WORKDIR /home/student

# 安装ttyd（一个Web终端工具）
RUN git clone https://github.com/tsl0922/ttyd.git /opt/ttyd && \
    cd /opt/ttyd && \
    mkdir build && cd build && \
    cmake .. && make && make install

# 切换到普通用户student
USER student

# 暴露ttyd使用的端口
EXPOSE 7681

# 设置容器启动时运行的命令，以普通用户身份登录
CMD ["ttyd", "--writable", "-p", "7681", "bash"]