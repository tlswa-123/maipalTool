# 中医智能诊断平台

## 项目简介

这是一个基于Web的**真实AI识别**中医诊断平台，实现**面诊**和**舌诊**两大核心功能。用户可以通过上传面部或舌头照片，获得详细的中医诊断分析结果和调理建议。

**✨ 核心特性：使用OpenCV、MediaPipe等成熟的AI库实现真实的图像识别，无需训练自己的模型！**

## 功能特性

### 🎭 面诊功能
- **面部识别**：支持人脸检测和分析
- **脸色分析**：识别面色主色调、颜色分布、光泽度等
- **神态评估**：分析精神状态、眼神状况、面部表情
- **面部特征**：检测发质、浮肿、皮肤纹理等
- **中医辨证**：根据面诊结果提供证型判断和调理建议

### 👅 舌诊功能
- **舌体分析**：识别舌色、舌形、舌质纹理、舌体活动度
- **舌苔分析**：检测苔色、苔厚薄、分布情况、苔质类型
- **舌下络脉**：分析络脉可见性、颜色、粗细、迂曲程度
- **中医辨证**：根据舌诊结果提供证型判断和调理建议

### 📋 通用功能
- 图片拖拽上传
- 图片预览与删除
- 结果导出（TXT格式）
- 结果一键复制
- 响应式设计，支持移动端

## 快速开始

### 🚀 完整版（推荐）- 包含真实AI识别

这个版本使用真实的AI库进行图像识别，提供准确的诊断结果。

#### 1. 启动后端服务

**macOS/Linux:**
```bash
cd backend
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
cd backend
start.bat
```

或者手动启动：
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### 2. 打开前端页面

在另一个终端窗口中：
```bash
# 使用Python 3启动HTTP服务器
python3 -m http.server 8001

# 或使用Node.js http-server
npx http-server -p 8001
```

然后在浏览器访问：`http://localhost:8001`

#### 3. 使用API文档

后端启动后，访问 `http://localhost:8000/docs` 查看完整的API文档和测试接口。

---

### 📱 模拟版（离线使用）- 纯前端模拟分析

这个版本不需要后端，适合离线演示或测试。

1. 克隆或下载本项目到本地
2. 用浏览器直接打开 `index.html` 文件
3. 即可使用所有功能

```bash
# 在项目目录下
open index.html  # macOS
# 或双击 index.html 文件
```

### 方法二：使用本地服务器

如果需要使用本地服务器：

```bash
# 使用 Python 3
python3 -m http.server 8000

# 使用 Node.js http-server
npx http-server -p 8000
```

然后在浏览器访问：`http://localhost:8000`

## 使用说明

### 面诊流程

1. **上传照片**
   - 点击上传区域或拖拽面部照片到上传框
   - 支持JPG、PNG、WebP格式

2. **开始分析**
   - 点击"开始面诊分析"按钮
   - 等待2-3秒分析完成

3. **查看结果**
   - 系统将显示详细的面诊结果
   - 包括中医辨证、调理建议和详细诊断数据

4. **导出/复制**
   - 点击"导出报告"下载TXT格式报告
   - 点击"复制结果"将结果复制到剪贴板

### 舌诊流程

1. **上传照片**
   - 点击上传区域或拖拽舌头照片到上传框
   - 支持JPG、PNG、WebP格式

2. **开始分析**
   - 点击"开始舌诊分析"按钮
   - 等待2-3秒分析完成

3. **查看结果**
   - 系统将显示详细的舌诊结果
   - 包括舌体、舌苔、舌下络脉分析和中医辨证建议

4. **导出/复制**
   - 点击"导出报告"下载TXT格式报告
   - 点击"复制结果"将结果复制到剪贴板

## 面诊数据结构

### 面色分析 (complexion_color)
- `primary_color`: 主色调（淡白/淡红/红/黄/青/黑）
- `color_distribution`: 颜色分布（均匀/斑块状/区域性分布）
- `brightness`: 光泽度评分（0-100）
- `glossiness`: 光泽感（有光泽/无光泽/晦暗）

### 神态评估 (spirit_expression)
- `mental_state`: 精神状态（精神饱满/萎靡不振/疲惫）
- `eye_condition`: 眼睛状况
  - `brightness`: 眼神（明亮/暗淡/呆滞）
  - `dark_circles`: 黑眼圈（无/轻度/中度/重度）
  - `eye_bags`: 眼袋（无/轻度/中度/重度）
  - `redness`: 眼睛充血（无/眼白有红血丝/充血）
- `facial_expression`: 面部表情（自然/焦虑/痛苦/疲惫）

### 面部特征 (facial_features)
- `hair_condition`: 发质
  - `shine`: 光泽（光泽/干燥/毛躁）
  - `density`: 发量（浓密/正常/稀疏/明显脱发）
- `facial_puffiness`: 浮肿
  - `status`: 浮肿程度（无/轻度/中度/重度浮肿）
  - `location`: 浮肿位置（眼周/全脸/下颌）
