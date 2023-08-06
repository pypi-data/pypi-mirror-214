

## 开发的小工具/小脚本的使用方式
# 1. 直接使用源码 - requirements.txt
# 2. 作为可安装的库-pip 安装使用 pypi wheel   setup.py
# 3. 作为命令行工具 excel-runner a.xlsx     setup.py
# 4. 做成直接可运行的（带界面的）app  pyqt5 + pyinstaller

## requirements.txt 和setup.py
# - requirements.txt: 作为源码使用时，表明依赖包
# - setup.py：打包安装和发布

def hi():
    print("hello")


if __name__ == "__main__":
    hi()