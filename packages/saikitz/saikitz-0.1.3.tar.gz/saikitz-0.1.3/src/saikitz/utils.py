from IPython.display import Markdown, display

__all__ = ["printmd","lastoflistdict"]

def printmd(string):
    """用于在Jupyter Notebook中打印Markdown格式的字符串"""
    display(Markdown(string))

def lastoflistdict(dict_list:list[dict], key:any, value:any) -> int :
    """
    用于获取固定字典组成的列表中满足要求的最后一个字典的索引。
    """
    max_index = -1
    n = len(dict_list)
    for i in range(n) :
        if key in dict_list[i].keys() :
            if dict_list[i][key] == value :
                max_index = i
    return max_index
