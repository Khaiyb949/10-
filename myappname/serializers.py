from rest_framework import serializers
from .models import Image
from dj_app.models import Truyen

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class TruyenSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Truyen
        fields = ['id', 'title', 'img', 'img_url']

    def get_img_url(self, obj):
        if obj.img:
            # Trả về đường dẫn đầy đủ của ảnh
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.img)
        return None
