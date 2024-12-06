#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import tritonclient.http as httpclient
import json
import traceback
from ultralytics import YOLO

class TritonClient:
    def __init__(self, triton_ip, task, model_name, **kwargs):
        """
        初始化 Triton 客户端。

        :param triton_ip: Triton 服务器的 IP 地址和端口，例如 "localhost:8000"
        :param task: 任务类型，例如 "speech_recognition" 或 "detect"
        :param model_name: 要调用的模型名称
        :param kwargs: 其他任务特定的参数
        """
        self.triton_ip = triton_ip
        self.task = task
        self.model_name = model_name

        if self.task == 'speech_recognition':
            try:
                self.triton_client = httpclient.InferenceServerClient(url=self.triton_ip)
                self.input_name = 'AUDIO_INPUT'
                self.output_name = 'RESULT'
            except Exception as e:
                print(f"Error initializing Triton InferenceClient: {e}")
                self.triton_client = None
        elif self.task == 'detect':
            try:
                # 加载 YOLO 模型，指向 Triton 服务器的 YOLO 模型
                self.yolo_model = YOLO(f"http://{self.triton_ip}/{self.model_name}", task="detect")
            except Exception as e:
                print(f"Error initializing YOLO model: {e}")
                self.yolo_model = None
        else:
            raise ValueError(f"Unsupported task: {self.task}")

    def infer(self, file_path, **args):
        """
        执行推理。

        :param file_path: 要处理的文件路径
        :param args: 其他任务特定的参数
        :return: 推理结果
        """
        if self.task == 'speech_recognition':
            if not self.triton_client:
                print("Triton client is not initialized.")
                return None
            try:
                # 读取音频文件的字节数据
                with open(file_path, 'rb') as f:
                    audio_bytes = f.read()

                inputs = [
                    httpclient.InferInput(self.input_name, [1], "BYTES")
                ]
                inputs[0].set_data_from_numpy(np.array([audio_bytes], dtype=object))

                outputs = [httpclient.InferRequestedOutput(self.output_name)]

                response = self.triton_client.infer(
                    model_name=self.model_name,
                    inputs=inputs,
                    outputs=outputs,
                )

                result = response.as_numpy(self.output_name)[0]
                decoded_result = json.loads(result.decode('utf-8'))

                return decoded_result

            except Exception as e:
                error_msg = traceback.format_exc()
                print(f"Error processing file {file_path}:\n{error_msg}")
                return None

        elif self.task == 'detect':
            if not hasattr(self, 'yolo_model') or self.yolo_model is None:
                print("YOLO model is not initialized.")
                return None
            try:
                results = self.yolo_model.predict(source=file_path, **args)
                return results
            except Exception as e:
                error_msg = traceback.format_exc()
                print(f"Error processing file {file_path}:\n{error_msg}")
                return None
        else:
            print(f"Unsupported task: {self.task}")
            return None
