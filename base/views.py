from rest_framework import generics, permissions, mixins, viewsets,status, views
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, AddExpenseModelSerializer, CategoryLookupSerializer
from .models import AddExpenseModel, CategoryLookup
from datetime import datetime
from .utils import makeJson
import requests

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
        
class AddExpenseView(viewsets.ModelViewSet):
    queryset = AddExpenseModel.objects.all()
    serializer_class = AddExpenseModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data

        if "category" not in data:
            data['category'] = None
            
        if data['category'] is not None and not CategoryLookup.objects.filter(name=data['name']).exists():
            CategoryLookup.objects.create(category=data['category'], name=data['name'])
            
        if data['category'] is None and CategoryLookup.objects.filter(name=data['name']).exists():
            data['category'] = CategoryLookup.objects.get(name=data['name']).category
            
        category = data['category']
        data['user'] = request.user.id
        data['expense_added'] = datetime.now()
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class CategoryLookupView(viewsets.ModelViewSet):
    queryset = CategoryLookup.objects.all()
    serializer_class = CategoryLookupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class VoiceExpenseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        data = request.data
        output_json = makeJson(data['text'])
        addexpense_data = requests.post(url = 'http://127.0.0.1:8000/users/addexpense/',
                                  headers={'Authorization': 'Bearer ' + request.headers.get('Authorization').split()[1],'Content-Type': 'application/json'},
                                  json = output_json).json()

        return Response(addexpense_data, status= status.HTTP_201_CREATED)