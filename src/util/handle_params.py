import json
import os
def save_best_params(model_name, params):
    path = "src/models/params/"
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = f"{model_name.lower().replace(' ', '_')}_params.json"
    with open(os.path.join(path, file_name), 'w') as f:
        json.dump(params, f, indent=4)
    print(f"Đã lưu tham số cho {model_name} vào {file_name}")

def load_best_params(model_name):
    file_name = f"src/models/params/{model_name.lower().replace(' ', '_')}_params.json"
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file params cho {model_name}. Hãy chạy Tuning trước!")
        return None
    