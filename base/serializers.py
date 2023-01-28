from rest_framework import  serializers
from django.contrib.auth.models import User
from .models import AddExpenseModel, CategoryLookup

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],     password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
        return user
    
# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class AddExpenseModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddExpenseModel
        fields = '__all__'
        
class CategoryLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryLookup
        fields = '__all__'