确实，你可以在命令行中临时更改你的`PATH`环境变量。首先，你需要知道脚本`clear_clean_go.py`的绝对路径，然后在你的命令行中输入以下命令：

```bash
export PATH=$PATH:/full/path/to/your/clear_clean_go/
```

请将`/full/path/to/your/clear_clean_go/`替换为你的脚本实际的完整路径。你可以使用`pwd`命令来找到当前目录的完整路径。

然后，就像我之前提到的，你需要给你的脚本添加执行权限：

```bash
chmod +x /full/path/to/your/clear_clean_go/clear_clean_go.py
```

并且你需要在你的脚本的顶部添加一个shebang行：

```python
#!/usr/bin/env python3
```

现在你应该可以在任何位置直接运行你的脚本：

```bash
clear_clean_go.py
```

这个`PATH`的更改只在当前的终端会话中有效。如果你关闭并重新打开你的终端，你将需要重新执行这个`export`命令。

这条`export`命令用于在 Unix 和 Unix-like 操作系统（如 Linux 和 macOS）中设置或修改环境变量。

1. `export`是一个 shell 命令，用于将后面定义的变量设置为环境变量，使得该变量在当前 shell 会话和所有从当前会话启动的子会话中可用。
   
2. `PATH`是一个特殊的环境变量，它告诉 shell 在哪些目录下搜索可执行文件。这些目录由冒号 (:) 分隔。

3. `$PATH`是 shell 用来引用环境变量 PATH 的当前值的方式。

4. `:`是一个分隔符，用于在已有的 PATH 值后面添加新的路径。

5. `/full/path/to/your/clear_clean_go/`是你想要添加到 PATH 中的新目录。这应该替换为你的 `clear_clean_go.py` 脚本所在的实际目录。

所以，当你运行这个命令 `export PATH=$PATH:/full/path/to/your/clear_clean_go/` 时，你告诉 shell 把你的 `clear_clean_go.py` 脚本所在的目录添加到 PATH 环境变量中去。这样，你就可以在任何位置运行你的脚本，因为 shell 会在 PATH 中列出的所有目录中查找可执行的脚本和程序。

## ----#  关于版本非最新的情况 
你可以在Python脚本中读取`setup.py`文件的版本号，然后在shell脚本中使用这个版本号来指定安装。以下是一种可能的实现方式：

1. 在`renew_setup_version.py`脚本的最后，将新的版本号写入一个临时文件，如`new_version.txt`：

```python
# 在 renew_setup_version.py 的最后添加以下代码
with open('new_version.txt', 'w') as f:
    f.write(new_version)
```

2. 在你的`upload_new_version.sh`脚本中，读取这个新的版本号，并使用它来指定安装：

```bash
#!/bin/bash

# Update version number in setup.py
echo "Update version number in setup.py..."
python3 ./clear_clean_go_upgrage/renew_setup_version.py

echo "Removing old distributions..."
rm -rf ./dist/*

echo "Building new distribution..."
python setup.py sdist bdist_wheel

echo "Uploading new distribution to PyPI..."
twine upload dist/*

echo "Uninstalling old version of kangforecast..."
pip uninstall -y kangforecast

# Set the waiting time
WAIT_TIME=20

echo "Waiting for the server to update to the latest version...we set 20 seconds. Please take a break or have a cup of coffee."
for ((i=0; i<$WAIT_TIME; i++)); do
  printf "\rWaiting... [%-20s] %d sec" $(printf '%0.s#' $(seq 1 $i)) $i
  sleep 1
done
printf "\n"

echo "Waiting for the server to update to the latest version..."
sleep 20  # waits for 60 seconds. Adjust this value as needed.

# Read the new version number
NEW_VERSION=$(cat new_version.txt)

echo "Installing new version of kangforecast..."
pip install --no-cache-dir kangforecast==$NEW_VERSION

echo "All done!"
```

以上脚本将首先卸载旧版本的`kangforecast`，然后安装你在`setup.py`中指定的新版本。你可以根据你的需求调整这个脚本。
---

