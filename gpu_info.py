import GPUtil
import time
import psutil

def get_gpu_info():
    Gpus = GPUtil.getGPUs()
    gpulist = []
    GPUtil.showUtilization()

    # 获取多个GPU的信息，存在列表里
    for gpu in Gpus:
        print('gpu.id:', gpu.id)
        print('GPU总量：', gpu.memoryTotal)
        print('GPU使用量：', gpu.memoryUsed)
        print('gpu使用占比:', gpu.memoryUtil * 100)
        # 按GPU逐个添加信息
        gpulist.append([gpu.id, gpu.memoryTotal, gpu.memoryUsed, gpu.memoryUtil * 100])

    return gpulist


if __name__ == '__main__':
    get_gpu_info()