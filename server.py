"""ETA 意图识别交互原型 — 本地Web服务"""

import json
import os
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from src.intent import classify_intent

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "intent-history.jsonl")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")


def _check_auth(handler) -> bool:
    """Return True if request carries valid token, or no token is configured."""
    if not ACCESS_TOKEN:
        return True
    auth = handler.headers.get("Authorization", "")
    return auth == f"Bearer {ACCESS_TOKEN}"


def append_history(record: dict):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_history() -> list[dict]:
    if not os.path.exists(HISTORY_FILE):
        return []
    records = []
    with open(HISTORY_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/classify":
            if not _check_auth(self):
                self._json_response(401, {"error": "Unauthorized"})
                return

            length = int(self.headers["Content-Length"])
            body = json.loads(self.rfile.read(length))
            user_input = body.get("input", "").strip()

            if not user_input:
                self._json_response(400, {"error": "输入不能为空"})
                return

            try:
                result = classify_intent(user_input)
                record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "input": user_input,
                    "intent": result.intent.value,
                    "intent_label": INTENT_LABELS[result.intent.value],
                    "domain": result.domain.value,
                    "domain_label": DOMAIN_LABELS.get(result.domain.value, result.domain.value),
                    "level": result.level.value,
                    "level_label": LEVEL_LABELS.get(result.level.value, result.level.value),
                    "confidence": result.confidence,
                    "reasoning": result.reasoning,
                    "thinking": result.thinking,
                }
                append_history(record)
                self._json_response(200, record)
            except Exception as e:
                self._json_response(500, {"error": str(e)})
            return

        if self.path == "/api/history":
            if not _check_auth(self):
                self._json_response(401, {"error": "Unauthorized"})
                return
            self._json_response(200, {"records": load_history()})
            return

        self._json_response(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/api/history":
            if not _check_auth(self):
                self._json_response(401, {"error": "Unauthorized"})
                return
            self._json_response(200, {"records": load_history()})
            return
        if self.path in ("/", "/index.html"):
            self._serve_index()
            return
        if self.path.startswith("/static/"):
            super().do_GET()
            return
        self._json_response(404, {"error": "not found"})

    def _serve_index(self):
        html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
        with open(html_path, encoding="utf-8") as f:
            content = f.read()
        content = content.replace("__ACCESS_TOKEN__", ACCESS_TOKEN)
        body = content.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_response(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


INTENT_LABELS = {
    "K": "知识查询", "D": "错误诊断", "S": "解题求助",
    "M": "方法策略", "P": "练习请求", "E": "情感表达",
}

DOMAIN_LABELS = {
    "1.1": "词义理解", "1.2": "词汇辨析", "1.3": "词性与构词法",
    "1.4": "固定搭配", "1.5": "拼写",
    "2.1": "时态与语态", "2.2": "非谓语动词", "2.3": "从句",
    "2.4": "特殊句式", "2.5": "主谓一致", "2.6": "冠词与介词",
    "2.7": "代词", "2.8": "情态动词", "2.9": "比较级最高级", "2.10": "名词形态",
    "3.1": "篇章结构", "3.2": "衔接手段", "3.3": "文体特征", "3.4": "主旨概括",
    "4.1": "语境理解", "4.2": "语言得体性", "4.3": "中式英语",
    "5.1": "阅读策略", "5.2": "七选五策略", "5.3": "完形策略",
    "5.4": "语法填空策略", "5.5": "读后续写策略", "5.6": "应用文策略", "5.7": "听力策略",
    "6.1": "记忆方法", "6.2": "复习规划", "6.3": "时间管理", "6.4": "自我监控",
    "unknown": "未确定",
}

LEVEL_LABELS = {
    "L1": "L1 识记", "L2": "L2 理解", "L3": "L3 应用", "L4": "L4 分析",
    "unknown": "不适用",
}


def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer((host, port), Handler)
    if ACCESS_TOKEN:
        print(f"ETA 原型启动: http://localhost:{port}  [token 保护已启用]")
    else:
        print(f"ETA 原型启动: http://localhost:{port}  [无 token，仅限本机访问]")
    print(f"历史记录文件: {HISTORY_FILE}")
    server.serve_forever()


if __name__ == "__main__":
    main()
