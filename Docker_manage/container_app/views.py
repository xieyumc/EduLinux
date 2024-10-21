import os

import docker
from django.shortcuts import render, redirect, get_object_or_404
import subprocess
from django.shortcuts import redirect
from django.http import HttpResponse

# 初始化 Docker 客户端
client = docker.from_env()

# 展示所有容器
def list_containers(request):
    containers = client.containers.list(all=True)  # 获取所有容器
    container_data = []

    for container in containers:
        try:
            stats = container.stats(stream=False)  # 获取容器的资源使用情况
            memory_usage = stats.get('memory_stats', {}).get('usage', 0) / (1024 * 1024)  # 转为MB
            cpu_percent = stats.get('cpu_stats', {}).get('cpu_usage', {}).get('total_usage', 0)

            container_data.append({
                'id': container.short_id,
                'name': container.name,
                'status': container.status,
                'cpu_percent': cpu_percent,
                'memory_usage': memory_usage,
            })
        except Exception as e:
            print(f"Error retrieving stats for container {container.name}: {str(e)}")

    return render(request, 'containers.html', {'containers': container_data})

# 查看具体容器状态
def container_detail(request, container_name):
    try:
        # 获取容器
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)  # 获取容器资源使用情况

        # 获取当前和上次的 CPU 使用数据
        cpu_stats = stats.get('cpu_stats', {})
        precpu_stats = stats.get('precpu_stats', {})

        # 获取累计 CPU 使用时间
        current_total_usage = cpu_stats.get('cpu_usage', {}).get('total_usage', 0)
        previous_total_usage = precpu_stats.get('cpu_usage', {}).get('total_usage', 0)

        # 获取系统 CPU 使用时间
        current_system_usage = cpu_stats.get('system_cpu_usage', 0)
        previous_system_usage = precpu_stats.get('system_cpu_usage', 0)

        # 获取 CPU 核心数
        cpu_count = len(cpu_stats.get('cpu_usage', {}).get('percpu_usage', []))

        # 计算 CPU 使用率
        cpu_delta = current_total_usage - previous_total_usage
        system_delta = current_system_usage - previous_system_usage
        cpu_percent = 0.0
        if system_delta > 0 and cpu_count > 0:
            cpu_percent = (cpu_delta / system_delta) * cpu_count * 100

        # 获取内存使用情况
        memory_usage = stats.get('memory_stats', {}).get('usage', 0) / (1024 * 1024)  # 转为MB

        # 组装容器的详细数据
        container_data = {
            'id': container.short_id,
            'name': container.name,
            'status': container.status,
            'image': container.image.tags,
            'cpu_percent': round(cpu_percent, 2),  # 四舍五入到2位小数
            'memory_usage': round(memory_usage, 2),
            'logs': container.logs().decode('utf-8'),  # 获取最近10行日志
        }

        return render(request, 'container_detail.html', {'container': container_data})
    except docker.errors.NotFound:
        return HttpResponse(f"Container '{container_name}' not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error retrieving container: {str(e)}", status=500)


# 重启容器
def restart_container(request, container_name):
    try:
        container = client.containers.get(container_name)
        container.restart()  # 重启容器
        return redirect('container_detail', container_name=container_name)
    except docker.errors.NotFound:
        return HttpResponse(f"Container '{container_name}' not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error restarting container: {str(e)}", status=500)



# 重置容器：停止并重新启动 Docker Compose 中的容器
def reset_container(request, container_name):
    try:
        # Get the directory of the current file (views.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the absolute path to the docker-compose.yml file
        compose_file_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'Docker_config', 'docker-compose.yml'))

        # Define the base Docker Compose command with the new file path
        base_command = ['docker', 'compose', '-f', compose_file_path]

        # Stop and remove the container
        subprocess.run(base_command + ['stop', container_name], check=True)
        subprocess.run(base_command + ['rm', '-f', container_name], check=True)

        # Start the container
        subprocess.run(base_command + ['up', '-d', container_name], check=True)

        # Redirect back to the container detail page
        return redirect('container_detail', container_name=container_name)

    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Error resetting container: {str(e)}", status=500)