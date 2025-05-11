import requests
import json
import os
import dotenv
from workflow_utils import *
dotenv.load_dotenv()



# 使用示例
if __name__ == "__main__":
    # 配置参数
    API_KEY = os.getenv("DIFY_API_KEY_PROBLEM")  # 替换为你的API密钥
    FILE_PATH = "./upload_files/题目.txt"         # 替换为你要上传的文件路径
    
    # 工作流输入参数
    workflow_inputs = {
        
        "choice": "1",
        "True_False": "1",
        "Difficulty_Level": "简单",
        "subject": "计算机",
        "Gap_filling": "1",
        "Programming": "1",
        "Pattern_type": "从上传题库中抽取"
    }
    
    # 上传文件并执行工作流
    result = upload_and_run_workflow(API_KEY, FILE_PATH, workflow_inputs)
    
    # 打印结果
    if result:
        print("工作流执行成功!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("工作流执行失败")