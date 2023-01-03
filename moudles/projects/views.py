from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Project
from rest_framework import viewsets
from .serializers import ProjectSerializer

# class ProjectViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows projects to be viewed or edited.
#     """
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProjectList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # here

    # 定义 GET 请求的方法，内部实现相同 @api_view
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 定义 POST 请求的方法
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # here

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ## to permit delete action or not
    # def delete(self, request, pk):
    #     project = self.get_object(pk)
    #     project.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
