"""
后端API测试脚本
用于验证面诊和舌诊API是否正常工作
"""
import requests
import json
import sys
from pathlib import Path

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端健康检查通过")
            return True
        else:
            print(f"❌ 后端健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到后端: {e}")
        return False

def test_face_analysis(image_path):
    """测试面诊分析接口"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/face/analyze", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 面诊分析成功")
            print(f"   - 主要证型: {', '.join(result.get('tcm_diagnosis', {}).get('主要证型', []))}")
            return True
        else:
            print(f"❌ 面诊分析失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 面诊分析异常: {e}")
        return False

def test_tongue_analysis(image_path):
    """测试舌诊分析接口"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/api/tongue/analyze", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 舌诊分析成功")
            print(f"   - 主要证型: {', '.join(result.get('tcm_diagnosis', {}).get('主要证型', []))}")
            return True
        else:
            print(f"❌ 舌诊分析失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 舌诊分析异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 中医智能诊断平台 - API测试")
    print("=" * 50)
    print()
    
    # 测试健康检查
    if not test_health():
        print()
        print("❌ 后端服务未启动，请先运行: python app.py")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print()
    
    # 检查是否有测试图片
    test_dir = Path(__file__).parent.parent / "test_images"
    
    face_image = None
    tongue_image = None
    
    if test_dir.exists():
        images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png")) + list(test_dir.glob("*.jpeg"))
        
        for img in images:
            name = img.name.lower()
            if "face" in name or "面" in name:
                face_image = img
            elif "tongue" in name or "舌" in name:
                tongue_image = img
    
    # 测试面诊
    print("📸 测试面诊分析...")
    if face_image and face_image.exists():
        test_face_analysis(face_image)
    else:
        print("⚠️  未找到测试图片，跳过面诊测试")
        print("   提示: 在 test_images 目录下放置测试图片")
    
    print()
    
    # 测试舌诊
    print("👅 测试舌诊分析...")
    if tongue_image and tongue_image.exists():
        test_tongue_analysis(tongue_image)
    else:
        print("⚠️  未找到测试图片，跳过舌诊测试")
        print("   提示: 在 test_images 目录下放置测试图片")
    
    print()
    print("=" * 50)
    print("✅ 测试完成")
    print()
    print("💡 提示:")
    print("   - 访问 http://localhost:8000/docs 查看API文档")
    print("   - 使用前端界面: python3 -m http.server 8001")
    print("   - 浏览器访问: http://localhost:8001")

if __name__ == "__main__":
    main()
