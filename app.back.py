from flask import Flask, render_template, request, jsonify
import os
import json
import dotenv
from workflow_utils import upload_and_run_workflow, run_three_txt_files_workflow

# 加载环境变量
dotenv.load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/multi_upload', methods=['GET'])
def multi_upload():
    return render_template('multi_upload.html')

@app.route('/run_workflow', methods=['POST'])
def run_workflow():
    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_PROBLEM")
    
    # 获取上传的文件
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    
    # 保存文件到临时位置
    temp_path = "./uploads/txt/" + file.filename
    file.save(temp_path)
    
    # 获取表单参数
    workflow_inputs = {
        "choice": request.form.get('choice', '1'),
        "True_False": request.form.get('true_false', '1'),
        "Difficulty_Level": request.form.get('difficulty', '简单'),
        "subject": request.form.get('subject', '计算机'),
        "Gap_filling": request.form.get('gap_filling', '1'),
        "Programming": request.form.get('programming', '1'),
        "Pattern_type": request.form.get('pattern_type', '从上传题库中抽取')
    }
    
    # 调用API
    result = upload_and_run_workflow(api_key, temp_path, workflow_inputs)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "API调用失败"}), 500

@app.route('/run_multi_workflow', methods=['POST'])
def run_multi_workflow():
    # 获取API密钥
    api_key = os.getenv("DIFY_API_KEY_MARKING")
    
    # 检查是否有3个文件上传
    if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files:
        return jsonify({"error": "需要上传3个文件"}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    
    # 检查文件是否选择
    if file1.filename == '' or file2.filename == '' or file3.filename == '':
        return jsonify({"error": "请选择所有3个文件"}), 400
    
    # 保存文件到临时位置
    os.makedirs("./uploads/txt", exist_ok=True)
    temp_path1 = "./uploads/txt/" + file1.filename
    temp_path2 = "./uploads/txt/" + file2.filename
    temp_path3 = "./uploads/txt/" + file3.filename
    
    file1.save(temp_path1)
    file2.save(temp_path2)
    file3.save(temp_path3)
    
    # 调用API - 不再传递 workflow_inputs
    result = run_three_txt_files_workflow(api_key, temp_path1, temp_path2, temp_path3)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "API调用失败"}), 500

if __name__ == "__main__":
    # 确保上传目录存在
    os.makedirs("./uploads/txt", exist_ok=True)
    app.run(debug=True)