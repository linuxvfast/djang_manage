from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from cmdb import models
from django.shortcuts import redirect
import json


def add_info(request):
    '''
    添加测试数据
    :param request:
    :return:
    '''
    # models.Host.objects.create(nid=1,hostname='www.a.com',ip='192.168.1.123',port=22,module_id=1)
    # models.Host.objects.create(nid=2,hostname='www.b.com',ip='192.168.1.12',port=3389,module_id=2)
    # models.Application.objects.create(name='web')
    # models.Application.objects.create(name='后台')
    # models.Application.objects.create(name='db')
    # models.Application.objects.create(name='设计')
    # obj = models.Application.objects.filter(id=2).first()
    # obj.r.add(*[3,4,5,6])
    return HttpResponse('OK')

def business(request):
    '''
    获取busines表中的数据显示在模板文件中
    :param request:
    :return:
    '''
    v1 = models.Business.objects.all()  #对象
    print(v1)
    v2 = models.Business.objects.all().values('id','caption')   #字典
    v3 = models.Business.objects.all().values_list('id','caption')  #元组
    print(v2)
    print(v3)
    return render(request,'business.html',{'v1':v1,'v2':v2,'v3':v3})

def hosts(request):
    '''
    获取host表中的数据显示在模板文件中
    :param request:
    :return:
    '''
    if request.method == 'GET':
        busines_list = models.Business.objects.all()
        v1 = models.Host.objects.filter(nid__gt=0)
        # for row in v1:
        #     print(row.nid,row.hostname,row.ip,row.port,row.module_id,row.module.id,row.module.caption)
        #对象中取值时使用.进行取值
        v2 = models.Host.objects.filter(nid__gt=0).values('nid','hostname','ip','port','module_id','module__id','module__caption')
        # print(v2)
        # for row in v2:
        #     print(row['nid'],row['hostname'],row['ip'],row['port'],row['module_id'],row['module__id'],row['module__caption'])
        
        v3 = models.Host.objects.filter(nid__gt=0).values_list('nid','hostname','ip','port','module_id','module__id','module__caption')
        # print(v3)
        # for row in v3:
        #     print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        return render(request,'host.html',{'v1':v1,'v2':v2,'v3':v3,'busines_list':busines_list})
    elif request.method == 'POST':
        host_name = request.POST.get('hostname',None)
        host_ip = request.POST.get('ip',None)
        host_port = request.POST.get('port',None)
        businesid = request.POST.get('module_id',None)
        # print(host_name,host_ip,host_port,businesid)
        models.Host.objects.create(hostname=host_name,ip=host_ip,port=host_port,module_id=businesid)
        return redirect('/cmdb/host')

def test_ajax(request):
    '''host表添加功能'''
    # print(request.method,request.GET.get('hostname',None),request.GET.get('ip',None),sep='\t')
    ret = {'status': True, 'error': None, 'data': None}
    try:
        host_name = request.POST.get('hostname', None)
        host_ip = request.POST.get('ip', None)
        host_port = request.POST.get('port', None)
        businesid = request.POST.get('module_id', None)
        if host_name and len(host_name) > 5:
            models.Host.objects.create(hostname=host_name,
                                       ip=host_ip,
                                       port=host_port,
                                       module_id=businesid)
            return HttpResponse('接收成功')
        else:
            ret['status'] = False
            ret['error'] = "主机名太短了"
    except Exception as e:
        ret['status'] = False
        ret['error'] = '请求错误'
    return HttpResponse(json.dumps(ret))

def edit_ajax(request):
    '''host编辑功能'''
    ret = {'status': True, 'error': None, 'data': None}
    try:
        host_name = request.POST.get('hostname', None)
        host_ip = request.POST.get('ip', None)
        host_port = request.POST.get('port', None)
        businesid = request.POST.get('module_id', None)
        nid = request.POST.get('nid', None)
        # print(nid,businesid,host_port,host_ip,host_name)
        if host_name and len(host_name) > 5:
            models.Host.objects.filter(nid=nid).update(
                hostname=host_name,
                ip=host_ip,
                port=host_port,
                module_id=businesid)
        else:
            ret['status'] = False
            ret['error'] = "主机名太短了"
    except Exception as e:
        ret['status'] = False
        ret['error'] = '请求错误'
    return HttpResponse(json.dumps(ret))

def add_more_to_more(request):
    print(type(request))
    from django.core.handlers.wsgi import WSGIRequest
    print(request.environ)
    if request.method == 'GET':
        del_nid = request.GET.get('del_nid',None)
        app_list = models.Application.objects.all()
        host_list = models.Host.objects.all()
        print(del_nid)
        return render(request,'app.html',{'app_list':app_list,'host_list':host_list})
    elif request.method == 'POST':
        app_name = request.POST.get('app_name',None)
        host_list = request.POST.getlist('host_list',None)
        print(app_name,host_list)
        obj = models.Application.objects.create(name=app_name)
        obj.r.add(*host_list)
        return redirect('/cmdb/add_more_to_more')