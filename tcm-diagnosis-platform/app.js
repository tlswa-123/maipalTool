// ========= 摄像头管理器 =========
class CameraManager {
    constructor() {
        this.streams = {};
        this.facingModes = {};
    }

    async open(type) {
        const video = document.getElementById(`${type}-video`);
        if (!this.facingModes[type]) this.facingModes[type] = 'user';
        try {
            this.close(type);
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: this.facingModes[type], width: { ideal: 1280 }, height: { ideal: 960 } },
                audio: false
            });
            this.streams[type] = stream;
            video.srcObject = stream;
            await video.play();
            return true;
        } catch (err) {
            if (err.name === 'NotAllowedError') alert('请允许浏览器使用摄像头权限');
            else if (err.name === 'NotFoundError') alert('未检测到可用的摄像头设备');
            else alert('摄像头打开失败: ' + err.message);
            return false;
        }
    }

    close(type) {
        const stream = this.streams[type];
        if (stream) { stream.getTracks().forEach(t => t.stop()); delete this.streams[type]; }
        const video = document.getElementById(`${type}-video`);
        if (video) video.srcObject = null;
    }

    async switchCamera(type) {
        this.facingModes[type] = this.facingModes[type] === 'user' ? 'environment' : 'user';
        return this.open(type);
    }

    capture(type) {
        const video = document.getElementById(`${type}-video`);
        const canvas = document.getElementById(`${type}-canvas`);
        if (!video || !video.videoWidth) return null;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        return canvas.toDataURL('image/jpeg', 0.92);
    }
}

// ========= 中医诊断分析器（纯后端调用，无模拟） =========
class TCMAnalyzer {
    constructor() {
        this.faceImage = null;
        this.tongueImage = null;
        this.apiBaseUrl = 'http://localhost:8001';
    }

    async analyzeFace(imageData) {
        return await this._callAPI('/api/face/analyze', imageData);
    }

    async analyzeTongue(imageData) {
        return await this._callAPI('/api/tongue/analyze', imageData);
    }

    async _callAPI(endpoint, imageData) {
        const formData = this._buildFormData(imageData);

        let response;
        try {
            response = await fetch(`${this.apiBaseUrl}${endpoint}`, {
                method: 'POST',
                body: formData
            });
        } catch (err) {
            throw new Error('无法连接到后端服务，请确认后端已启动（端口8001）');
        }

        if (response.ok) {
            return await response.json();
        }

        // 失败——提取后端返回的具体原因
        let detail = '未知错误';
        try {
            const errData = await response.json();
            detail = errData.detail || detail;
        } catch (_) {}
        throw new Error(detail);
    }

    _buildFormData(imageData) {
        const formData = new FormData();

        // 如果已经是 File/Blob（比如未来扩展直接传文件）
        if (imageData instanceof File || imageData instanceof Blob) {
            formData.append('file', imageData, 'image.jpg');
            return formData;
        }

        // base64 dataURL → Blob
        if (typeof imageData !== 'string') {
            throw new Error('不支持的图片数据类型');
        }

        let base64Str, mimeType = 'image/jpeg';

        if (imageData.startsWith('data:')) {
            const commaIdx = imageData.indexOf(',');
            if (commaIdx === -1) throw new Error('图片数据格式异常');
            const meta = imageData.substring(0, commaIdx);
            const mimeMatch = meta.match(/data:([^;]+)/);
            if (mimeMatch) mimeType = mimeMatch[1];
            base64Str = imageData.substring(commaIdx + 1);
        } else {
            base64Str = imageData;
        }

        const binaryStr = atob(base64Str);
        const bytes = new Uint8Array(binaryStr.length);
        for (let i = 0; i < binaryStr.length; i++) {
            bytes[i] = binaryStr.charCodeAt(i);
        }
        const blob = new Blob([bytes], { type: mimeType });
        formData.append('file', blob, 'capture.jpg');
        return formData;
    }
}

