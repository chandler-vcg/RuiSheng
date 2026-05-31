# 贡献指南

感谢您对睿声项目的兴趣！我们欢迎任何形式的贡献，包括但不限于提交问题报告、功能建议、代码提交等。

## 如何贡献

### 1. 报告问题

如果您发现任何bug或有功能建议，请通过GitHub Issues提交。请包含以下信息：
- 清晰的问题描述
- 复现步骤
- 预期行为与实际行为
- 您的环境信息（操作系统、Python版本等）

### 2. 代码贡献

#### 开发流程

1. **Fork 本仓库**
   - 点击GitHub页面右上角的"Fork"按钮

2. **克隆您的 Fork**
   ```bash
   git clone https://github.com/您的用户名/ruisheng.git
   cd ruisheng
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/您的功能名称
   # 或者修复bug
   git checkout -b fix/您修复的bug描述
   ```

4. **进行开发**
   - 遵循项目的代码规范
   - 编写有意义的提交信息
   - 确保代码可以正常运行

5. **提交更改**
   ```bash
   git add .
   git commit -m "Add: 添加您的功能描述"
   ```

6. **推送到您的 Fork**
   ```bash
   git push origin feature/您的功能名称
   ```

7. **创建 Pull Request**
   - 前往原始仓库页面
   - 点击"New Pull Request"按钮
   - 选择您的分支并描述您的更改

### 3. 代码规范

#### Python 代码
- 遵循 PEP 8 编码规范
- 使用有意义的变量和函数命名
- 添加必要的注释和文档字符串

#### Vue/前端代码
- 遵循 Vue 3 Composition API 风格
- 使用清晰的组件命名
- 组件文件使用 PascalCase 命名

### 4. 测试

在提交PR之前，请确保：
- 新功能已进行适当测试
- 现有功能未被破坏
- 代码没有明显的语法或逻辑错误

## 开发环境设置

### 前置要求
- Python 3.9+
- Node.js 16+
- Git

### 克隆仓库
```bash
git clone https://github.com/您的用户名/ruisheng.git
cd ruisheng
```

### 设置后端
```bash
cd GPT-SoVITS
pip install -r requirements.txt
```

### 设置前端
```bash
cd ruisheng2025
npm install
```

## 分支管理

- `main` - 主分支，包含稳定版本
- `develop` - 开发分支，用于集成新功能
- `feature/*` - 功能分支
- `fix/*` - 修复分支

## 问题反馈

如果您在贡献过程中遇到任何问题，欢迎通过以下方式联系：
- GitHub Issues
- 提交问题讨论

## 行为准则

请尊重其他贡献者，保持友好和专业的交流态度。我们期望所有参与者都能遵守开源社区的行为准则。

感谢您的贡献！
