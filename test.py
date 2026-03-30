import google.generativeai as genai
import os

# Thay API Key của Phan vào đây
genai.configure(api_key="AIzaSyAJKvbaQVYu76l08zceNi4nDUE7PFouBFY")

try:
    # Liệt kê các model mà Key này được phép dùng
    print("Các model bạn có thể dùng:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Lỗi rồi: {e}")