def create(**kwargs):
    # 1 获取参数
    # 2 检查参数
    for filed in kwargs.keys():
        if not hasattr(idc,filed):
            print "参数错误,{} 不在idc这张表里".format(filed)
            raise Exception("params error: {}".format(filed))
        if not kwargs.get(filed,None):
            print "参数错误, {}不能为空".format(filed)
            raise Exception("{} 不能为空".format(filed))
    # 3传输数据库
    try:
        idc.objects.create(**kwargs)
    except Exception,e:
        print "commit error: {}".format(e.message)
        raise Exception("commit error")
    return idc.id

def get(**kwargs)
    #整理条件
    output = kwargs.get("output", [])
    limit = kwargs.get("limit", 0)
    order_by = kwargs.get("order_by", "id desc")
    where = kwargs.get("where", {})

    #验证
    #验证output
    if not isinstance(output, list):
        print "output 必须为list"
        raise  Exception("output 必须为list")
    for field in output:
        if not hasattr(idc,field):
            print "{} 这个输出字段不存在".format(field)
            raise  Exception("{} 这个输出字段不存在".format(field))
    #order
    tmp_order_by = order_by.split()
    if len(tmp_order_by) !=2:
        print "order by 参数不正确"
        raise Exception("order by 参数不正确")

    order_by_list = ['desc', 'asc' ]
    if tmp_order_by[1].lower() not in order_by_list:
        print "排序方式不正确"
        raise Exception("排序参数不正确，值可以为：{}".format(order_by_list))
    if not hasattr(Idc, tmp_order_by[0].lower()):
        print "排序字段不在表中"
        raise Exception("排序字段不在表中")

    # 验证limit
    if not str(limit).isdigit():
        print "limit 值必须为数字"
        raise Exception("limit 值必须为数字")

    data = idc.objects.filter

    return  data