// ========= 初始化应用 =========
document.addEventListener('DOMContentLoaded', () => {
    const analyzer = new TCMAnalyzer();
    const camera = new CameraManager();

    // 标签切换
    const tabBtns = document.querySelectorAll('.tab-btn');
    const sections = document.querySelectorAll('.diagnosis-section');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            camera.close('face');
            camera.close('tongue');
            tabBtns.forEach(b => b.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`${btn.dataset.tab}-section`).classList.add('active');
        });
    });

    // 模式切换（上传 / 摄像头）
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const mode = btn.dataset.mode;
            const target = btn.dataset.target;
            btn.parentElement.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const uploadArea = document.getElementById(`${target}-upload-area`);
            const cameraArea = document.getElementById(`${target}-camera-area`);
            if (mode === 'upload') {
                camera.close(target);
                cameraArea.style.display = 'none';
                uploadArea.style.display = 'block';
            } else {
                uploadArea.style.display = 'none';
                cameraArea.style.display = 'block';
                await camera.open(target);
            }
        });
    });

    // 拍照 / 切换摄像头 / 关闭摄像头
    ['face', 'tongue'].forEach(type => {
        document.getElementById(`${type}-capture-btn`).addEventListener('click', () => {
            const dataUrl = camera.capture(type);
            if (!dataUrl) { alert('拍照失败，请确保摄像头正常工作'); return; }
            camera.close(type);
            document.getElementById(`${type}-camera-area`).style.display = 'none';
            analyzer[type + 'Image'] = dataUrl;
            document.getElementById(`${type}-image`).src = dataUrl;
            document.getElementById(`${type}-preview`).style.display = 'block';
        });

        document.getElementById(`${type}-switch-camera`).addEventListener('click', () => {
            camera.switchCamera(type);
        });

        document.getElementById(`${type}-close-camera`).addEventListener('click', () => {
            camera.close(type);
            document.getElementById(`${type}-camera-area`).style.display = 'none';
            document.getElementById(`${type}-upload-area`).style.display = 'block';
            const switcher = document.querySelector(`.mode-btn[data-target="${type}"][data-mode="upload"]`);
            if (switcher) {
                switcher.parentElement.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                switcher.classList.add('active');
            }
        });
    });

    // 文件上传
    setupFileUpload('face-input', 'face-upload-box', 'face-preview', 'face-image', 'remove-face-btn', 'face');
    setupFileUpload('tongue-input', 'tongue-upload-box', 'tongue-preview', 'tongue-image', 'remove-tongue-btn', 'tongue');

    // 面诊分析
    document.getElementById('analyze-face-btn').addEventListener('click', async () => {
        if (!analyzer.faceImage) { alert('请先上传或拍摄面部照片'); return; }
        showLoading();
        try {
            const result = await analyzer.analyzeFace(analyzer.faceImage);
            displayResult('face', result);
        } catch (error) {
            alert(error.message);
        } finally {
            hideLoading();
        }
    });

    // 舌诊分析
    document.getElementById('analyze-tongue-btn').addEventListener('click', async () => {
        if (!analyzer.tongueImage) { alert('请先上传或拍摄舌头照片'); return; }
        showLoading();
        try {
            const result = await analyzer.analyzeTongue(analyzer.tongueImage);
            displayResult('tongue', result);
        } catch (error) {
            alert(error.message);
        } finally {
            hideLoading();
        }
    });

    // 导出 / 复制
    document.querySelectorAll('.export-btn').forEach(btn => {
        btn.addEventListener('click', () => exportResult(btn.dataset.type));
    });
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => copyResult(btn.dataset.type));
    });

    // ========= 辅助函数 =========

    function setupFileUpload(inputId, uploadBoxId, previewId, imageId, removeBtnId, type) {
        const input = document.getElementById(inputId);
        const uploadBox = document.getElementById(uploadBoxId);
        const preview = document.getElementById(previewId);
        const image = document.getElementById(imageId);
        const removeBtn = document.getElementById(removeBtnId);

        uploadBox.addEventListener('click', () => input.click());

        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.style.borderColor = '#4a90e2';
            uploadBox.style.background = '#e8f0fe';
        });
        uploadBox.addEventListener('dragleave', () => {
            uploadBox.style.borderColor = '';
            uploadBox.style.background = '';
        });
        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.style.borderColor = '';
            uploadBox.style.background = '';
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) handleFile(file, preview, image, type);
            else alert('请上传图片文件');
        });

        input.addEventListener('change', (e) => {
            if (e.target.files[0]) handleFile(e.target.files[0], preview, image, type);
        });

        removeBtn.addEventListener('click', () => {
            analyzer[type + 'Image'] = null;
            input.value = '';
            preview.style.display = 'none';
            document.getElementById(`${type}-upload-area`).style.display = 'block';
            uploadBox.style.display = 'block';
            document.getElementById(`${type}-camera-area`).style.display = 'none';
            const switcher = document.querySelector(`.mode-btn[data-target="${type}"][data-mode="upload"]`);
            if (switcher) {
                switcher.parentElement.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                switcher.classList.add('active');
            }
            document.getElementById(`${type}-result`).style.display = 'none';
        });
    }

    function handleFile(file, preview, image, type) {
        const reader = new FileReader();
        reader.onload = (e) => {
            analyzer[type + 'Image'] = e.target.result;
            image.src = e.target.result;
            document.getElementById(`${type}-upload-area`).style.display = 'none';
            document.getElementById(`${type}-camera-area`).style.display = 'none';
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    function showLoading() { document.getElementById('loading-overlay').style.display = 'flex'; }
    function hideLoading() { document.getElementById('loading-overlay').style.display = 'none'; }

    function displayResult(type, result) {
        const resultContainer = document.getElementById(`${type}-result`);
        const resultContent = document.getElementById(`${type}-result-content`);

        let html = '<div class="result-sections">';

        // 中医辨证
        html += '<div class="result-section">';
        html += '<h4>🩺 中医辨证</h4>';
        html += `<div class="result-item"><strong>主要证型：</strong>${result.tcm_diagnosis.主要证型.join('、') || '无明显证型'}</div>`;
        html += `<div class="result-item"><strong>辨证要点：</strong>${result.tcm_diagnosis.辨证要点.join('；') || '无'}</div>`;
        html += `<div class="result-item"><strong>调理建议：</strong>${result.tcm_diagnosis.调理建议.join('；') || '无'}</div>`;
        html += '</div>';

        // 详细数据
        const mainKey = type === 'face' ? 'facial_diagnosis' : 'tongue_diagnosis';
        html += '<div class="result-section">';
        html += '<h4>📊 详细诊断数据</h4>';
        html += '<pre>' + JSON.stringify(result[mainKey], null, 2) + '</pre>';
        html += '</div>';

        html += '</div>';
        resultContent.innerHTML = html;
        resultContainer.style.display = 'block';
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function exportResult(type) {
        const el = document.getElementById(`${type}-result`);
        if (!el || el.style.display === 'none') { alert('没有可导出的结果'); return; }
        const date = new Date().toLocaleString('zh-CN');
        const blob = new Blob([`中医${type === 'face' ? '面诊' : '舌诊'}报告\n时间：${date}\n\n${el.innerText}`], { type: 'text/plain;charset=utf-8' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `${type === 'face' ? '面诊' : '舌诊'}报告_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    function copyResult(type) {
        const el = document.getElementById(`${type}-result`);
        if (!el || el.style.display === 'none') { alert('没有可复制的结果'); return; }
        navigator.clipboard.writeText(el.innerText).then(() => alert('已复制')).catch(() => alert('复制失败'));
    }
});
