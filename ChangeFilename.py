import os, re
import shutil
import asyncio

# 需要删除的文件所属的后缀
needDelFilesuffixs = ['-gl.wav']
# 需要排除的文件夹，不去遍历的文件夹及其子集
excludeDirNames = ['table', 'logging']

# 查看两个列表的元素是否有交集
def inter(a, b):
    return list(set(a) & set(b))

# 批量删除指定的文件
async def delect_allocate_file(file_dir):
    dle_number = 0
    # 获取这个路径下所有的文件和文件夹
    for root, dirs, files in os.walk(file_dir, topdown=True):
        isExclude = False
        for excludedir in excludeDirNames:
            if not (excludedir in root):
                isExclude = True

        if isExclude:
            for filename in files:
                file_name_only, file_extension = os.path.splitext(filename)
                print(file_name_only, file_extension)
                if (len(needDelFilesuffixs) > 0):
                    for del_suffix in needDelFilesuffixs:
                        if "-gl" in file_name_only:
                            fileFullName = os.path.join(root, filename)
                            os.remove(fileFullName)
                            print("删除 %s" % (fileFullName))
                            dle_number += 1
                # print(os.path.join(root, filename))

    print("总共删除了 %s 个文件 " % (dle_number))


async def files_pos():
    await delect_allocate_file(r'./TEST')


def reName(file_path):
    list = os.listdir(file_path)
    newname_num = 1
    for oldname in list:
        newname = str(newname_num) + ".wav"
        os.rename(os.path.join(file_path, oldname), os.path.join(file_path, newname))
        newname_num += 1
    #将文件名批量替换
    print('批量重命名运行完成！')

if __name__ == '__main__':
    asyncio.run(files_pos())
    filepath = './TEST' #定义文件路径
    reName(filepath) #调用reName函数


