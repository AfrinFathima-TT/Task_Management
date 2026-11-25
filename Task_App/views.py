from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from Task_App.serializer import UserSerializer,TaskSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Task_App.models import TaskDb
from rest_framework import serializers


# Create your views here.
class RegistrationView(APIView):
    def post(self,request):
        serializer_instance = UserSerializer(data = request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TaskListCreateView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        task = TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(task,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        serializer_instance = TaskSerializer(data = request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TaskRetriveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        task_object=get_object_or_404(TaskDb,id=pk)
        if task_object.user!=request.user:
            raise serializers.ValidationError("Access Denied")
        else:
            serializers_instance=TaskSerializer(task_object)
            return Response(data=serializers_instance.data)

    def put(self,request,pk):
        task_object=get_object_or_404(TaskDb,id=pk)
        if task_object.user!=request.user:
            raise serializers.ValidationError("Access Denied")
        else:
            serializers_instance=TaskSerializer(data=request.data,instance=task_object)
            if serializers_instance.is_valid():
                serializers_instance.save
                return Response(data=serializers_instance.data)
            else:
                return Response(data=serializers_instance.errors)

    def delete(self,request,pk):
        task_object=get_object_or_404(TaskDb,id=pk)
        if task_object.user!=request.user:
            raise serializers.ValidationError("Access Denied")
        else:
            task_object.delete()
            return Response({
                "Message":"Task deleted..!"
            })

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.data.delete
        return Response({
            "Message":"Logout success...!"
        })




