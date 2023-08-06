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

