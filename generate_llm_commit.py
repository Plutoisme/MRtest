import requests
import os

# 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Plutoisme/MRtest"
PR_NUMBER = 1
LLM_API_KEY = os.getenv("LLM_API_KEY")

# 获取 PR 的 diff
def get_pr_diff():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

# 调用 LLM 生成 review comments
def llm_review(code_diff):
    prompt = f"""你是一个代码审查机器人。请对以下 diff 代码做审查，给出不超过3条、准确定位的 review comments，格式为：
[
  {{"line": 行号, "comment": "内容"}}
]
代码diff如下：
{code_diff}
"""
    resp = requests.post(
        "https://api.siliconflow.cn/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "Qwen/QwQ-32B",  # 推荐使用官方文档中的模型名
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"}
        }
    )
    resp.raise_for_status()
    print("LLM response:")
    print(resp.json()["choices"][0]["message"]["content"])
    return resp.json()["choices"][0]["message"]["content"]

# 提交 review comments 到 PR
def post_review_comments(comments, file_path):
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    for c in comments:
        data = {
            "body": c["comment"],
            "commit_id": get_latest_commit_sha(),
            "path": file_path,
            "side": "RIGHT",
            "line": c["line"]
        }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()

def get_latest_commit_sha():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()[-1]["sha"]

def main():
    files = get_pr_diff()
    for f in files:
        print("dealing file: ", f["filename"])
        code_diff = f["patch"]
        print("code diff: ", code_diff)
        comments_str = llm_review(code_diff)
        import json
        comments = json.loads(comments_str)
        post_review_comments(comments, f["filename"])

if __name__ == "__main__":
    main()