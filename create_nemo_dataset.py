import codecs
import json
import os
import shutil

import librosa


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        print(path + ' Creat successfully')
        return True
    else:
        print(path + ' Dir already exists')
        return False


def create_nemo_dataset(_contrast_dict, _wav_dir: str, _output_dir: str = "./wav_dataset", _scale_factor: float = 0.9):
    # 创建输出路径
    mkdir(_output_dir + "train/")
    mkdir(_output_dir + "val/")
    # 输入的音频文件名列表
    wav_list = os.listdir(_wav_dir)
    # 指定json文件
    train_json = codecs.open(_output_dir + "train.json", "w", "utf-8")
    val_json = codecs.open(_output_dir + "val.json", "w", "utf-8")

    # 创建文件名对应标签类型字典
    label_dict = {}
    for key in list(_contrast_dict.keys()):
        label_dict[key] = {"filename_list": [], "train_num": 0, "val_num": 0}
    for filename in wav_list:
        for key in list(_contrast_dict.keys()):
            # if key in filename:
            print(key)
            if filename.replace("\\", "/").split("/")[-1].split("_")[0] is key:
                label_dict[key]["filename_list"].append(filename)
        for key in list(_contrast_dict.keys()):
            label_dict[key]["train_num"] = int(len(label_dict[key]["filename_list"]) * _scale_factor)
    print(label_dict)

    # 根据标签字典复制文件到数据集
    for key in label_dict.items():
        num = 1
        if key[1]["filename_list"]:
            for filename in key[1]["filename_list"]:
                json_basic_dict = {}
                if num <= key[1]["train_num"]:
                    shutil.copy(_wav_dir + filename, _output_dir + "train/")
                    json_basic_dict["audio_filepath"] = _output_dir + "train/" + filename
                    json_basic_dict["duration"] = librosa.get_duration(filename=_wav_dir + filename)
                    json_basic_dict["text"] = _contrast_dict[key[0]]
                    json.dump(json_basic_dict, train_json, ensure_ascii=False)
                    train_json.write("\n")
                else:
                    shutil.copy(_wav_dir + filename, _output_dir + "val/")
                    json_basic_dict["audio_filepath"] = _output_dir + "val/" + filename
                    json_basic_dict["duration"] = librosa.get_duration(filename=_wav_dir + filename)
                    json_basic_dict["text"] = _contrast_dict[key[0]]
                    json.dump(json_basic_dict, val_json, ensure_ascii=False)
                    val_json.write("\n")
                num += 1
    train_json.close()
    val_json.close()


def creat_nemo_dataset_refactor(_contrast_dict, _wav_dir: str, _output_dir: str = "./wav_dataset",
                                _scale_factor: float = 0.9):
    train_path = os.path.join(_output_dir, "train")
    val_path = os.path.join(_output_dir, "val")
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(val_path):
        os.makedirs(val_path)

    train_json = codecs.open(_output_dir + "train.json", "w", "utf-8")
    val_json = codecs.open(_output_dir + "val.json", "w", "utf-8")

    # 构建基础字典
    label_dict = {}
    for key in list(_contrast_dict.keys()):
        label_dict[key] = {"filenames": [], "train_num": 0}

    # 逐类添加文件名到基础字典
    for filename in os.listdir(_wav_dir):
        for key in list(_contrast_dict.keys()):
            if filename.split("_")[0] == key:
                label_dict[key]["filenames"].append(filename)
        for key in list(_contrast_dict.keys()):
            label_dict[key]["train_num"] = int(len(label_dict[key]["filenames"]) * _scale_factor)
    print(label_dict)

    # 根据标签字典复制文件到数据集
    for key in label_dict.items():
        num = 1
        if key[1]["filenames"]:
            for filename in key[1]["filenames"]:
                json_basic_dict = {}
                if num <= key[1]["train_num"]:
                    shutil.copy(os.path.join(_wav_dir, filename), train_path)
                    json_basic_dict["audio_filepath"] = os.path.join(train_path, filename).replace("\\", "/")
                    json_basic_dict["duration"] = librosa.get_duration(filename=_wav_dir + filename)
                    json_basic_dict["text"] = _contrast_dict[key[0]]
                    json.dump(json_basic_dict, train_json, ensure_ascii=False)
                    train_json.write("\n")
                else:
                    shutil.copy(os.path.join(_wav_dir, filename), val_path)
                    json_basic_dict["audio_filepath"] = os.path.join(val_path, filename).replace("\\", "/")
                    json_basic_dict["duration"] = librosa.get_duration(filename=_wav_dir + filename)
                    json_basic_dict["text"] = _contrast_dict[key[0]]
                    json.dump(json_basic_dict, val_json, ensure_ascii=False)
                    val_json.write("\n")
                num += 1
    train_json.close()
    val_json.close()


if __name__ == '__main__':
    # 构建对照字典
    contrast_dict = {
        "cat": "请指出哪个图片的序列号是1",
        "dog": "请指出哪个图片的序列号是2",
        "horse": "请指出哪个图片的序列号是3",
        "person": "请指出哪个图片的序列号是4"}
    # 取出wav文件列表
    wav_dir = "./asr_wavdata/"
    # 语音数据集输出文件夹
    output_dir = "./wav_dataset/"
    # 测试集和验证机拆分比例系数
    scale_factor = 0.9

    create_nemo_dataset(contrast_dict, wav_dir, output_dir, scale_factor)
