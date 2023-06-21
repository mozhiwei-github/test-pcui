# PC端UI自动化测试

[TOC]

**测试项目**

- 毒霸
- PDF
- 导航

**目录结构**

```text
├── common                 # 功能库子模块
│   ├── api                  # api请求目录
│   ├── tools                  # 各项目常用工具函数
│   ├── config                 # 配置文件目录
│   │   ├── common.yml         # 通用配置文件
│   │   └── config.yml         # 案例配置文件
│   └── exe                  # exe文件目录
├── duba                   # 毒霸项目目录
│   ├── api                  # 毒霸api请求目录
│   ├── PageObjects          # 毒霸页面对象
│   ├── PageShot             # 毒霸页面截图
│   ├── TestCases            # 毒霸测试用例
│   ├── config.py            # 毒霸配置文件
│   ├── contants.py          # 毒霸常量文件
│   └── page_resource.py     # 毒霸页面资源配置文件
├── dubateam               # 毒霸团队版项目目录
├── conew                  # 可牛产品项目目录
├── daohang                # 导航项目目录
├── wallpaper              # 壁纸项目目录
├── liebao                 # 猎豹浏览器项目目录
├── liebaoent              # 猎豹浏览器企业版项目目录
├── pcmaster               # 金牌电脑管家项目目录
├── drivergenius           # 驱动精灵项目目录
├── convert                # PDF转换器项目目录
├── reader                 # PDF阅读器项目目录
├── logs                   # 日志目录
├── auto_main.py           # tcservice.exe启动测试文件
├── conftest.py            # 共用pytest套件
├── requirements.txt       # 依赖库文件
├── run_ui_test.py         # 毒霸UI自动化测试启动脚本
└── README.md              # 自述文件
```

## 常用命令

### 获取项目

```bash
# 克隆项目及其子模块
git clone --recursive http://autotest.cf.com:10101/r/tc/dubatestpro.git

# 或者先克隆项目，然后拉取子模块
git clone http://autotest.cf.com:10101/r/tc/dubatestpro.git
git submodule init
git submodule update --recursive
```

### 更新子模块（common目录）

```bash
git submodule update --recursive
```

### 启动UI自动化测试

**运行UI自动化测试（指定用例）**

```bash
python run_ui_test.py base_cases/test_vip_center_open_operation.py
```

**运行UI自动化测试（指定用例，并启动allure报告服务）**
```bash
python run_ui_test.py base_cases/test_vip_center_open_operation.py -s
```

**运行UI自动化测试（指定用例，并生成html报告）**
```bash
python run_ui_test.py base_cases/test_vip_center_open_operation.py -g
```

### 构建导航python容器

```bash
sudo docker build -f daohang/Dockerfile.python -t daohang/python39a:v1.0.0 -t daohang/python39a:latest .
```

### 构建导航项目容器

```bash
sudo docker build -f daohang/Dockerfile -t daohang/ui:v1.0.0 -t daohang/ui:latest .
```