- `skin_texture`: 皮肤纹理
  - `oiliness`: 出油情况（干燥/正常/油腻）
  - `pores`: 毛孔状态（细腻/正常/粗大）
  - `elasticity`: 皮肤弹性（紧致/正常/松弛）

## 舌诊数据结构

### 舌体分析 (tongue_body)
- `color`: 舌色
  - `main_color`: 主色（淡白/淡红/红/绛/青紫）
  - `uniformity`: 均匀度（均匀/不均匀）
  - `abnormal_colorations`: 异常着色区域
- `shape`: 舌形
  - `size`: 大小（瘦薄/正常/胖大/肿胀）
  - `teeth_marks`: 齿痕（无/轻度/中度/重度齿痕）
  - `fissures`: 裂纹
    - `has_fissures`: 是否有裂纹
    - `fissure_pattern`: 裂纹形态
    - `fissure_count`: 裂纹数量
- `texture`: 舌质
  - `type`: 老嫩（老舌/嫩舌）
  - `dryness`: 干湿度（正常/偏干/偏湿）
  - `petechiae`: 瘀点
    - `has_petechiae`: 是否有瘀点
    - `count`: 瘀点数量
    - `location`: 瘀点位置
    - `color`: 瘀点颜色
- `movement`: 舌体活动度（灵活/僵硬/颤抖）

### 舌苔分析 (tongue_coating)
- `color`: 苔色
  - `main_color`: 主色（白苔/黄苔/灰黑苔/霉酱色苔）
  - `uniformity`: 均匀度（均匀/不均匀）
- `thickness`: 苔厚薄
  - `level`: 等级（薄苔/厚苔/腻苔）
  - `thickness_value`: 厚度量化值（0-10）
- `distribution`: 分布情况
  - `coverage`: 覆盖情况（全覆盖/局部覆盖）
  - `distribution_pattern`: 分布规律
  - `mapping_tongue`: 是否为地图舌
- `texture`: 苔质
  - `type`: 类型（正常/腻苔/糙苔/剥脱）
  - `greasiness`: 腻感程度（无/轻度/中度/重度腻）

### 舌下络脉 (sublingual_vein)
- `visible`: 是否可见
- `color`: 络脉颜色（淡紫/青紫/紫暗/紫黑）
- `width`: 粗细
  - `status`: 状态（正常/增粗/明显增粗）
  - `width_value`: 宽度数值（mm）
- `tortuosity`: 迂曲程度（正常/轻度/中度/明显）
- `length`: 长度（mm）
- `branching`: 分支
  - `has_branching`: 是否有分支
  - `branch_count`: 分支数量
- `stasis`: 瘀血
  - `has_stasis`: 是否有瘀血
  - `stasis_degree`: 瘀血程度（轻度/中度/重度）

## 技术说明

### ✅ 已实现真实AI识别

本项目已经集成了真实的AI识别能力，使用成熟的开源库：

**面诊技术栈：**
- **MediaPipe** - Google的人脸检测和关键点识别
- **OpenCV** - 图像处理和颜色分析
- **sklearn (K-Means)** - 颜色聚类分析

**舌诊技术栈：**
- **OpenCV** - 舌体分割（颜色+形态学）
- **HSV色彩空间** - 精确的舌色分析
- **Canny边缘检测** - 裂纹和纹理分析

### 🎯 核心功能

**面诊实现：**
1. 人脸检测和关键点定位（MediaPipe）
2. 人脸区域裁剪和分析
3. 面色分析：HSV色彩空间 + K-Means聚类
4. 神态评估：眼睛开合度、表情分析
5. 面部特征：纹理强度、边缘密度分析

**舌诊实现：**
1. 舌体分割：颜色阈值 + 形态学处理
2. 舌色分析：HSV空间聚类分类
3. 舌形判断：轮廓分析 + 凸包检测
4. 舌苔分析：厚度、分布、纹理量化
5. 舌下络脉：紫色区域检测 + 形态分析

### 🔧 技术优势

1. **无需训练模型** - 使用成熟的开源库，开箱即用
2. **准确可靠** - 基于计算机视觉经典算法
3. **本地运行** - 数据不上传云端，保护隐私
4. **易于部署** - 只需Python和基础依赖
5. **性能优秀** - OpenCV和MediaPipe都是高性能库

### 📦 依赖说明

- `opencv-python` - 图像处理核心库
- `mediapipe` - 人脸检测和关键点
- `scikit-learn` - 机器学习算法（K-Means聚类）
- `numpy` - 数值计算
- `fastapi` - 高性能Web框架
- `uvicorn` - ASGI服务器

### 🚀 性能优化建议

1. **GPU加速**：如需更快的处理速度，可以启用CUDA
2. **异步处理**：对于批量图片，可以使用异步队列
3. **结果缓存**：相同图片可以缓存分析结果
4. **图片压缩**：上传前压缩图片可以提高处理速度

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 许可证

MIT License

## 免责声明

本平台仅供学习和研究使用，诊断结果仅供参考，不能替代专业医疗诊断。如有健康问题，请咨询专业中医师或正规医疗机构。

## 联系方式

如有问题或建议，欢迎提出Issue或Pull Request。
