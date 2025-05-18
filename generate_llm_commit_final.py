# this file is used for generating review comments for a PR.
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
def llm_review(code_diffs):
    # 将所有文件的diff合并到一个prompt中
    all_diffs = ""
    for file_info in code_diffs:
        patch = file_info['patch']
        # 处理patch，添加行号信息
        lines = patch.split('\n')
        new_lines = []
        line_number = 0
        
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                # 这是新增的行，添加行号信息
                line_number += 1
                new_lines.append(f"+[行号:{line_number}] {line[1:]}")
            elif line.startswith(' '):
                # 这是上下文行，也需要计算行号
                line_number += 1
                new_lines.append(line)
            else:
                # 其他行（如@@行或-行）保持不变
                new_lines.append(line)
        
        modified_patch = '\n'.join(new_lines)
        #all_diffs += f"文件: {file_info['filename']}\n{modified_patch}\n\n"
        all_diffs += f"文件: {file_info['filename']}\n{file_info['patch']}\n\n"
        print(f"""all_diffs is \n{all_diffs}""")
    
    prompt = f"""你是一个代码审查机器人。请对以下 diff 代码做审查，给出有且仅有3条、准确定位的 review comments，你的输出格式为应该为：

[
  {{"file": "文件名", "line": 行号, "comment": "内容"}}
]

注意：行号已经在每行前面标注为 "+[行号:X]"，请直接使用这个行号。

代码diff如下：
{all_diffs}

请严格按照输出格式输出。方便我直接通过 json.loads 解析。我注意到你返回经常尝试使用```json```进行markdown渲染，\
    请不要这样做，这会导致解析错误。
"""
    resp = requests.post(
        "https://api.siliconflow.cn/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "Pro/deepseek-ai/DeepSeek-V3",  
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 4096,
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
def post_review_comments(comments):
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    # 获取commit SHA只需要一次，避免重复API调用
    commit_sha = get_latest_commit_sha()
    for c in comments:
        data = {
            "body": c["comment"],
            "commit_id": commit_sha,
            "path": c["file"],
            "side": "RIGHT",
            # 根据GitHub PR评论的实际显示情况调整行号
            "line": c["line"]  # 修改为-1而不是-2
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
    # 不再对每个文件单独处理，而是将所有文件的diff一起发送给LLM
    comments_str = llm_review(files)
    import json
    comments = json.loads(comments_str)
    # 直接提交所有评论（不超过3条）
    post_review_comments(comments)

if __name__ == "__main__":
    main()