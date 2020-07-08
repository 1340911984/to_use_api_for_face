import requests  # 网络访问控件
from json import JSONDecoder  # 互联网数据交换标准格式
import cv2 as cv  # 图像处理控件

http_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"  # face++apiDETECT模块
key = ""
secret = ""
def com(image_file1,image_file2):
    try:
        data = {"api_key": key, "api_secret": secret}
        # 数据格式化准备发送到face，词典格式json
        files = {"image_file1": open(image_file1, "rb"), "image_file2": open(image_file2, "rb")}  # 准备打开
        response = requests.post(http_url, data=data, files=files)  # 用post方式（还有get）发送数据到网站
        req_con = response.content.decode('utf-8')  # 网页解码
        req_dict = JSONDecoder().decode(req_con)  # 把json解码成python词典格式
        return req_dict
    except BaseException as e:
        fail ='失败了'
        return fail



if __name__ == '__main__':
    image_file1 = "C:\\Users\\86139\\Desktop\\Cache_51cb1462898756c..jpg"
    image_file2 = "C:\\Users\\86139\\Desktop\\87D0A5BA21AD1BCB5ADB888B96CE4F72.jpg"  # 图像位置
    res = com(image_file1, image_file2)
    face1 = res['faces1']
    face2 = res['faces2']
    face1_rect = 0
    face2_rect = 0
    num = 1
    try:
        for i in face1:
            face1_rect = str(i['face_rectangle'])
            print("图一中的" + "第" + str(num) + "个脸的位置" + face1_rect)
            num+=1

        num = 1
        for k in face2:
            face2_rect = str(k['face_rectangle'])
            print("图二中的" + "第" + str(num) + "个脸的位置" + face2_rect)
            num += 1

        conf = str(res['confidence'])

        print("两张图片中最高相似度为" + conf + '%')
    except BaseException as e:
        result = com(image_file1,image_file2)
        print(result)
        print("1.图片不是个人")
        print("2.图片人物实在是太多了")
        print("3.我太菜了写错了什么地方")

