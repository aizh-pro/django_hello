import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, Http404
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView

from api_v1.serializers import ArticleSerializer
from webapp.models import Article
from rest_framework.response import Response


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response

# class ArticleCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             article = serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)
#
#
# class ArticleListView(APIView):
#     def get(self, request, *args, **kwargs):
#         objects = Article.objects.all()
#         serializer = ArticleSerializer(objects, many=True)
#         return Response(serializer.data)


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        slr = ArticleSerializer(article, many=False)
        return JsonResponse(slr.data, safe=False)


class ArticleUpdateView(View):
    def put(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs['pk'])
        data = json.loads(request.body)
        slr = ArticleSerializer(data=data, instance=article)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleDeleteView(View):
    def delete(self,request, *args, **kwargs):
        print('Номер статьи')
        print(kwargs['pk'])
        article = Article.objects.get(pk=kwargs['pk'])
        article.delete()
        return JsonResponse(article.pk)


class ArticleFullView(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


