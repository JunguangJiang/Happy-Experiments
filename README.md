# Happy Experiments in Python (HEPY)

### 中文介绍
HE是一个针对命令行实验的管理工具。主要对实验中的三个部分进行管理：
1. 实验代码版本管理。对每个实验（Experiment），HE会维护一个代码版本，用户可以随时切换到过去的代码版本进行实验。
对于需要频繁修改代码的实验而言，HE可以节省实验者大量的精力，同时提高了实验的可复现性。

2. 实验（超）参数管理。每个实验只有一份代码，但是可能包含多个试验（Trial）。
每个试验的命令行参数不同，命令行参数决定了这次试验的实验参数。HE在每次试验的开始，会记录这次试验的超参数。

3. 实验结果的管理。HE可以将实验结果自动保存到对应的实验文件夹下。也支持在实验结果中的评价指标进行正则匹配。

### 安装方式
```shell script
pip install hepy
```
或者
```shell script
pip install git+https://github.com/JunguangJiang/Happy-Experiments.git@master
```

### 使用教程
##### 注意事项 
由于代码版本管理时会复制代码目录下的文件，用户首先需要：
1. 创建.heignore文件，这个文件的语法和.gitignore相似。在进行代码版本管理时，会忽略.heignore中匹配的文件。
2. 确保所有相对路径的数据文件夹都是软连接。否则复制数据文件夹会消耗大量的资源。

##### 正式的教程
1. 进入代码目录下
2. 初始化
    ```shell script
    he init
    ```
    在代码目录下会出现文件夹he_workspace。

3. 运行一个试验
    ```shell script
    he run --exp ${experiment_name} -- ${script}
    ```
    ${experiment_name}是你给这个实验取的名字， ${script}是运行这个实验的脚本。
    比如运行
    ```shell script
    he run --exp test -- ls -l
    ```
    会得到下列输出
    ```text
    Create new experiment: test
    
    Running script: ls -l
    total 44
    ....
    
    Finish experiment: test
    ```
    在he_workspace文件夹下出现了一个新的文件夹test。
    test/code中包含了当前时刻的代码。test/0.txt包含了第一次试验的结果。
    - 如果不指定实验名称，默认会采用当前的时间作为实验名称。
    - 如果指定的实验名称与此前的重复，则会**使用过去实验时刻的代码**。
    
    如果要运行多个试验，则在${script_file}中的每行写一个试验命令，并运行
    ```shell script
    he run --exp ${experiment_name} --script ${script_file}
    ```

4. 展示实验结果
```shell script
he show ${experiment_names}
```

