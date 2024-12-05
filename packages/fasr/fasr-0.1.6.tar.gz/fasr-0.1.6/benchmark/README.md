## fasr benchmark


## 双通道音频

###  pipeline

**vad->asr->punc**

运行命令
```
fasr benchmark pipeline ./data/zhuzhan.txt --batch_size 10 --batch_size_s 100
```

测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|368.8s|46.34| 1.0|
|fasr|153.92s|111.03| 2.4|


###  vad

运行命令
```
fasr benchmark vad ./data/zhuzhan.txt --batch_size 10
```

测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|219.8s|77.75| 1.0|
|fasr|86.32s|197.98| 2.55|


## 单通道音频

###  pipeline

**vad->asr->punc**

运行命令
```
fasr benchmark pipeline ./data/dantongdao.txt --batch_size 10 --batch_size_s 100
```

测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|123.8s|22.05| 1.0|
|fasr|59.04s|46.24| 2.1|


###  vad

运行命令
```
fasr benchmark vad ./data/dantongdao.txt --batch_size 10
```

测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|59.26s|46.07| 1.0|
|fasr|36.84s|74.1| 1.61|


## AISHELL

###  pipeline

**vad->asr->punc**

测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|123.8s|18.65| 1.0|
|fasr|59.04s|32.71| 1.8|

