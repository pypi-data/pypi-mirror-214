# 关于FreeplanIr的简单介绍 
    用于解析freeplan脑图的*.mm文件，输出为从根节点到子节点的数据
    
    例如你的脑图 a-b-c
                  -d-e
                  -f-g
                h-i-g
                 -k-l
        那么最终的输出为[
            [a, b, c],
            [a, d, e],
            [a, f, g],
            [h, i, j],
            [h, k, l]
        ]
## 使用方法
    安装相关模块后
    导入模块和类 form FreeplanIr import FreeplanIr
    file_path = r"XXXX.mm" # 你的文件路径
    test_plan = FreeplanIr(file_path) # 实例化类
### 获取转换数据
    datas = test_plan.plan_test() # 调用plan_test方法即可，返回为转换好数据
    print(datas)  
### 下载为xlxs
    path = test_plan.download() # 调用plan_test方法即可，返回为文件保存地址
    print(datas)  
  此方法返回的结果就是如上所说，需要注意次方返回目前仅支持所有节点的长度一致。
### 下载为csv，导入禅道中生成测试用例
    path = test_plan.download_chandao() # download_chandao，返回为文件保存地址
    print(datas)  
  使用此方法无需做其他数据源头更改
    

  