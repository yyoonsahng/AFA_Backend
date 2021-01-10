import mimetypes
import os, sys

import boto3
from django.http import HttpResponse

from .models import User

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import trimesh
from trimesh.exchange import obj
from trimesh.exchange import off
from trimesh.exchange import gltf
from trimesh.exchange import load
import json
import ast
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from pathlib import Path
import shutil

class UserView(APIView):
    """
    POST /user
    """

    def post(self, request):
        global convert_gltf
        user_serializer = UserSerializer(data=request.data)  # Request의 data를 UserSerializer로 변환
        print(user_serializer)
        BASE_DIR = Path(__file__).resolve().parent.parent
        print(BASE_DIR)
        if user_serializer.is_valid():
            print('save')
            print(user_serializer.save())  # UserSerializer의 유효성 검사를 한 뒤 DB에 저장
            user_queryset = User.objects.all()
            get_db = UserSerializer(User.objects.get(id=user_queryset[len(user_queryset) - 1].id))  # id에 해당하는 User의 정보를 불러온다
            print(get_db.data['image'])
            path = '.' + get_db.data['image']
            print(path)
            path2 = './occupancy_networks/demo/'
            shutil.copy(path, path2)
            print('current '+ os.getcwd())
            base = os.getcwd()
            os.chdir(base + '/occupancy_networks')
            os.system('python generate.py configs/demo.yaml')
            #os.chdir('/mnt/d/github/AFA_Backend/grad_project/api_user') 
            os.chdir(base)
            
            filename = path.split('/')
            filename = filename[len(filename) - 1]
            print(filename)
            os.remove(path2 + filename)



            #fh에 있는 이미지와 딥러닝을 통해 모델 생성
            #off -> obj
            path = './occupancy_networks/demo/generation/meshes/' + filename + '.off'
            #path = './result/01.jpg.off'
            fh = open(path, 'r')
            ch = off.load_off(fh)
            l = load.load_kwargs(ch)
            sc = trimesh.Scene(geometry=l)
            ob = obj.export_obj(sc)
            save_p = path
            path = './result/' + filename + '.obj'
            fh.close()
            fh = open(path, 'w')
            fh.write(ob)
            fh.close()
            os.remove(save_p)

            #obb적용

            #obj -> gltf
            fh = open(path, 'r')
            ch = obj.load_obj(fh)
            l = load.load_kwargs(ch)
            sc = trimesh.Scene(geometry=l)
            gl = gltf.export_gltf(sc, merge_buffers=True)
            ob = obj.export_obj(sc)
            # print(gl)
            print(gl.keys())
            dict_str = gl['model.gltf'].decode("UTF-8")
            mydata = ast.literal_eval(dict_str)
            fh.close()
            f = open('./result/model.gltf', 'w')
            json.dump(mydata, f)
            # print(repr(mydata), file=f)
            f.close()

            f = open('./result/gltf_buffer.bin', 'wb')
            # print(gl['gltf_buffer.bin'].decode())
            f.write(gl['gltf_buffer.bin'])
            f.close()
            os.remove(path)


            s3 = boto3.resource('s3',aws_access_key_id='aws id', aws_secret_access_key='secret key')

            bucket_name = 'grad-project-s3'
            #image = user_serializer.image
            data = open('./result/model.gltf', 'rb')
            print('data' + str(data))
            s3.Bucket(bucket_name).put_object(ACL = 'public-read',Key='model.gltf', Body=data)
            data = open('./result/gltf_buffer.bin', 'rb')
            s3.Bucket(bucket_name).put_object(ACL='public-read', Key='gltf_buffer.bin', Body=data)
            res = 'https://grad-project-s3.s3.ap-northeast-2.amazonaws.com/model.gltf'
            print(res)
            #return Response(res, status=status.HTTP_201_CREATED)  # client에게 JSON response 전달
            return Response(res, status=status.HTTP_201_CREATED)  # client에게 JSON response 전달

        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    GET /user
    GET /user/{user_id}
    """

    def get(self, request,  **kwargs):
        print(request)
        #print(request.data['image'])
        if kwargs.get('model') is None:
            user_queryset = User.objects.all() #모든 User의 정보를 불러온다.
            user_queryset_serializer = UserSerializer(user_queryset, many=True)
            return Response(user_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            key = kwargs.get('model')
            print(key)

            '''
            user_serializer = UserSerializer(User.objects.get(id=user_id)) #id에 해당하는 User의 정보를 불러온다
            print(user_serializer.data.keys())
            '''
            if key == 'model':
                path = './result/chair1.gltf'
                print(path)
                f = open(path, 'r')
                print(f)
                filename = path.split('/')
                filename = filename[len(filename) - 1]
                fl = open(path, 'rb')
                mime_type, _ = mimetypes.guess_type(path)
                print(mime_type)
                response = HttpResponse(fl, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % filename
                return response
            #return Response(response, status=status.HTTP_200_OK)

    """
    PUT /user/{user_id}
    """

    def put(self, request):
        return Response("test ok", status=200)

    """
    DELETE /user/{user_id}
    """

    def delete(self, request):
        return Response("test ok", status=200)
