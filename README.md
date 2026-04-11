<div align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
    </a>
    <a href="https://www.ixigua.com/">
        <img src="https://img.shields.io/badge/platform-ixigua-orange" alt="iXigua">
    </a>
</div>

# 🍉 Watermelon Platform

**✨ 专业的西瓜视频数据采集解决方案，支持用户信息、视频详情、评论全量抓取与关键词搜索**

当你需要让 AI Agent 感知西瓜视频内容生态——自动采集评论舆情、分析用户观点、驱动内容运营策略——第一道墙往往不是模型能力，而是**平台数据获取能力的缺失**。

本项目做的事很简单：把这道墙拆掉。

**⚠️ 严禁用于爬取用户隐私、违规商业用途！本项目仅供学习与技术研究使用，后果自负。**

## 🌟 功能特性

- ✅ **用户信息采集**
  - 获取西瓜视频创作者主页详情（`AuthorDetailInfo`）
- 🎬 **视频信息采集**
  - 获取视频完整元数据（`_SSR_HYDRATED_DATA`）
  - 支持 AES-CBC 解密还原真实视频播放地址
- 📋 **视频列表采集**
  - 自动翻页，获取指定用户发布的全部视频
- 💬 **评论全量采集**
  - 支持视频**外层评论**抓取，自动翻页
  - 支持**楼中楼（子评论/回复）**递归获取
- 🔍 **关键词搜索**
  - 支持按关键词搜索视频，可指定返回数量

## 🛠️ 快速开始

### ⛳ 运行环境

- Python 3.10+

### 🎯 本地安装

```bash
pip install -r requirements.txt
```

### 🚀 运行项目

```python
from watermelon_api import WatermelonApi
from builder.auth import WatermelonAuth

api = WatermelonApi()
auth = WatermelonAuth()
auth.perepare_auth("your_cookie_str_here")

# 获取用户信息
user_url = 'https://www.ixigua.com/home/253336705311643'
info, msg = api.get_user_info(user_url, auth)

# 获取视频全部评论（含子评论）
work_url = 'https://www.ixigua.com/7387380613373755967'
comments, msg = api.get_work_all_comment(work_url, auth)
```

### 🎨 Cookie 配置

在浏览器中打开 [www.ixigua.com](https://www.ixigua.com)，**登录账号**后按 `F12` 打开开发者工具，点击「网络」→ 找任意一个 API 请求 → 复制请求头中的 `Cookie` 字段值。

将获取到的 Cookie 字符串作为 `cookie_str` 参数传入 `WatermelonAuth.perepare_auth()`：

```
UIFID_TEMP=xxx; csrf_session_id=xxx; msToken=xxx; ...
```

## 📡 接口说明

### `get_user_info(home_url, auth)`

获取西瓜视频**创作者主页**详情信息。

| 参数       | 类型            | 说明              |
|----------|---------------|-----------------|
| home_url | str           | 创作者主页 URL       |
| auth     | WatermelonAuth | 鉴权对象           |

---

### `get_work_info(work_url, auth)`

获取**视频详情**，包含完整元数据与加密视频资源。

| 参数       | 类型            | 说明        |
|----------|---------------|-----------|
| work_url | str           | 视频页面 URL  |
| auth     | WatermelonAuth | 鉴权对象      |

---

### `get_user_all_work(home_url, auth)`

获取指定用户发布的**全部视频列表**，自动翻页。

| 参数       | 类型            | 说明         |
|----------|---------------|------------|
| home_url | str           | 创作者主页 URL  |
| auth     | WatermelonAuth | 鉴权对象       |

---

### `get_work_all_comment(home_url, auth)`

获取视频**全部评论**（含所有楼中楼子评论），自动翻页。

| 参数       | 类型            | 说明       |
|----------|---------------|----------|
| home_url | str           | 视频页面 URL |
| auth     | WatermelonAuth | 鉴权对象     |

**响应示例**

```json
[
  {
    "id": "7363239522114634250",
    "comment": {
      "user_name": "用户昵称",
      "text": "评论内容",
      "reply_count": 2,
      "reply_list": [
        {
          "user": { "name": "回复用户" },
          "content": "子评论内容"
        }
      ]
    }
  }
]
```

---

### `search_some_by_num(query, num, auth)`

按**关键词搜索**视频，指定最大返回数量。

| 参数    | 类型            | 说明         |
|-------|---------------|------------|
| query | str           | 搜索关键词      |
| num   | int           | 最多返回视频条数   |
| auth  | WatermelonAuth | 鉴权对象       |

**请求示例**

```python
works, msg = api.search_some_by_num('拜登', 20, auth)
```

## 🔐 视频地址解密

部分视频资源经过 AES-CBC 加密，可使用内置工具函数还原播放地址：

```python
from utils.watermelon_utils import aes_decrypt

main_url = videoDash['dynamic_video']['main_url']
ptk = videoDash['ptk']
real_url = aes_decrypt(main_url, ptk)
```

## 🐳 Docker 部署

```bash
docker build -t watermelon-platform .
docker run -d watermelon-platform
```

## 📁 项目结构

```
watermelon/
├── watermelon_api.py       # 核心 API 封装
├── builder/
│   ├── auth.py             # 鉴权对象
│   ├── header.py           # 请求头构建器
│   └── params.py           # 请求参数构建器
├── utils/
│   └── watermelon_utils.py # 工具函数（Cookie 解析、AES 解密）
├── static/                 # 静态资源
├── Dockerfile
└── .env
```

## 🍥 日志

| 日期       | 说明                                        |
|----------|-------------------------------------------|
| 26/04/11 | 项目初始化，完成用户信息、视频信息、评论全量抓取及搜索 API 封装 |

## 🤝 欢迎贡献 PR

本项目欢迎任何形式的贡献！如果你有新功能想法、Bug 修复或文档改进，欢迎提交 PR。

- Fork 本仓库并在新分支上开发
- 保持代码风格与现有代码一致
- PR 描述中请简要说明改动内容和目的
- 也欢迎通过 Issue 提出建议或报告问题

## 🧸 额外说明

1. 感谢 star⭐ 和 follow📰！不时更新
2. 作者的联系方式在主页里，有问题可以随时联系我
3. 可以关注下作者的其他项目，欢迎 PR 和 issue
4. 感谢赞助！如果此项目对您有帮助，请作者喝一杯奶茶~~ （开心一整天😊😊）
5. thank you~~~
