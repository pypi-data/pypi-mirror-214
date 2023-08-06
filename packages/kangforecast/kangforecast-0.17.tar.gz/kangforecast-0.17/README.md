python setup.py sdist bdist_wheel
twine upload dist/*
pip install kangforecast

-关于测试

在Python项目中，通常将测试代码放在一个名为"tests"的目录下，这个目录与你的"src"（源代码）目录是平行的。在你的情况下，源代码目录是"kangforecast"，因此你可以创建一个与"kangforecast"平行的新目录，命名为"tests"。如下所示：

```bash
kang@Love-Grace release_pypi$ tree
.
├── README.md
├── build
│   └── bdist.macosx-12-arm64
├── data
│   └── special_dates.csv
├── dist
│   ├── kangforecast-0.1-py3-none-any.whl
│   └── kangforecast-0.1.tar.gz
├── kangforecast
├── tests
├── kangforecast.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
└── setup.py
```

你可以在"tests"目录中添加你的测试代码。例如，你可以创建一个名为"test_kangforecast.py"的文件。这样，你的测试代码不会被包含在你的发布包（即通过`pip install`安装的包）中，但是它仍然在你的项目结构中，可以方便你进行开发和测试。

然后，你可以使用测试框架（如`pytest`）来运行你的测试。只需在项目根目录下运行命令`pytest`，它会自动查找并运行所有的测试。

当然，你也可以在你的`setup.py`中指定`tests`目录，这样当其他人安装你的包并希望运行测试时，他们可以直接使用`python setup.py test`命令。如果你决定这样做，你可能需要对你的`setup.py`做一些修改，添加一些关于测试的配置。


--- 关于执行顺序。
当你在终端中键入python，操作系统会遍历你的PATH环境变量中的每一个目录，寻找名为python的可执行文件。

PATH是一个包含了多个文件路径的环境变量，各路径之间由冒号:分隔。当你键入命令时，系统会按照PATH中的顺序，从前往后查找每个路径，看看哪个路径中包含了你要执行的命令。

比如你的PATH可能类似这样：/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/kang/miniconda3/bin。

当你键入python后，系统首先会查看/usr/local/bin目录下是否有python这个可执行文件，如果有，就会运行它。如果没有，就会接着查看/usr/bin，以此类推。只有在前面的路径都没有找到python可执行文件的情况下，才会去查看/Users/kang/miniconda3/bin。

所以，你使用的Python解释器版本是由PATH中的顺序决定的。如果你希望使用Homebrew的Python解释器，你需要确保Homebrew的路径（通常是/usr/local/bin）在PATH中的位置比Miniconda的路径（/Users/kang/miniconda3/bin）靠前。你可以通过修改PATH来改变这个顺序。
------ for Homebrew:
export PATH="/usr/local/bin:$PATH"

source ~/.bashrc

------for conda
conda create -n new_env python=3.11
conda activate new_env
pip install kangforecast

------
您在 kangforecast 包中包含的数据文件无法通过 pip 安装后直接通过文件路径访问。这是因为当一个包被安装时，它的数据文件被存储在一个特定的位置，而不是在您的当前工作目录或相对路径下。

Python 的包分发工具（如 setuptools 或 distutils）提供了一种机制来包括这些数据文件，并在运行时访问它们。这通常是通过在 setup.py 文件中使用 package_data 关键字来实现的。

为了在您的 kangforecast 模块中访问这些数据文件，您需要使用 pkg_resources 模块，这是 setuptools 提供的一个模块。下面是如何使用它来访问您的数据文件的示例：


import pandas as pd
from pkg_resources import resource_filename

# Use resource_filename to get the path to your data file
datafile = resource_filename('kangforecast', 'data/special_dates.csv')

data = pd.read_csv(datafile)
print(data)
这段代码中，resource_filename 函数接收两个参数：包的名字和文件的相对路径（相对于包的路径）。它返回文件在文件系统中的绝对路径。

请注意，要使此代码工作，您需要确保在 setup.py 中正确地设置了 package_data 参数。例如：

python
Copy code
setup(
    ...
    package_data={
        'kangforecast': ['data/*.csv'],
    },
    ...
)
这会将所有 data 目录下的 CSV 文件包括到分发的包中。
----------
从你展示的目录结构来看，data文件夹是在kangforecast目录的外部，而不是作为kangforecast包的一部分。这就是为什么你的安装包没有包含这些数据文件。

要解决这个问题，你应该将data文件夹移动到kangforecast包内，然后重新打包和安装。你可以使用以下命令将data文件夹移动到kangforecast包内：


mv data kangforecast/

----

pip install --no-cache-dir --upgrade kanglib

-----

在Python中，__init__.py文件用于表示其所在的目录应被视为一个Python包，可以包含代码，也可以为空。这个文件会在导入包时首先被执行。如果你没有特殊的初始化代码需要执行，那么这个文件可以是空的。

下面是一个简单的__init__.py文件例子，它什么也不做：

python
Copy code
# This is an empty file.
如果你在包中有某些函数或者类需要导出，你可以在__init__.py文件中指定。例如，假设你有一个叫做forecast.py的模块，其中有一个prepare_data函数，你可以这样写__init__.py：

python
Copy code
from .forecast import prepare_data
然后，你就可以这样导入函数：

python
Copy code
from kangforecast import prepare_data
如果你没有特殊的导出需求，那么一个空的__init__.py文件就足够了。

在你的情况下，你需要在kangforecast目录下创建一个__init__.py文件（如果不存在的话）。然后，你需要确保你的数据文件（special_dates.csv）在kangforecast/data目录下，然后在你的setup.py文件中指定package_data={'kangforecast': ['data/*.csv']}。完成这些后，你应该就可以正确地打包和安装你的kangforecast包，并能够在安装后读取数据文件了。

最后，重新生成新版本的包，你需要更新setup.py中的版本号，比如改为version='0.3'，然后重新运行python setup.py sdist bdist_wheel来生成新的发行版本。
----
you are rght! we got it !!!  kang@Love-Grace release_pypi$ python test_kangforecast.py 
---------print file kangforecast.__file__:

/Users/kang/1.live_wit_GPT4/code_project/demand_forcast_retail/release_pypi/kangforecast/__init__.py
---------

   start_date    end_date             type
0  2022-06-01  2022-06-07         discount
1  2022-12-23  2022-12-26          holiday
2  2022-02-01   2022-02-5  extreme_weather


------为避免冲突，特别是 pip kanglib pip kangforecast 我们使用Docker 并建设镜像
uname -a
cat /etc/os-release

root@64fe8260fc20:/app/demand_forcast_retail/release_pypi# uname -a
Linux 64fe8260fc20 5.15.49-linuxkit-pr #1 SMP PREEMPT Thu May 25 07:27:39 UTC 2023 aarch64 GNU/Linux
root@64fe8260fc20:/app/demand_forcast_retail/release_pypi# cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 10 (buster)"
NAME="Debian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
-------
我们的系统是PRETTY_NAME="Debian GNU/Linux 10 (buster)" 稳定的linux 10. 


-------1. 完成数据准备。2. 数据处理  3. 数据展示。

---test_activity_special_date_v2.py  这个程序是可以用的。