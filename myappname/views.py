from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dj_app.models import Truyen 
from rest_framework import status, viewsets 
from .models import Image
from .serializers import ImageSerializer
from .serializers import TruyenSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        truyen_id = request.data.get('truyen_id')

        try:
            truyen = get_object_or_404(Truyen, pk=truyen_id)
            truyen.img = '/truyen_images/' + image_file.name  # Lưu đường dẫn đầy đủ của ảnh
            truyen.save()

            # Serialize lại truyen để trả về response
            serializer = TruyenSerializer(truyen, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Truyen.DoesNotExist:
            return Response({'error': 'Không tìm thấy Truyen'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({'error': 'Yêu cầu không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)