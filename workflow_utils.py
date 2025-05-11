import requests
import json
import os

def upload_file_to_dify(api_key, file_path, file_type=None, user_id="abc-123"):
    """
    上传文件到Dify API
    
    Args:
        api_key (str): Dify API密钥
        file_path (str): 本地文件路径
        file_type (str, optional): 文件MIME类型，如果为None则自动根据文件扩展名推断
        user_id (str): 用户标识
        
    Returns:
        dict: API响应结果，如果失败则返回None
    """
    # API端点
    url = "https://api.dify.ai/v1/files/upload"
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # 如果未指定文件类型，则根据文件扩展名推断
    if file_type is None:
        if file_path.lower().endswith('.png'):
            file_type = 'image/png'
        elif file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            file_type = 'image/jpeg'
        elif file_path.lower().endswith('.gif'):
            file_type = 'image/gif'
        elif file_path.lower().endswith('.webp'):
            file_type = 'image/webp'
        elif file_path.lower().endswith('.pdf'):
            file_type = 'application/pdf'
        elif file_path.lower().endswith('.txt'):
            file_type = 'text/plain'
        else:
            # 默认类型
            file_type = 'application/octet-stream'
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        return None
    
    # 准备文件表单
    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, file_type)
            }
            
            # 准备表单数据
            form_data = {
                'user': user_id
            }
            
            # 发送POST请求
            response = requests.post(url, headers=headers, files=files, data=form_data)
        
        # 返回结果
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"上传失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"上传文件时发生错误: {str(e)}")
        return None

def run_dify_workflow(api_key, workflow_inputs, file_id=None, response_mode="blocking", user_id="user-123"):
    """
    执行Dify工作流
    
    Args:
        api_key (str): Dify API密钥
        workflow_inputs (dict): 工作流输入参数
        file_id (str, optional): 已上传文件的ID，如果提供则会自动添加到inputs中
        response_mode (str): 响应模式，可选"blocking"或"streaming"
        user_id (str): 用户标识
        
    Returns:
        dict: 工作流执行结果，如果失败则返回None
    """
    # API端点
    url = "https://api.dify.ai/v1/workflows/run"
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 准备工作流输入参数
    inputs = workflow_inputs.copy() if workflow_inputs else {}
    
    # 如果提供了文件ID，添加文件参数
    if file_id:
        inputs["file"] = {
            "type": "document",
            "transfer_method": "local_file",
            "upload_file_id": file_id
        }
    
    # 请求体
    data = {
        "inputs": inputs,
        "response_mode": response_mode,
        "user": user_id
    }
    
    try:
        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # 处理响应
        if response.status_code == 200:
            return response.json()
        else:
            print(f"工作流执行失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"执行工作流时发生错误: {str(e)}")
        return None

def upload_multi_files_to_dify(api_key, file_paths, user_id="abc-123"):
    """
    上传多个文件到Dify API
    
    Args:
        api_key (str): Dify API密钥
        file_paths (list): 本地文件路径列表
        user_id (str): 用户标识
        
    Returns:
        list: 上传成功的文件ID列表，如果全部失败则返回空列表
    """
    file_ids = []
    
    for file_path in file_paths:
        upload_result = upload_file_to_dify(api_key, file_path, None, user_id)
        if upload_result:
            print(f"文件 '{os.path.basename(file_path)}' 上传成功! ID: {upload_result.get('id')}")
            file_ids.append(upload_result.get('id'))
        else:
            print(f"文件 '{os.path.basename(file_path)}' 上传失败!")
    
    return file_ids

def run_multi_files_workflow(api_key, file_paths, workflow_inputs=None, response_mode="blocking", user_id="user-123"):
    """
    上传多个文件并执行Dify工作流
    
    Args:
        api_key (str): Dify API密钥
        file_paths (list): 本地文件路径列表
        workflow_inputs (dict, optional): 工作流其他输入参数
        response_mode (str): 响应模式，可选"blocking"或"streaming"
        user_id (str): 用户标识
        
    Returns:
        dict: 工作流执行结果，如果失败则返回None
    """
    # 上传多个文件
    file_ids = upload_multi_files_to_dify(api_key, file_paths, user_id)
    file_names=['Student_answer','Question','Evaluate_standard']
    if not file_ids:
        print("所有文件上传失败，无法执行工作流")
        return None
    
    print(f"成功上传 {len(file_ids)}/{len(file_paths)} 个文件")
    
    # 准备工作流输入参数
    inputs = workflow_inputs.copy() if workflow_inputs else {}
    
    # 如果上传了多个文件，添加到inputs中
    if len(file_ids) == 1:
        # 单文件情况
        inputs["file"] = {
            "type": "document",
            "transfer_method": "local_file",
            "upload_file_id": file_ids[0]
        }
    else:
        # 多文件情况
        for i, file_id in enumerate(file_ids):
            inputs[file_names[i]] = {
                "type": "document",
                "transfer_method": "local_file",
                "upload_file_id": file_id
            }
    
    # 执行工作流
    workflow_result = run_dify_workflow(api_key, inputs, None, response_mode, user_id)
    
    return workflow_result

def run_three_txt_files_workflow(api_key, file_path1, file_path2, file_path3, response_mode="blocking", user_id="user-123"):
    """
    上传3个txt文件并执行Dify工作流的专用函数
    
    Args:
        api_key (str): Dify API密钥
        file_path1 (str): 第一个txt文件路径
        file_path2 (str): 第二个txt文件路径
        file_path3 (str): 第三个txt文件路径
        response_mode (str): 响应模式，可选"blocking"或"streaming"
        user_id (str): 用户标识
        
    Returns:
        dict: 工作流执行结果，如果失败则返回None
    """
    file_paths = [file_path1, file_path2, file_path3]
    
    # 验证所有文件是否存在且为txt格式
    for i, path in enumerate(file_paths):
        if not os.path.exists(path):
            print(f"错误: 文件 {i+1} '{path}' 不存在")
            return None
        
        if not path.lower().endswith('.txt'):
            print(f"警告: 文件 {i+1} '{path}' 不是txt格式")
    
    # 使用空字典代替 workflow_inputs
    return run_multi_files_workflow(api_key, file_paths, {}, response_mode, user_id)

def upload_and_run_workflow(api_key, file_path, workflow_inputs=None, file_type=None, response_mode="blocking", user_id="user-123"):
    """
    上传文件并执行Dify工作流
    
    Args:
        api_key (str): Dify API密钥
        file_path (str): 本地文件路径
        workflow_inputs (dict, optional): 工作流其他输入参数
        file_type (str, optional): 文件MIME类型
        response_mode (str): 响应模式，可选"blocking"或"streaming"
        user_id (str): 用户标识
        
    Returns:
        dict: 工作流执行结果，如果失败则返回None
    """
    # 上传文件
    upload_result = upload_file_to_dify(api_key, file_path, file_type, user_id)
    
    if not upload_result:
        print("文件上传失败，无法执行工作流")
        return None
    
    print("文件上传成功!")
    print(f"文件ID: {upload_result.get('id')}")
    print(f"文件名: {upload_result.get('name')}")
    
    # 准备工作流输入参数
    inputs = workflow_inputs if workflow_inputs else {}
    
    # 执行工作流
    workflow_result = run_dify_workflow(api_key, inputs, upload_result.get('id'), response_mode, user_id)
    
    return workflow_result