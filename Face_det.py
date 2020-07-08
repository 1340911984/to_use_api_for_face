# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
def find_face(filepath):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = ""
    secret = ""

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    fr = open(filepath, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        resp = urllib.request.urlopen(req, timeout=5)
        # urllib.request.close()
        qrcont = resp.read()
        qrcont = qrcont.decode('utf-8')
        dictinfo = eval(qrcont)
        FACE = dictinfo['faces']

        result = '\n'
        result = result + '共检测到' + str(len(FACE)) + '张人脸' + '\n'
        num = 1
        for i in FACE:
            try:#可能会损失属性
                sx = i['attributes']
            except BaseException as e:
                return result, num-1, FACE

            result = result + "第" + str(num)  + "个人的数据" + '\n'
            num += 1

            gen = sx['gender']['value']
            result = result + '性别' + str(gen) + '\n'

            age = sx['age']['value']
            result = result + '年龄' + str(age) + '\n'

            smi = sx['smile']['value']
            result = result + '微笑率:' + str(smi) + '%' + '\n''\n'

        return result,len(FACE),FACE
    except urllib.error.HTTPError as e:
        return str(e.read().decode('utf-8'))

if __name__ == '__main__':
    try:
        file="C:\\Users\\86139\\Desktop\\AAD3ED227D47F25B1A899A383FFA747B.jpg"
    except BaseException as e:
        print("在这就有问题，那估计您的路径有毛病哈")
    try:
        fine_faces_notmatterwhat,num_people,FACES = find_face(file)
        print(fine_faces_notmatterwhat) #可能是识别了很多人 但是读取不到精准信息 这里说出一共多少人
        num = 0
        for i in FACES:
            num+=1
            print(str(num)+'号人物在图片里的像素位置')
            top = 'top';left = 'left';width='width';height = 'height'
            print(top+': '+str(i['face_rectangle']['top'])+', '
                 +left+': '+str(i['face_rectangle']['left'])+', '
                 +width+': '+str(i['face_rectangle']['width'])+', '
                 +height+': '+str(i['face_rectangle']['height']))
        print( str(num_people) +'个人可以完整识别' + '\n')#这里说出多少人的属性可以读取
        '''   请注意 本文中的属性代表为age/sex/smile等并非是脸部的位置这种    '''
    except BaseException as e:
        result = find_face(file)
        print(result)
        print("1.图片不是个人")
        print("2.图片人物实在是太多了")
        print("3.我太菜了写错了什么地方")