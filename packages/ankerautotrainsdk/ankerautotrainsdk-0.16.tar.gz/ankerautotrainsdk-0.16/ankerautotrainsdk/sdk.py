import logging
import requests
import hashlib
import os
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from os.path import join, dirname, abspath, basename, exists
from typing import Optional, Dict, Any
from os import makedirs
from .types import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnkerAutoTrainSDK:
    def __init__(self, url="https://dataloop.anker-in.com"):
        self.url = url
        self.logger = logging.getLogger(__name__)

    def _calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except IOError as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        return hash_md5.hexdigest()

    def _query_origin_data(self, query_data: dict) -> dict:
        try:
            url = f"{self.url}/query_origin_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=query_data)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while querying origin data: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")

    def _summarize_and_download(self, dataset_name: str, dataset_version: str) -> SummaryAndDownloadDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/summarize_and_download"
            headers = { 'accept': 'application/json', 'Content-Type': 'application/json' }
            dataset_list = [{"datasetName": dataset_name, "datasetVersion": dataset_version}]
            dataset_info = {"dataset": dataset_list}
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return SummaryAndDownloadDataSetResponse(
                url=response.get("url", ""),
                bucket=response.get("bucketName", ""),
                object_name=response.get("objectName", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while summarizing and downloading dataset: {e}")

    def upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        try:
            url = f"{self.url}/get_upload_url"
            file_name = basename(file_path)
            response = requests.post(url, params={"directory": directory, "file_name": file_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while getting upload URL: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting upload URL: {e}")

        try:    
            upload_url = response.get("url")  # 从响应中获取上传URL
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # 计算文件的MD5
            # 然后put到这个路径
            with open(file_path, "rb") as f:
                res = requests.put(upload_url, data=f)
                res.raise_for_status()  # 检查HTTP错误
                return UploadFileResponse(
                    url=upload_url,
                    bucket=response.get("bucket", ""),
                    storage_id=response.get("storage_id", ""),
                    object_name=response.get("object_name", ""),
                    uid=file_md5
                )
        except requests.exceptions.RequestException as e:
            if res is None:
                raise Exception(f"HTTP error occurred while uploading file: {e}")
            detail = res.json().get("detail")
            raise Exception(f"HTTP error occurred while uploading file: {detail}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")

    def upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/upload_raw_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=raw_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadRawDataResponse(
                raw_data_id=response.get("raw_data_id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while uploading raw data: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while uploading raw data: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")

    def upload_annotated_data(self, annotated_data: dict) -> UploadAnnotationDataResponse: 
        try:
            url = f"{self.url}/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=annotated_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadAnnotationDataResponse( 
                annotation_data_id=response.get("id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while uploading annotated data: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while uploading annotated data: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")

    def download_file_by_storage(self, storage_id: str, bucket: str, object_name: str, directory: str) -> str:
        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while getting download URL: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

        try:
            download_url = response.get("url")  # 从响应中获取下载URL
            if not download_url:
                raise Exception("No download URL found in the response.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while downloading file: {detail}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")

    def download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self._query_origin_data(query_origin_data)

            if not origin_data:  # 检查origin_data是否为空
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if not records or len(records) == 0:  # 检查records是否为空
                raise Exception("No origin data found for the given UID.")

            record = records[0]  # 获取第一个记录
            get_uid = record.get("uid")
            if not get_uid or get_uid != uid:
                raise Exception("UID mismatch.")
            storage = record.get("storage")
            storage_id = storage.get("storageId")
            bucket = storage.get("bucket")
            object_name = storage.get("objectName")
            if not storage_id or not bucket or not object_name:
                raise Exception("Missing storage_id, bucket or object_name in origin data.")
            return self.download_file_by_storage(storage_id, bucket, object_name, directory)  # 调用原始下载方法
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

    def create_dataset(self, dataset_info: dict) -> CreateDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/version"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 棃查HTTP错误
            response = response.json()
            return CreateDataSetResponse(
                dataset_id=response.get("dataset_version_id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while creating dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while creating dataset: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while creating dataset: {e}")

    def link_dataset(self, annotation_id_list: list, dataset_id: str) -> dict:
        try:
            # 去除annotation_id_list中的重复元素
            unique_annotation_id_list = list(set(annotation_id_list))

            url = f"{self.url}/data/annotation/link"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            dataset_info = {
                "annotationIds": unique_annotation_id_list,
                "annotationVersionId": dataset_id
            }
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while linking dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while linking dataset: {detail}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while linking dataset: {e}")

    def download_dataset(self, dataset_name: str, dataset_version: str, directory: str) -> str:
        try:
            download_response = self._summarize_and_download(dataset_name, dataset_version)

            download_url = download_response.url  # 从响应中获取下载URL
            download_object_name = download_response.object_name
            if not download_url:
                raise Exception("No download URL found in the download_dataset.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, download_object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is None:
                raise Exception(f"HTTP error occurred while downloading dataset: {e}")
            detail = response.json().get("detail")
            raise Exception(f"HTTP error occurred while downloading dataset: {detail}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading dataset: {e}")

    def batch_download_annotation4human(
        self, req: dict, file_path="./data.json", num_threads: int = 4
    ) -> str:
        """创建数据集

        Args:
            req (dict): 请求参数
            file_path (str): 输出文件路径
            num_threads (int, optional): 线程数量. Defaults to 4.

        Returns:
            str: 处理结果
        """
        logger = self.logger
        logger.info("开始处理数据集创建请求...")

        param = CreateDatasetRequest.model_validate(req)
        multi_query_data = []

        # 处理多标签查询
        if param.mutipleLabelQuery:
            for i in param.mutipleLabelQuery:
                query_data = param.model_dump()
                if i.get("label"):
                    query_data["labelQuery"] = {
                        "label": i.get("label", ""),
                    }
                multi_query_data.append(query_data)

        query_data = param.model_dump()
        multi_query_data = [query_data] if len(multi_query_data) == 0 else multi_query_data

        # 查询总数
        logger.info("开始查询标注数据总数...")
        label_count = 0
        for i in tqdm(multi_query_data, desc="查询数据总数"):
            try:
                data = requests.post(f"{self.url}/data/annotation/query", json=i)
                data.raise_for_status()
                data = data.json()
                if data["total"] > 0:
                    i["total_count"] = int(data["total"])
                    label_count += int(data["total"])
            except Exception as e:
                logger.error(f"查询总数失败: {str(e)}")
                continue

        logger.info(f"找到总计 {label_count} 条标注数据")

        # 分页查询数据
        page_size = 1000
        annotation_data = []

        def fetch_page_data(args):
            query, page = args
            current_query = query.copy()  # 创建查询参数的副本
            current_query["limit"] = page_size
            current_query["skip"] = (page - 1) * page_size
            try:
                data = requests.post(
                    f"{self.url}/data/annotation/query_no_total", json=current_query
                )
                data.raise_for_status()
                return data.json()["records"]
            except Exception as e:
                logger.error(f"获取页面 {page} 数据失败: {str(e)}")
                return []

        logger.info("开始分页获取标注数据...")
        all_page_args = []

        # 收集所有查询的分页参数
        for query in multi_query_data:
            if "total_count" in query:
                total_pages = (query["total_count"] + page_size - 1) // page_size
                page_args = [(query, page) for page in range(1, total_pages + 1)]
                all_page_args.extend(page_args)

        # 使用线程池并行处理所有页面
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = list(
                tqdm(
                    executor.map(fetch_page_data, all_page_args),
                    total=len(all_page_args),
                    desc="获取标注数据",
                )
            )
            for result in results:
                if result:
                    annotation_data.extend(result)

        logger.info(f"成功获取 {len(annotation_data)} 条标注数据")

        # 获取原始数据ID
        raw_data_ids = list(
            set(
                item["dataId"][0]
                for item in annotation_data
                if item.get("dataId") and len(item["dataId"]) > 0
            )
        )

        def fetch_raw_data_batch(id_batch):
            """批量获取原始数据
            
            Args:
            id_batch (list): UID列表
            """
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    data = requests.post(
                    f"{self.url}/batch_query_origin_data", json={"uids": id_batch}
                    )
                    data.raise_for_status()
                    return data.json()["records"]
                except Exception as e:
                    logger.error(f"批量获取原始数据失败: {str(e)}, UIDs: {id_batch[:5]}... 尝试次数: {attempt + 1}")
                    if attempt == max_retries - 1:  
                        return []

        logger.info(f"开始获取原始数据，共 {len(raw_data_ids)} 条...")
        raw_data = []
        # 将ID列表分割成批次
        id_batches = [
            raw_data_ids[i:i + page_size] 
            for i in range(0, len(raw_data_ids), page_size)
        ]
        with ThreadPoolExecutor(max_workers=num_threads * 10) as executor:
            results = list(
                tqdm(
                    executor.map(fetch_raw_data_batch, id_batches),
                    total=len(id_batches),
                    desc="获取原始数据",
                )
            )
            # 展平结果列表
            for batch_result in results:
                if batch_result:
                    raw_data.extend(batch_result)

        logger.info(f"成功获取 {len(raw_data)} 条原始数据")

        # 保存数据到文件
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"originalData": raw_data, "annotationData": annotation_data},
                    f,
                    ensure_ascii=False,
                )
            logger.info(f"数据已保存到文件: {file_path}")
        except Exception as e:
            logger.error(f"保存数据到文件失败: {str(e)}")

        logger.info("数据集创建完成!")
        return raw_data


class AnkerAutoTrainModelSDK:
    def __init__(self, url: str = 'https://aidc-us.anker-in.com'):
        """初始化 AnkerAutoTrainModelSDK 类，设置基础 URL 和会话"""
        self.url = url.rstrip('/')  # 确保基URL没有尾部斜杠
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        # 其他可能的 URL 作为注释
        # self.url = 'https://aidc-dev.anker-in.com'

    def get_url(
        self, 
        model_name: str, 
        model_version_name: str, 
        path: str, 
        url_type: str, 
        interface: str = '/api/model/internal/getUploadUrl'
    ) -> Optional[str]:
        """获取上传文件的 URL

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param path: 文件路径
        :param url_type: URL 类型，例如 "upload"
        :param interface: API 接口路径
        :return: 上传 URL 或 None
        """
        url_interface = f"{self.url}{interface}"
        print(f"请求上传 URL 的接口: {url_interface}")

        payload = {
            "modelName": model_name,
            "modelVersionName": model_version_name,
            "type": url_type,
            "path": path
        }
        print(f"获取上传 URL 的请求体: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url_interface, json=payload)
            response.raise_for_status()  # 如果响应状态码不是200，将引发HTTPError
            response_data = response.json()
            print(f"获取上传 URL 的响应: {json.dumps(response_data, indent=4)}")

            if response_data.get('ok'):
                upload_url = response_data.get('data')
                if upload_url:
                    return upload_url
                else:
                    print("响应中未包含上传 URL。")
                    return None
            else:
                print(f"获取上传 URL 失败: {json.dumps(response_data, indent=4)}")
                return None
        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在获取上传 URL 时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在获取上传 URL 时: {req_err}")
            return None
        except Exception as e:
            print(f"获取上传 URL 时发生未知错误: {e}")
            return None

    def _upload_file(self, upload_url: str, file_path: str) -> bool:
        """上传文件到指定的 URL

        :param upload_url: 上传的 URL
        :param file_path: 文件路径
        :return: 上传成功返回 True，否则返回 False
        """
        print(f"开始上传文件到: {upload_url}")
        try:
            with open(file_path, 'rb') as file:
                headers = {'Content-Type': 'application/octet-stream'}
                response = self.session.put(upload_url, data=file, headers=headers)
                response.raise_for_status()
                print(f"文件成功上传到 {upload_url}")
                return True
        except FileNotFoundError:
            print(f"文件未找到，路径: {file_path}")
            return False
        except requests.HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else '未知'
            print(f"HTTP 错误发生在文件上传时: {http_err} - 状态码: {status_code}")
            return False
        except requests.RequestException as req_err:
            print(f"请求异常发生在文件上传时: {req_err}")
            return False
        except Exception as e:
            print(f"上传文件时发生未知错误: {e}")
            return False

    def _upload_one_file(self, model_name: str, model_version_name: str, file_path: str) -> Optional[str]:
        """上传单个文件，并返回上传的 URL

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param file_path: 文件路径
        :return: 上传 URL 或 None
        """
        upload_url = self.get_url(
            model_name=model_name, 
            model_version_name=model_version_name, 
            path=file_path, 
            url_type="upload"
        )
        if upload_url:
            success = self._upload_file(upload_url, file_path)
            if success:
                print(f"文件上传成功。上传 URL: {upload_url}")
                return upload_url
            else:
                print("文件上传失败。")
                return None
        else:
            print("获取上传 URL 失败，无法上传文件。")
            return None

    def upload_model_file(self, model_name: str, model_version_name: str, file_path: str) -> Dict[str, Any]:
        """
        上传模型文件并返回包含上传 URL 的字典。

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param file_path: 文件路径
        :return: 字典 { "model_name:model_version_name": upload_data }
        """
        upload_data = self._upload_one_file(model_name, model_version_name, file_path)
        key = f"{model_name}:{model_version_name}"
        result = {key: upload_data}
        if upload_data:
            print(f"上传结果: {json.dumps(result, indent=4)}")
        else:
            print(f"上传失败，模型: {key}")
        return result

    def download_model_file(self, model_name: str, model_version_name: str, file_path: str, save_to: str) -> bool:
        """
        获取模型文件的下载链接并下载文件到本地

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param file_path: 服务器上文件的路径
        :param save_to: 本地保存路径
        :return: 下载结果（成功或失败信息）
        """
        url = f"{self.url}/api/model/internal/getUploadUrl"
        payload = {
            "modelName": model_name,
            "modelVersionName": model_version_name,
            "type": "download",
            "path": file_path
        }

        print(f"请求下载 URL 的接口: {url}")
        print(f"获取下载 URL 的请求体: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"获取下载 URL 的响应: {json.dumps(response_data, indent=4)}")

            if response_data.get("code") == 0 and response_data.get("ok"):
                download_url = response_data["data"]
                print(f"Download URL obtained: {download_url}")

                file_response = self.session.get(download_url, stream=True)
                if file_response.status_code == 200:
                    with open(save_to, "wb") as file:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                    print(f"文件成功下载并保存到 {save_to}")
                    return True
                else:
                    print(f"从 URL 下载文件失败: {download_url} - 状态码: {file_response.status_code}")
                    return False
            else:
                print(f"错误: {json.dumps(response_data.get('msg', '未知错误'), indent=4)}")
                return False

        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在下载模型文件时: {http_err}")
            return False
        except requests.RequestException as req_err:
            print(f"请求异常发生在下载模型文件时: {req_err}")
            return False
        except Exception as e:
            print(f"下载模型文件时发生未知错误: {e}")
            return False

    def download_file(self, url: str, local_path: str) -> bool:
        """
        从指定URL下载文件并保存到本地路径

        :param url: 文件的URL地址
        :param local_path: 本地保存文件的路径
        :return: 下载是否成功
        """
        print(f"开始从 URL 下载文件: {url}")
        try:
            response = self.session.get(url, stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                print(f"文件成功下载到 {local_path}")
                return True
            else:
                print(f"下载文件失败。状态码: {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"请求错误发生在下载文件时: {e}")
            return False
        except Exception as e:
            print(f"下载文件时发生未知错误: {e}")
            return False

    def get_model_version_files(self, model_name: str, model_version_name: str) -> Optional[list]:
        """
        获取模型版本下的所有文件信息

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :return: 文件信息列表或错误信息
        """
        url = f"{self.url}/api/model/internal/getDirectory"
        payload = {
            "modelName": model_name,
            "modelVersionName": model_version_name
        }

        print(f"请求获取模型版本文件信息的接口: {url}")
        print(f"获取模型版本文件信息的请求体: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"获取模型版本文件信息的响应: {json.dumps(response_data, indent=4)}")

            if response_data.get("code") == 0 and response_data.get("ok"):
                files = response_data["data"]["records"]
                print(f"找到的文件总数: {len(files)}")
                for file in files:
                    print(f"名称: {file['name']}, 大小: {file['size']}, 最后修改: {file['lastModified']}")
                return files
            else:
                print(f"错误: {json.dumps(response_data.get('msg', '未知错误'), indent=4)}")
                return None

        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在获取模型版本文件信息时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在获取模型版本文件信息时: {req_err}")
            return None
        except Exception as e:
            print(f"获取模型版本文件信息时发生未知错误: {e}")
            return None

    def add_model_to_db(
        self, 
        bg: str, 
        owner: str, 
        model_name: str, 
        model_version_name: str, 
        tar_md5: str, 
        onnx_md5: str, 
        rknn_md5: str, 
        model_arc: str, 
        region: str,
        model_id: str = None,
        test_result: Optional[list] = None, 
        test_set_ids: Optional[list] = None, 
        train_set_ids: Optional[list] = None, 
        quant_set_ids: Optional[list] = None, 
        params: Optional[Any] = None, 
        show: Optional[Any] = None, 
        task_type: str = 'detection', 
        desc: Optional[Any] = None, 
        code_id: Optional[Any] = None, 
        docker_image_id: Optional[Any] = None, 
        frame_type: str = 'pytorch', 
        model_format: str = 'onnx', 
        model_type: str = '目标检测'
    ) -> Optional[Dict[str, Any]]:
        """将模型信息添加到数据库

        :param bg: 背景信息
        :param owner: 所有者
        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param tar_md5: tar 文件的 MD5
        :param onnx_md5: onnx 文件的 MD5
        :param rknn_md5: rknn 文件的 MD5
        :param model_arc: 模型架构
        :param region: 区域
        :param test_result: 测试结果
        :param test_set_ids: 测试集 ID 列表
        :param train_set_ids: 训练集 ID 列表
        :param quant_set_ids: 量化集 ID 列表
        :param params: 参数
        :param show: 显示信息
        :param task_type: 任务类型
        :param desc: 描述
        :param code_id: 代码 ID
        :param docker_image_id: Docker 镜像 ID
        :param frame_type: 框架类型
        :param model_format: 模型格式
        :param model_type: 模型类型
        :return: 上传响应的 JSON，或如果未上传则为 None
        """
        url = f"{self.url}/api/model/internal/version"

        payload = {
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version_name,
            "region": region,
            "taskType": task_type,
            "modelArc": model_arc,
            "params": params,
            "testResult": test_result,
            "show": show,
            "trainSetIds": train_set_ids,
            "testSetIds": test_set_ids,
            "quantSetIds": quant_set_ids,
            "codeId": code_id,
            "dockerImageId": docker_image_id,
            "modelFile": {
                "tar": tar_md5,
                "onnx": onnx_md5,
                "rknn": rknn_md5
            },
            "modelDescription": desc,
            "modelType": model_type,
            "frameType": frame_type,
            "modelFormat": model_format
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        print(f"添加模型到数据库的请求体: {json.dumps(payload, indent=4)}")
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"添加模型到数据库的响应: {json.dumps(response_data, indent=4)}")
            return response_data
        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在添加模型到数据库时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在添加模型到数据库时: {req_err}")
            return None
        except Exception as e:
            print(f"添加模型到数据库时发生未知错误: {e}")
            return None

    def get_model_list(
        self, 
        model_name: Optional[str] = None, 
        model_version_name: Optional[str] = None, 
        bg: Optional[str] = None, 
        owner: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """获取模型列表

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :param bg: 背景信息
        :param owner: 所有者
        :return: 模型列表的 JSON 数据或错误信息
        """
        url = f"{self.url}/api/model/internal/version/list"
        payload = { 
            "bg": bg,
            "owner": owner,
            "modelName": model_name,
            "modelVersion": model_version_name
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        print(f"请求获取模型列表的接口: {url}")
        print(f"获取模型列表的请求体: {json.dumps(payload, indent=4)}")
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print(f"获取模型列表的响应: {json.dumps(response_data, indent=4)}")
            return response_data
        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在获取模型列表时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在获取模型列表时: {req_err}")
            return None
        except Exception as e:
            print(f"获取模型列表时发生未知错误: {e}")
            return None

    def get_model_id(self, model_name: str, model_version_name: str) -> Optional[str]:
        """获取模型版本的 ID

        :param model_name: 模型名称
        :param model_version_name: 模型版本名称
        :return: 模型版本的 ID 或 None
        """
        model_list = self.get_model_list(model_name, model_version_name)
        if model_list and model_list.get('code') == 0 and model_list.get('data'):
            return model_list.get('data')[0].get('modelVersionId')
        else:
            print(f"未找到模型 ID: {model_name} - {model_version_name}")
            return None

    def add_board_result_to_db(
        self, 
        model_name: str, 
        model_version_name: str, 
        board_result: list, 
        chip: str, 
        test_set_ids: list, 
        input_h: int, 
        input_w: int, 
        infer_time: float, 
        memory: int, 
        flash: int, 
        project: str, 
        projectId: str, 
        modelPath: str, 
        boardTestVersion: str, 
        testResultPath: str, 
        bad_case_ids: list,
        model_id: str = None,
        quant_algo: str = "normal", 
        quant_method: str = "channel"
    ) -> Optional[Dict[str, Any]]:
        """
        上传板端测试结果到数据库

        :param model_name: 模型名称
        :param model_version: 模型版本
        :param board_result: 板端测试结果
        :param chip: 芯片信息
        :param model_id: 模型 ID，默认为 None
        :param project: 项目名称
        :param quant_algo: 量化算法，默认为 "normal"
        :param quant_method: 量化方法，默认为 "channel"
        :param test_set_ids: 测试集 ID 列表
        :param input_h: 输入高度
        :param input_w: 输入宽度
        :param infer_time: 推理时间
        :param memory: 内存使用情况
        :param flash: 闪存大小
        :param projectId: 项目 ID
        :param modelPath: 模型路径
        :param boardTestVersion: 板端测试版本
        :param testResultPath: 测试结果路径
        :param bad_case_ids: 错误案例 ID 列表
        :return: 上传响应的 JSON，或如果未上传则为 None
        """
        if model_id is None:
            model_id = self.get_model_id(model_name, model_version_name)
            if model_id is None:
                print(f"未找到模型 ID: {model_name} - {model_version_name}。跳过板端结果上传。")
                return None

        url = f"{self.url}/api/model/internal/versionTest"
        
        payload = {
            "modelVersionId": model_id,
            "projectId": projectId,
            "projectName": project,
            "chipName": chip,
            "modelPath": modelPath,
            "boardTestVersion": boardTestVersion,
            "quantAlgo": quant_algo,
            "quantMethod": quant_method,
            "testResultBoard": board_result,
            "testResultPath": testResultPath,
            "testSetIds": test_set_ids,
            "badCaseIds": bad_case_ids,
            "inputH": input_h,
            "inputW": input_w,
            "inferTime": infer_time,
            "memory": memory,
            "flash": flash
        }

        payload = {k: v for k, v in payload.items() if v is not None}
        
        print(f"上传板端测试结果的请求体: {json.dumps(payload, indent=4)}")

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            response_data = response.json()
            print(f"上传板端测试结果的响应: {json.dumps(response_data, indent=4)}")
            return response_data
        except requests.HTTPError as http_err:
            print(f"HTTP 错误发生在上传板端测试结果时: {http_err}")
            return None
        except requests.RequestException as req_err:
            print(f"请求异常发生在上传板端测试结果时: {req_err}")
            return None
        except Exception as e:
            print(f"上传板端测试结果时发生未知错误: {e}")
            return None


class ai_tools:
    def __init__(self):
        """
        初始化 BadCaseDetector 类。
        所有必要的参数通过设置方法进行配置。
        """
        self.class_names = {}
        self.thresholds = {}
        self.badcase_positive_file_path = ""
        self.badcase_false_positive_file_path = ""
        self.val_file_path = ""
        self.positive_dataset_paths = []
        self.negative_dataset_paths = []
        
    def _compute_iou(self, rec1, rec2):
        """
        计算两个矩形框的 IoU
        :param rec1: (x1, y1, x2, y2)
        :param rec2: (x1, y1, x2, y2)
        :return: IoU 值
        """
        # 计算每个矩形的面积
        S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

        # 计算交集
        left_line = max(rec1[0], rec2[0])
        right_line = min(rec1[2], rec2[2])
        top_line = max(rec1[1], rec2[1])
        bottom_line = min(rec1[3], rec2[3])

        if left_line >= right_line or top_line >= bottom_line:
            return 0
        else:
            intersect = (right_line - left_line) * (bottom_line - top_line)
            union = S_rec1 + S_rec2 - intersect
            return intersect / union

    def is_badcase(self, predicted_labels, groundtruth_labels, class_names, thresholds, iou_threshold=0.5, is_positive=True):
        """
        判断一个标签文件是否为坏案例。

        参数：
        - predicted_labels: 模型预测的标签列表，每个标签格式为 [cls, conf, x1, y1, x2, y2]
        - groundtruth_labels: 真实标签列表，每个标签格式为 [cls, x1, y1, x2, y2]
        - class_names: 类别名称字典，键为类别索引，值为类别名称
        - thresholds: 阈值字典，键为类别名称，值为对应的阈值
        - iou_threshold: IoU 阈值，默认值为 0.5
        - is_positive: 布尔变量，判断是否为正检测（True）还是误检测（False）
        
        返回：
        - bool: 如果是坏案例返回 True，否则返回 False
        """
        if is_positive:
            # 正检测需要比较预测与真实标签
            matched = False
            for gt in groundtruth_labels:
                gt_cls = gt[0]
                gt_class_name = class_names.get(gt_cls, "")
                gt_conf_thres = thresholds.get(gt_class_name, 0)
                gt_box = gt[2:]  # [x1, y1, x2, y2]

                for pred in predicted_labels:
                    pred_cls, pred_conf, pred_box = pred[0], pred[1], pred[2:]
                    if pred_cls != gt_cls or pred_conf < gt_conf_thres:
                        continue
                    iou = self._compute_iou(gt_box, pred_box)
                    if iou > iou_threshold:
                        matched = True
                        break
            return not matched  # 如果没有匹配到，则为坏案例
        else:
            # 误检测只需要检查是否有假阳性
            for pred in predicted_labels:
                pred_cls, pred_conf, _ = pred
                class_name = class_names.get(pred_cls, "")
                conf_thres = thresholds.get(class_name, 0)
                if pred_conf > conf_thres:
                    return True  # 存在假阳性
            return False
