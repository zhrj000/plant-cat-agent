#!/bin/bash

# 设置 Git 仓库并推送到 GitHub 的脚本
# 使用方法：bash setup_git.sh

echo "🚀 开始设置 Git 仓库并推送到 GitHub..."

# 1. 初始化 Git 仓库
echo "📦 初始化 Git 仓库..."
git init

# 2. 添加所有文件（排除 .env 文件）
echo "📁 添加文件到 Git..."
git add .

# 3. 创建初始提交
echo "💾 创建初始提交..."
git commit -m "$(cat <<'EOF'
🎉 初始提交：植物猫咪安全助手 - AI Agent 完整思考过程版

项目特色：
🤖 完整展示 AI Agent 5 步思考过程：
  1. 📥 感知 - 接收用户输入
  2. 🧠 思考 - LLM 分析意图并选择工具
  3. 🎯 决策 - 解析 LLM 选择，决定工具
  4. ⚡ 行动 - 执行选定的工具
  5. 📊 评估 - 判断任务完成情况

🔐 安全特性：
  - API 密钥存储在 .env 文件中
  - 不会上传到 Git 仓库
  - 自动处理代理问题

🚀 功能：
  - 智能工具选择（数据库查询、AI 专家分析等）
  - 完整可视化 Agent 思考过程
  - 支持 DeepSeek API
  - 详细的配置和文档

📚 包含完整文档：
  - README.md - 项目介绍
  - SECURITY_GUIDE.md - 安全配置指南
  - EXAMPLES.md - 使用示例
  - CONFIG_GUIDE.md - 配置说明

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>
EOF
)"

# 4. 添加远程仓库
echo "🌐 添加远程仓库..."
git remote add origin https://github.com/zhrj000/plant-cat-agent.git

# 5. 推送到 GitHub
echo "🚀 推送到 GitHub..."
git branch -M main
git push -u origin main

echo "✅ 完成！项目已推送到 GitHub：https://github.com/zhrj000/plant-cat-agent"