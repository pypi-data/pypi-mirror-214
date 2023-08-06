# Python:mml-qae库帮助文档
## 使用环境
+ Python环境:最好使用3.7.2。如果不在3.7.2环境下出现报错，请区分ImportError(由mml内部引入包的版本错误)和其他错误。
+ 编译格式：没什么好说的，Python默认使用的Unicode和UTF-8解码格式。
+ 请尽可能保持mml-qae包的最新版本。1.2及以前的版本并不全面！
---
## 开发公告
    此处将放置每一个的更新日志.与历史版本一栏不同的是,这里是实时更新且更加详细的.
+ 1.0.0 2023.5.14 初代版本.框架构建.
+ 1.0.1 ----------- 略微扩充了方法.
+ 1.0.1.1 --------- 向pypi.org中扩充了项目描述.
+ 1.0.1.2 --------- 向pypi.org中扩充了说明文档.(由于作者脑抽忘记再1.0.1.1时上传了不得不新增一个版本)
+ 1.0.1.3 --------- 加入了子模块MoreErrors以提供更多错误支持.
+ 1.0.1.4 2023.5.15 突然引起的恶性错误,此为紧急修复版本.
+ 1.0.2.10 2023.5.26 中文语言处理(简易版).在测试中本版本出现了一些问题待修复.请见谅.
+ 1.0.2.11 2023.6.10 修复了上次更新的遗留问题.
+ 1.0.3.1 2023.6.17  增加了基于socket的简易网络模块.
---
## 开发者发言
+ We now have packages to deal with big data like statsmodels, sklearn, Spark, or packages to deal with natural language, such as jieba or spaCy. I admit that those packages are really useful while facing whith tons of csv data. BUT! I think we need a nicer package to deal with data, don't we? So, the mml-qae package(the whole name is My Machine Learning-Quicker and Easier) is here to help you. Alright, so, I have to say that I didn't do anything new, but I put those complex codes together into grand-new methods, so that you will be able to deal with MachineLearning and DataDealing. I started this project on 14th, May 2023 with version 1.0.1. In a more proper way, I worked on this project with my team ETRO(to see the Author's Email). I promise to update it regularly, but I cannot say how long the interval between two updataions will be for certain. Another thing needed to be paid attentioned is, this package only works at Python3.7.2, and you MUST pip install the packages needed in mml, like statsmodels. I will speak of all those packages you need to preinstall in README.md. Last but not least, never use 'from mml-qae import *'. Many methods in mml are the same name with the built-in functions! That'll be all, and have fun with MachineLearning and DataDealing!
+ Packages needed
> + statsmodels
> + sklearn
> + jieba
> + spaCy
> + pandas
> + numpy
> + matplotlib
> + wordcloud
> + opencv-python
---
## Documents for easily using
### builtins
In this package, it usually doesn't have a started print. But if you DO NOT have all the packages we need, it will raise a ImportError just after import. The common builtin values are like __versions__,__name__ or sth. like __doc__.
### Chinese_dealing
With this package, you can use the following methods:
#### add(words,tag)
The two values are all must-needed. They must be same-shape lists, and the elements of both must correspond one-to-one. All elements must be strings. They will be added as new words one by one in the jieba.
#### make_words_list(text)
The parameter text must be given. This method will split the given text into several words and return the list form.
#### make_words_list_with_tags(text)
The parameter text must be given. This method splits the given text into several words and returns a list format, including the part of speech of each word; The return format is two lists, each containing participles and corresponding parts of speech.
#### make_words_list_with_extra_words(text,path1,path2)
To use this method, you must download jiebapos.xlsx and data3-1.txt from Git at https://github.com/ZYpS-leader/mml-qae. Pass in their absolute paths on the local machine, which should end with ".../jiebapos. xlsx" and ".../data3-1. txt". The return value is the same as make_words_list_with_tags method. 
