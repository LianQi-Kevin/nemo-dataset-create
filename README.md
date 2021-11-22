### 创建nemo训练数据集
创建NVIDIA nemo asr或tts训练所需的数据集和json文件

#### 1. 安装依赖库
```
pip install librosa shutil codecs json
```
#### 2. 修改必要的项
1. 构建对照字典
```
contrast_dict = {"文件名关键词": "标签文字"}
# 例如:
# contrast_dict = {
#     "cat": "请指出哪个图片的序列号是1",
#     "dog": "请指出哪个图片的序列号是2",
#     "horse": "请指出哪个图片的序列号是3",
#     "person": "请指出哪个图片的序列号是4"}
```
2. wav文件位置
`wav_dir = "./asr_wavdata/"`
3. 数据集输出文件夹
`output_dir = "./wav_dataset/"`
4. 测试集和验证集拆分比例系数
`scale_factor = 0.9`
#### 3. 输出的文件夹结构
```
wav_dataset
  ├─ train
  │   ├─ xxx.wav
  │   └─ xxx.wav
  └─ val
      ├─ xxx.wav
      └─ xxx.wav
train.json
val.json
```