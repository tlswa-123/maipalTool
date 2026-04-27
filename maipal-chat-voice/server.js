/**
 * 脉大夫中医问诊系统 - 后端服务
 * 基于 WorkBuddy Claw API 的流式对话代理
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// ============ 配置 ============
const CONFIG = {
  port: process.env.PORT || 3215,
  apiEndpoint: 'copilot.tencent.com',
  apiPath: '/v2/chat/completions',
  apiKey: process.env.CODEBUDDY_API_KEY || ''
};

// ============ 加载脉大夫人设 ============
const TCM_PERSONA_PATH = path.join(__dirname, 'persona.md');
let TCM_PERSONA = '';

try {
  TCM_PERSONA = fs.readFileSync(TCM_PERSONA_PATH, 'utf-8');
  console.log(`Loaded TCM persona: ${TCM_PERSONA.length} chars`);
} catch (e) {
  console.error('Failed to load TCM persona:', e.message);
  TCM_PERSONA = '你是脉大夫，一位资深中医师。';
}

// 提取开场白（脉大夫的第一条消息）
function extractOpeningMessage() {
  const match = TCM_PERSONA.match(/\*\*脉大夫\*\*：[\s\S]*?(?=---|$)/);
  if (match) {
    return match[0].replace(/\*\*脉大夫\*\*：/, '').trim();
  }
  return '您好，欢迎来找我聊聊。我是脉大夫。先问一下，怎么称呼您呢？';
}

const OPENING_MESSAGE = extractOpeningMessage();

// 构建 System Prompt
function buildSystemPrompt() {
  // 提取角色设定部分（从"一、AI角色设定"到"二、"之前）
  const roleMatch = TCM_PERSONA.match(/## 一、AI角色设定[\s\S]*?(?=## 二、|$)/);
  const roleSection = roleMatch ? roleMatch[0] : '';
  
  // 提取知识库核心能力
  const kbMatch = TCM_PERSONA.match(/### 知识库核心能力清单[\s\S]*?(?=## 三、|$)/);
  const kbSection = kbMatch ? kbMatch[0] : '';
  
  // 提取问诊流程
  const flowMatch = TCM_PERSONA.match(/### 3\.1 问诊总体流程[\s\S]*?(?=### 3\.2|$)/);
  const flowSection = flowMatch ? flowMatch[0] : '';
  
  // 提取诊断报告模板结构
  const reportMatch = TCM_PERSONA.match(/## 四、诊断报告模板[\s\S]*?(?=## 五、|$)/);
  const reportSection = reportMatch ? reportMatch[0] : '';

  return `${roleSection}

${kbSection}

${flowSection}

${reportSection}

【重要提示】
- 你正在使用网页端与患者对话
- 严格遵循"一次只问一个问题"的原则
- 问诊从问称呼开始，逐步深入
- 最终需要出具完整的中医健康调理报告
- 养生为主，治未病理念
- 主要面向45-65岁中老年人

【当前状态】
- 这是全新的问诊会话
- 你应该以脉大夫的身份，用开场白开始对话
- 等待患者回复后，根据回答继续问诊流程`;
}

// ============ MIME 类型 ============
const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

// ============ 工具函数 ============
function generateId() {
  return Math.random().toString(36).substring(2, 15);
}

// 调用 CodeBuddy API（使用 HTTPS）
function callCodeBuddyAPI(model, messages, onData, onEnd, onError) {
  const systemPrompt = buildSystemPrompt();
  const fullMessages = [
    { role: 'system', content: systemPrompt },
    ...messages
  ];

  const requestData = JSON.stringify({
    model: model || 'claude-sonnet-4.6-1m',
    messages: fullMessages,
    stream: true
  });

  const options = {
    hostname: CONFIG.apiEndpoint,
    path: CONFIG.apiPath,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${CONFIG.apiKey}`,
      'Content-Length': Buffer.byteLength(requestData)
    }
  };

  const apiReq = https.request(options, (apiRes) => {
    // 处理重定向
    if (apiRes.statusCode === 301 || apiRes.statusCode === 302) {
      const redirectUrl = apiRes.headers.location;
      console.log('Redirect to:', redirectUrl);
      
      // 解析重定向 URL
      const redirectMatch = redirectUrl.match(/https?:\/\/([^\/]+)(.*)/);
      if (redirectMatch) {
        const newHost = redirectMatch[1];
        const newPath = redirectMatch[2] || CONFIG.apiPath;
        
        const redirectOptions = {
          hostname: newHost,
          path: newPath,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${CONFIG.apiKey}`,
            'Content-Length': Buffer.byteLength(requestData)
          }
        };
        
        const redirectReq = https.request(redirectOptions, (redirectRes) => {
          handleStreamResponse(redirectRes, onData, onEnd, onError);
        });
        
        redirectReq.on('error', onError);
        redirectReq.write(requestData);
        redirectReq.end();
        return;
      }
    }
    
    handleStreamResponse(apiRes, onData, onEnd, onError);
  });

  apiReq.on('error', onError);
  apiReq.write(requestData);
  apiReq.end();
}

// 处理流式响应
function handleStreamResponse(res, onData, onEnd, onError) {
  if (res.statusCode !== 200) {
    let errorData = '';
    res.on('data', chunk => errorData += chunk);
    res.on('end', () => {
      onError(new Error(`API Error (${res.statusCode}): ${errorData}`));
    });
    return;
  }

  let buffer = '';
  res.on('data', (chunk) => {
    buffer += chunk.toString();
    const lines = buffer.split('\n');
    buffer = lines.pop();
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith('data:')) {
        const data = trimmed.slice(5).trim();
        if (data === '[DONE]') {
          onData('[DONE]');
          continue;
        }
        try {
          const parsed = JSON.parse(data);
          const content = parsed.choices?.[0]?.delta?.content;
          if (content && content.length > 0) {
            onData(content);
          }
        } catch (e) {
          // 忽略解析错误
        }
      }
    }
  });

  res.on('end', onEnd);
  res.on('error', onError);
}

// ============ 服务器 ============
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;

  // CORS 头
  const setCORS = () => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  };

  setCORS();

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // API: 获取开场白（用于新会话开始）
  if (pathname === '/api/opening' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      opening: OPENING_MESSAGE,
      persona: '脉大夫',
      contextSize: TCM_PERSONA.length
    }));
    return;
  }

  // API: 获取人设信息
  if (pathname === '/api/persona' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      name: '脉大夫',
      title: '资深中医师',
      targetAudience: '45-65岁中老年人',
      approach: '一次只问一个问题，温和亲切',
      contextSize: TCM_PERSONA.length
    }));
    return;
  }

  // API: 望闻诊图像/音频分析代理（面部 / 舌部 / 语声）→ 转发到 tcm-diagnosis-platform (8000)
  if (pathname.startsWith('/api/diagnosis/') && req.method === 'POST') {
    const parts = pathname.split('/');
    const kind = parts[3]; // face | tongue | voice
    if (kind !== 'face' && kind !== 'tongue' && kind !== 'voice') {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'unknown diagnosis kind' }));
      return;
    }

    const upstreamOptions = {
      hostname: '127.0.0.1',
      port: 8000,
      path: `/api/${kind}/analyze`,
      method: 'POST',
      headers: req.headers
    };

    const upstreamReq = http.request(upstreamOptions, (upstreamRes) => {
      res.writeHead(upstreamRes.statusCode, upstreamRes.headers);
      upstreamRes.pipe(res);
    });

    upstreamReq.on('error', (err) => {
      console.error('望闻诊代理错误:', err.message);
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        error: '望闻诊服务未就绪，请确认已启动 tcm-diagnosis-platform (8000)',
        detail: err.message
      }));
    });

    req.pipe(upstreamReq);
    return;
  }

  // API: 聊天（流式）
  if (pathname === '/api/chat' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { model, messages } = JSON.parse(body);

        res.writeHead(200, {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive'
        });

        callCodeBuddyAPI(
          model,
          messages,
          (data) => {
            if (data === '[DONE]') {
              res.write('data: [DONE]\n\n');
            } else {
              res.write(`data: ${JSON.stringify({ content: data })}\n\n`);
            }
          },
          () => {
            res.write('data: [DONE]\n\n');
            res.end();
          },
          (err) => {
            console.error('API error:', err);
            res.write(`data: ${JSON.stringify({ error: err.message })}\n\n`);
            res.end();
          }
        );

      } catch (err) {
        console.error('Chat error:', err);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // 静态文件服务
  let filePath = pathname === '/' ? '/index.html' : pathname;
  filePath = path.join(__dirname, 'public', filePath);

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Server Error');
      }
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(content);
  });
});

server.listen(CONFIG.port, () => {
  console.log(`\n🏥 脉大夫中医问诊系统已启动`);
  console.log(`   地址: http://localhost:${CONFIG.port}`);
  console.log(`   人设: 脉大夫 (${TCM_PERSONA.length} chars)`);
  console.log(`   可用模型: 24 个`);
  console.log(`   问诊流程: 全新会话，从开场白开始\n`);
});
