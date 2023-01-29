from rest_framework import generics, permissions, mixins, viewsets,status, views
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, AddExpenseModelSerializer, CategoryLookupSerializer
from .models import AddExpenseModel, CategoryLookup, User
from datetime import date
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
        
class UserDetails(views.APIView):
    def get(self,request):
        user_details = User.objects.get(id=request.user.id)
        
        return Response({
            "user": UserSerializer(user_details).data,
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
        
        if data['category'] is None:
            data['category'] = 'extra'
        
        category = data['category']
        data['user'] = request.user.id
        
        if "expense_added" not in data:
            data['expense_added'] = date.today()
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def list(self,request):
        expenses = AddExpenseModel.objects.filter(user=request.user.id)
        
        return Response(AddExpenseModelSerializer(expenses, many=True).data)
    
class CategoryLookupView(viewsets.ModelViewSet):
    queryset = CategoryLookup.objects.all()
    serializer_class = CategoryLookupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class VoiceExpenseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        data = request.data
        output_json = makeJson(data['text'])
        addexpense_data = requests.post(url = 'https://pocket-saver.onrender.com/users/addexpense/',
                                  headers={'Authorization': 'Bearer ' + request.headers.get('Authorization').split()[1],'Content-Type': 'application/json'},
                                  json = output_json).json()

        return Response(addexpense_data, status= status.HTTP_201_CREATED)
    
import json  
from collections import defaultdict
  
class PredictExpense(views.APIView):
    
    def get(self, request):
        # df = pd.read_csv('finaldata2.csv')
        # return Response(future_expense(df,7), status= status.HTTP_200_OK)
        db = AddExpenseModel.objects.filter(user=request.user)
        expenses = AddExpenseModelSerializer(db, many=True).data
        
        expenses_by_date = defaultdict(int)

        # Iterate through the expenses and add the amounts to the corresponding date
        for expense in expenses:
            expenses_by_date[expense["expense_added"]] += expense["price"]
        # Create a list to store the JSON objects
        expenses_json = []

        # Iterate through the expenses_by_date dictionary and create JSON objects
        for date, total in expenses_by_date.items():
            expense_json = {"expense_added": date, "price": total}
            expenses_json.append(expense_json)

        # Serialize the list of JSON objects to a JSON string

        json_string = json.dumps(expenses_json, indent=4)
                        
        df = pd.read_csv('finaldata2.csv')
        future_expense(df,7)

        return Response(future_expense(df,7), status= status.HTTP_200_OK)