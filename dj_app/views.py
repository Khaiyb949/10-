from django.shortcuts import render
from rest_framework.permissions import AllowAny
# views.py
from django.http import HttpResponseRedirect
from django.conf import settings
from rest_framework import viewsets
from dj_app.models import *
from .serializers import *

class TruyenViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Truyen.objects.all()
    serializer_class = TruyenSerializer

class TruyenViewSetbb(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Truyen.objects.all()
    serializer_class = TruyenSerializerbb

class EmojViewSet(viewsets.ModelViewSet): 
    permission_classes = [AllowAny]  
    queryset = Emoj.objects.all()
    serializer_class = EmojSerializer

class LikeCmtViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = LikeCmt.objects.all()
    serializer_class = LikeCmtSerializerb

class TheoDoiViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = TheoDoi.objects.all()
    serializer_class = TheoDoiSerializer

class DanhGiaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = DanhGia.objects.all()
    serializer_class = DanhGiaSerializer

class TaiKhoanViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TaiKhoan.objects.all()
    serializer_class = TaiKhoanSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'level_system': 'level'})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True, context={'level_system': 'level'})
        return Response(serializer.data)

class QuyenViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Quyen.objects.all()
    serializer_class = QuyenSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class TheLoaiViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TheLoai.objects.all()
    serializer_class = TheLoaiSerializer

class LuotXemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LuotXem.objects.all()
    serializer_class = LuotXemSerializer

class BinhLuanViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = BinhLuan.objects.all()
    serializer_class = BinhLuanSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializerbb

from rest_framework import generics
from .models import LuotXem
from .serializers import LuotXemSerializer

class LuotXemListAPIView(generics.ListAPIView):
    serializer_class = LuotXemSerializer

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen'] 
        return LuotXem.objects.filter(id_truyen=id_truyen)
    
class BinhLuanListAPIView(generics.ListAPIView):
    serializer_class = BinhLuanSerializer

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen'] 
        return BinhLuan.objects.filter(id_truyen=id_truyen)

class TheoDoiListAPIView(generics.ListAPIView):
    serializer_class = TheoDoiSerializer

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen'] 
        return TheoDoi.objects.filter(id_truyen=id_truyen)
    
class ChapterListAPIView(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen'] 
        return Chapter.objects.filter(id_truyen=id_truyen)

from rest_framework.response import Response 

class StoryListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = StorySerializerSTO

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen']
        id_chapter = self.kwargs['id_chapter']
        return Story.objects.filter(id_truyen_id=id_truyen, id_chapter_id=id_chapter)
    
    def list(self, request, *args, **kwargs):
        id_truyen = self.kwargs['id_truyen']
        id_chapter = self.kwargs['id_chapter']
        truyen = Truyen.objects.get(id=id_truyen)
        chapters = Chapter.objects.filter(id_truyen_id=id_truyen)
        stories = self.get_queryset()

        truyen_serializer = TruyenSerializerSTO(truyen, context={'id_chapter': id_chapter, 'id_truyen': id_truyen})
        chapter_serializer = ChapterSerializerSTO(chapters, many=True, context={'id_truyen': id_truyen})
        story_serializer = StorySerializerSTO(stories, many=True)

        return Response({
            'truyen': truyen_serializer.data,
            'chapters': chapter_serializer.data,
            'stories': story_serializer.data
        })


    
from django.http import JsonResponse
from django.views import View
from .models import LuotXem

class SumLuotXemView(View):
    def get(self, request, id_truyen):
        total_views = LuotXem.objects.filter(tinhtrang=True, id_truyen=id_truyen).count()
        return JsonResponse({'total_views': total_views})

class SumBinhLuanView(View):
    def get(self, request, id_truyen):
        total_views = BinhLuan.objects.filter(id_truyen=id_truyen).count()
        return JsonResponse({'total_views': total_views})

class SumTheoDoiView(View):
    def get(self, request, id_truyen):
        total_views = TheoDoi.objects.filter(tinhtrang=True, id_truyen=id_truyen).count()
        return JsonResponse({'total_views': total_views})
    

class SumLuotXemByChapView(View):
    def get(self, request, id_truyen, id_chap):
        total_views = LuotXem.objects.filter(tinhtrang=True, id_truyen=id_truyen, id_chap=id_chap).count()
        return JsonResponse({'total_views': total_views})
    
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([AllowAny])  # Không yêu cầu xác thực
def top3_chapter(request, id_truyen):
    latest_chapters = Chapter.objects.filter(id_truyen=id_truyen).order_by('-chap_ngay')[:3]
    serializer = ChapterSerializer(latest_chapters, many=True)
    return Response(serializer.data)

from datetime import datetime, timedelta
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LuotXem, Truyen, Chapter
from .serializers import TruyenSerializer, ChapterSerializer
from django.db.models import Q


class TopTruyenAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)


        top_truyens = Truyen.objects.annotate(
            total_luot_xem=Count('luot_xems', filter=Q(luot_xems__tinhtrang=True)),
            luot_xem_thang=Count('luot_xems', filter=Q(luot_xems__luotxem_ngay__gte=start_date, luot_xems__luotxem_ngay__lte=end_date))
        ).filter(total_luot_xem__gt=0).order_by('-luot_xem_thang')[:7]

        data = []
        for truyen in top_truyens:

            chap_moi_nhat = Chapter.objects.filter(id_truyen=truyen).order_by('-chap_ngay').first()


            luot_xem_truyen = LuotXem.objects.filter(id_truyen=truyen).count()


            serialized_truyen = TruyenSerializer(truyen).data
            serialized_chap = ChapterSerializer(chap_moi_nhat).data if chap_moi_nhat else None

            serialized_truyen['chap_moi_nhat'] = serialized_chap
            serialized_truyen['total_luot_xem'] = luot_xem_truyen

            data.append(serialized_truyen)

        return Response(data)


class TopTruyenTuanAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            top_truyens_tuan = Truyen.objects.annotate(
                total_luot_xem=Count('luot_xems', filter=Q(luot_xems__tinhtrang=True)),
            ).filter(
                luot_xems__luotxem_ngay__gte=start_of_week,
                luot_xems__luotxem_ngay__lte=end_of_week
            ).order_by('-total_luot_xem')[:7]

            if not top_truyens_tuan:
                return Response({'message': 'No data found for this week'}, status=status.HTTP_204_NO_CONTENT)

            data_tuan = []
            for truyen in top_truyens_tuan:
                chap_moi_nhat = Chapter.objects.filter(id_truyen=truyen).order_by('-chap_ngay').first()
                luot_xem_truyen = LuotXem.objects.filter(id_truyen=truyen).count()
                luot_xem_tuan = LuotXem.objects.filter(
                    id_truyen=truyen,
                    luotxem_ngay__gte=start_of_week,
                    luotxem_ngay__lte=end_of_week
                ).count()

                serialized_truyen = TruyenSerializer(truyen).data
                serialized_chap = ChapterSerializer(chap_moi_nhat).data if chap_moi_nhat else None

                serialized_truyen['chap_moi_nhat'] = serialized_chap
                serialized_truyen['total_luot_xem'] = luot_xem_truyen
                serialized_truyen['luot_xem_tuan'] = luot_xem_tuan

                data_tuan.append(serialized_truyen)

            return Response(data_tuan, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class TopTruyenNgayAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        today = datetime.now()
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)

        top_truyens_ngay = Truyen.objects.annotate(
            total_luot_xem=Count('luot_xems', filter=Q(luot_xems__tinhtrang=True)),
        ).filter(
            luot_xems__luotxem_ngay__gte=start_of_day,
            luot_xems__luotxem_ngay__lte=end_of_day
        ).order_by('-total_luot_xem')[:7]

        data_ngay = []
        for truyen in top_truyens_ngay:
            chap_moi_nhat = Chapter.objects.filter(id_truyen=truyen).order_by('-chap_ngay').first()
            luot_xem_truyen = LuotXem.objects.filter(id_truyen=truyen).count()
            luot_xem_ngay = LuotXem.objects.filter(
                id_truyen=truyen,
                luotxem_ngay__gte=start_of_day,
                luotxem_ngay__lte=end_of_day
            ).count()

            serialized_truyen = TruyenSerializer(truyen).data
            serialized_chap = ChapterSerializer(chap_moi_nhat).data if chap_moi_nhat else None

            serialized_truyen['chap_moi_nhat'] = serialized_chap
            serialized_truyen['total_luot_xem'] = luot_xem_truyen
            serialized_truyen['luot_xem_ngay'] = luot_xem_ngay

            data_ngay.append(serialized_truyen)

        return Response(data_ngay)
    
from django.db.models import Count, Avg
from django.http import JsonResponse
from .models import *
from datetime import date
from django.utils.timezone import now

def top_truyen_api(request, id_tk):
    today = now().date()

    # Fetch top truyens for today
    top_truyens_today = LuotXem.objects.filter(luotxem_ngay__date=today) \
                                        .values('id_truyen') \
                                        .annotate(total_luotxem=Count('id_truyen')) \
                                        .order_by('-total_luotxem')[:20]

    top_truyen_ids_today = [truyen['id_truyen'] for truyen in top_truyens_today]

    # Update or create TopTruyenDay entry
    TopTruyenDay.objects.update_or_create(
        date=today,
        defaults={'truyen_ids': top_truyen_ids_today}
    )

    # Get average ratings
    danh_gias = DanhGia.objects.filter(id_truyen__in=top_truyen_ids_today) \
                               .values('id_truyen') \
                               .annotate(avg_diem=Avg('diem'))

    avg_diem_dict = {danh_gia['id_truyen']: danh_gia['avg_diem'] for danh_gia in danh_gias}

    # Get old top truyens
    old_top_truyens = TopTruyenDay.objects.filter(date__lt=today) \
                                           .order_by('-date') \
                                           .first()

    old_truyen_ids = old_top_truyens.truyen_ids if old_top_truyens else []

    # Fetch all truyen details at once
    truyens = Truyen.objects.filter(pk__in=top_truyen_ids_today + old_truyen_ids)
    truyen_map = {truyen.pk: truyen for truyen in truyens}

    # Prepare the final list
    final_top_truyens = []

    for truyen_id in top_truyen_ids_today + old_truyen_ids:
        truyen = truyen_map.get(truyen_id)
        if not truyen:
            continue

        latest_chapter = Chapter.objects.filter(id_truyen=truyen_id) \
                                        .order_by('-chap_ngay') \
                                        .first()

        # Check if the latest chapter has been viewed by the user
        tinh_trang = False
        if latest_chapter:
            tinh_trang = LuotXem.objects.filter(id_tk=id_tk, id_chap=latest_chapter.id).exists()

        final_top_truyens.append({
            'id': truyen_id,
            'name': truyen.name,
            'tinh_trang': truyen.tinh_trang,
            'gioi_thieu': truyen.gioi_thieu,
            'tac_gia': truyen.tac_gia,
            'ten_khac': truyen.ten_khac,
            'img': truyen.img.url if truyen.img else None,
            'img_url': truyen.img_url if truyen.img_url else None,
            'avg_diem': avg_diem_dict.get(truyen_id, None),
            'latest_chapter': {
                'id': latest_chapter.id if latest_chapter else None,
                'name': latest_chapter.name if latest_chapter else None,
                'chap_ngay': latest_chapter.chap_ngay if latest_chapter else None,
                'tinh_trang': tinh_trang
            }
        })

    return JsonResponse(final_top_truyens, safe=False)


from rest_framework.pagination import PageNumberPagination

class TruyenPagination(PageNumberPagination):
    page_size = 36
    page_size_query_param = 'page_size'
    max_page_size = 10000  

from django.db.models import Max, Case, When, Value, BooleanField
from rest_framework.permissions import AllowAny

class TruyenListView(APIView):
    permission_classes = [AllowAny] 
    pagination_class = TruyenPagination

    def get(self, request, id_tk):
        truyens = Truyen.objects.annotate(
            newest_chapter_date=Max('chapters__chap_ngay'),
            has_chapters=Case(
                When(chapters__isnull=False, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('-has_chapters', '-newest_chapter_date')

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(truyens, request)
        
        serializer = TruyenSerializers(paginated_queryset, many=True, context={'id_tk': id_tk})
        return paginator.get_paginated_response(serializer.data)

    
from rest_framework import status
from django.db.models import Max

class LichSuXemTruyenView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id_tk):
        try:

            luot_xems = LuotXem.objects.filter(id_tk=id_tk, tinhtrang=True).order_by('-luotxem_ngay')
            

            seen_truyen = set()
            top_truyens = []
            for luot_xem in luot_xems:
                truyen_id = luot_xem.id_truyen_id
                if truyen_id not in seen_truyen:
                    seen_truyen.add(truyen_id)
                    top_truyens.append(truyen_id)
                if len(top_truyens) >= 3:
                    break

            result = []
            for truyen_id in top_truyens:
                truyen = Truyen.objects.get(id=truyen_id)
                latest_chapter = luot_xems.filter(id_truyen=truyen).aggregate(
                    max_chap_ngay=Max('id_chap__chap_ngay')
                )
                latest_chap = Chapter.objects.get(chap_ngay=latest_chapter['max_chap_ngay'])
                truyen_data = TruyenSerializer(truyen).data
                latest_chap_data = ChapterSerializer(latest_chap).data
                result.append({
                    'truyen': truyen_data,
                    'latest_chap': latest_chap_data,
                })
            
            return Response(result, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class TruyenDetailView(generics.RetrieveAPIView):
    queryset = Truyen.objects.all()
    serializer_class = TruyenSerializer

    
import random
class RandomTruyenView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        truyen_count = Truyen.objects.count()
        if truyen_count == 0:
            return Response({"error": "No truyens available"}, status=status.HTTP_404_NOT_FOUND)
        
        random_index = random.randint(0, truyen_count - 1)
        truyen = Truyen.objects.all()[random_index]
        serializer = TruyenSerializersss(truyen)
        return Response(serializer.data)
    
class ChapterListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = ChapterSerializer

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen']
        return Chapter.objects.filter(id_truyen=id_truyen)
    

class DanhGiaDetailView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, id_tk, id_truyen, format=None):
        danh_gias = DanhGia.objects.filter(id_tk=id_tk, id_truyen=id_truyen)
        if not danh_gias.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)  # Trả về phản hồi rỗng

        danh_gia = danh_gias.first()

        serializer = DanhGiaSerializer(danh_gia)
        return Response(serializer.data)

class TheoDoiListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = TheoDoiSerializer

    def get_queryset(self):
        id_tk = self.kwargs['id_tk']
        id_truyen = self.kwargs['id_truyen']
        return TheoDoi.objects.filter(id_tk=id_tk, id_truyen=id_truyen)
    
class BinhLuanPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100  


class BinhLuanListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = BinhLuanSerializerkkk
    pagination_class = BinhLuanPagination

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen']
        return BinhLuan.objects.filter(id_truyen=id_truyen, key='').order_by('-thoi_gian')

    def get_most_recent_chapter_view(self, id_tk, id_truyen):
        most_recent_view = LuotXem.objects.filter(id_tk=id_tk, id_truyen=id_truyen).order_by('-luotxem_ngay').first()
        return most_recent_view.id_chap if most_recent_view else None

    def get_like_count(self, comment_id):
        return LikeCmt.objects.filter(td_cmt_id=comment_id).count()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        id_tk = request.user.id
        id_truyen = self.kwargs['id_truyen']
        most_recent_chapter = self.get_most_recent_chapter_view(id_tk, id_truyen)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data

            for comment in serialized_data:
                comment_id = comment['id']
                count = BinhLuan.objects.filter(key=comment_id).count()
                like_count = self.get_like_count(comment_id)
                comment['count_with_specific_key'] = count
                comment['most_recent_chapter_name'] = most_recent_chapter.name if most_recent_chapter else "Unknown Chapter"
                comment['like_count'] = like_count

            response_data = {
                'comments': serialized_data,
                'total_comments': queryset.count(),
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
            }

            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        for comment in serialized_data:
            comment_id = comment['id']
            count = BinhLuan.objects.filter(key=comment_id).count()
            like_count = self.get_like_count(comment_id)
            comment['count_with_specific_key'] = count
            comment['most_recent_chapter_name'] = most_recent_chapter.name if most_recent_chapter else "Unknown Chapter"
            comment['like_count'] = like_count

        response_data = {
            'comments': serialized_data,
            'total_comments': queryset.count(),
            'count': len(serialized_data),
            'next': None,
            'previous': None,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class BinhLuanKeyListView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, id):
        key = str(id)
        binh_luans = BinhLuan.objects.filter(key=key)
        serializer = BinhLuanSerializerkkk(binh_luans, many=True)
        return Response(serializer.data)
    
class CheckLikeAPIView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, id_tk, id_truyen, format=None):
        try:
            # Retrieve the comment and account instances
            comment = BinhLuan.objects.get(id=id_truyen)
            account = TaiKhoan.objects.get(id_tk=id_tk)

            # Print statements to debug
            print(f"Comment ID: {comment.id}, Account ID: {account.id_tk}")
            
            # Check if a like entry exists for the given comment and account
            like_entry = LikeCmt.objects.filter(td_cmt=comment, id_tk=account).first()
            
            # Print statement to debug
            print(f"Like Entry: {like_entry}")

            if like_entry:
                serializer = LikeCmtSerializerb(like_entry)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'td_cmt': id_truyen, 'like': False}, status=status.HTTP_200_OK)

        except BinhLuan.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except TaiKhoan.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TruyenPagination(PageNumberPagination):
    page_size = 36
    page_size_query_param = 'page_size'
    max_page_size = 1000


class HotTruyenListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TruyenSerializers
    pagination_class = TruyenPagination

    def get_queryset(self):
        # Lọc các truyện có lượt xem lớn hơn hoặc bằng 130
        return Truyen.objects.filter(luot_xems__gte=130)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        seen_ids = set()  # Sử dụng một set để theo dõi các id đã thấy
        filtered_queryset = []

        # Tính toán view_growth_rate và views_this_week cho từng truyện
        for truyen in queryset:
            views_week_before_previous_week = self.get_views_week_before_previous_week(truyen)
            views_previous_week = self.get_views_previous_week(truyen)
            views_this_week = self.get_views_this_week(truyen)

            view_growth_rate = self.calculate_view_growth_rate(
                views_week_before_previous_week, views_previous_week
            )

            # Kiểm tra điều kiện và thêm truyện vào danh sách nếu thỏa mãn ít nhất một điều kiện
            if view_growth_rate >= 120 or views_this_week >= 10:
                # Thêm truyện vào danh sách nếu id chưa xuất hiện
                if truyen.id not in seen_ids:
                    truyen.view_growth_rate = view_growth_rate
                    truyen.views_this_week = views_this_week
                    filtered_queryset.append(truyen)
                    seen_ids.add(truyen.id)

        # Phân trang và trả về kết quả
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def calculate_view_growth_rate(self, views_week_before_previous_week, views_previous_week):
        if views_week_before_previous_week == 0:
            return 0 if views_previous_week == 0 else 100
        return ((views_previous_week - views_week_before_previous_week) / views_week_before_previous_week) * 100

    def get_views_previous_week(self, obj):
        start_date = datetime.strptime(self.get_previous_week_start(), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.get_previous_week_end(), '%Y-%m-%d').date()
        return LuotXem.objects.filter(id_truyen=obj.id, luotxem_ngay__date__range=[start_date, end_date]).count()

    def get_views_week_before_previous_week(self, obj):
        start_date = datetime.strptime(self.get_week_before_previous_week_start(), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.get_week_before_previous_week_end(), '%Y-%m-%d').date()
        return LuotXem.objects.filter(id_truyen=obj.id, luotxem_ngay__date__range=[start_date, end_date]).count()

    def get_views_this_week(self, obj):
        start_date = datetime.strptime(self.get_this_week_start(), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.get_this_week_end(), '%Y-%m-%d').date()
        return LuotXem.objects.filter(id_truyen=obj.id, luotxem_ngay__date__range=[start_date, end_date]).count()

    def get_previous_week_start(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        previous_week_start = start_of_week - timedelta(weeks=1)
        return previous_week_start.strftime('%Y-%m-%d')

    def get_previous_week_end(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        previous_week_end = start_of_week - timedelta(days=1)
        return previous_week_end.strftime('%Y-%m-%d')

    def get_week_before_previous_week_start(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_before_previous_week_start = start_of_week - timedelta(weeks=2)
        return week_before_previous_week_start.strftime('%Y-%m-%d')

    def get_week_before_previous_week_end(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_before_previous_week_end = start_of_week - timedelta(weeks=1) - timedelta(days=1)
        return week_before_previous_week_end.strftime('%Y-%m-%d')

    def get_this_week_start(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        return start_of_week.strftime('%Y-%m-%d')

    def get_this_week_end(self):
        today = datetime.now().date()
        end_of_week = today + timedelta(days=(6 - today.weekday()))
        return end_of_week.strftime('%Y-%m-%d')
    

class FollowedTruyenListPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

class FollowedTruyenListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TruyenSerializers
    pagination_class = FollowedTruyenListPagination

    def get_queryset(self):
        id_tk = self.kwargs['id_tk']
        return Truyen.objects.filter(theo_dois__id_tk=id_tk, theo_dois__tinhtrang=True).annotate(
            latest_chap_ngay=Max('chapters__chap_ngay')
        ).order_by('-latest_chap_ngay').distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"id_tk": self.kwargs['id_tk']})
        return context
    
class UnviewedTruyenListView(generics.ListAPIView):
    serializer_class = TruyenSerializers
    pagination_class = FollowedTruyenListPagination

    def get_queryset(self):
        id_tk = self.kwargs['id_tk']
        viewed_truyen_ids = LuotXem.objects.filter(id_tk=id_tk).values_list('id_truyen_id', flat=True)
        return Truyen.objects.filter(theo_dois__id_tk=id_tk, theo_dois__tinhtrang=True).exclude(id__in=viewed_truyen_ids).distinct()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"id_tk": self.kwargs['id_tk']})
        return context


class CustomPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

class ViewHistoryAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TruyenSerializers
    pagination_class = CustomPagination  

    def get_queryset(self):
        id_tk = self.kwargs.get('id_tk')
        if id_tk:

            return Truyen.objects.filter(luot_xems__id_tk=id_tk).distinct()
        return Truyen.objects.none()

    def get(self, request, *args, **kwargs):
        id_tk = self.kwargs.get('id_tk')
        if not id_tk:
            return Response({'error': 'id_tk parameter is required'}, status=400)


        response = super().get(request, *args, **kwargs)
        paginated_data = response.data


        truyen_ids = [item['id'] for item in paginated_data['results']]

        latest_chapters = (LuotXem.objects.filter(id_tk=id_tk, id_truyen__in=truyen_ids)
                                           .values('id_truyen')
                                           .annotate(latest_chapter_id=Max('id_chap'))
                                           .order_by())

        latest_chapter_mapping = {item['id_truyen']: item['latest_chapter_id'] for item in latest_chapters}

        for item in paginated_data['results']:
            truyen_id = item['id']
            latest_chapter_id = latest_chapter_mapping.get(truyen_id)
            if latest_chapter_id:
                latest_chapter = Chapter.objects.filter(id=latest_chapter_id).first()
                if latest_chapter:
                    item['latest_chapter'] = {
                        'id': latest_chapter.id,
                        'name': latest_chapter.name,
                        'chap_ngay': latest_chapter.chap_ngay,
                        'tinh_trang': LuotXem.objects.filter(id_tk=id_tk, id_chap=latest_chapter.id, tinhtrang=True).exists()
                    }
                else:
                    item['latest_chapter'] = {}
            else:
                item['latest_chapter'] = {}

        paginated_data['id_tk'] = id_tk
        return Response(paginated_data)
    
class ViewHistoryByIPAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TruyenSerializers
    pagination_class = CustomPagination  

    def get_queryset(self):
        ip = self.kwargs.get('ip')
        if ip:
            return Truyen.objects.filter(luot_xems__ip=ip).distinct()
        return Truyen.objects.none()

    def get(self, request, *args, **kwargs):
        ip = self.kwargs.get('ip')
        if not ip:
            return Response({'error': 'IP parameter is required'}, status=400)

        response = super().get(request, *args, **kwargs)
        paginated_data = response.data

        truyen_ids = [item['id'] for item in paginated_data['results']]

        latest_chapters = (LuotXem.objects.filter(ip=ip, id_truyen__in=truyen_ids)
                                           .values('id_truyen')
                                           .annotate(latest_chapter_id=Max('id_chap'))
                                           .order_by())

        latest_chapter_mapping = {item['id_truyen']: item['latest_chapter_id'] for item in latest_chapters}

        for item in paginated_data['results']:
            truyen_id = item['id']
            latest_chapter_id = latest_chapter_mapping.get(truyen_id)
            if latest_chapter_id:
                latest_chapter = Chapter.objects.filter(id=latest_chapter_id).first()
                if latest_chapter:
                    item['latest_chapter'] = {
                        'id': latest_chapter.id,
                        'name': latest_chapter.name,
                        'chap_ngay': latest_chapter.chap_ngay,
                        'tinh_trang': LuotXem.objects.filter(ip=ip, id_chap=latest_chapter.id, tinhtrang=True).exists()
                    }
                else:
                    item['latest_chapter'] = {}
            else:
                item['latest_chapter'] = {}

        paginated_data['ip'] = ip
        return Response(paginated_data)
    
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters

class TruyenFilter(filters.FilterSet):
    theloai_id = filters.NumberFilter(field_name='nametl__id', lookup_expr='exact', required=False)

    class Meta:
        model = Truyen
        fields = ['theloai_id']

    def filter_queryset(self, queryset):
        theloai_id = self.request.query_params.get('theloai_id', None)

        if theloai_id == '0':
            return queryset

        return super().filter_queryset(queryset)

class TruyenListViews(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = TruyenSerializer
    queryset = Truyen.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = TruyenFilter
    search_fields = ['name']

@api_view(['POST'])
def create_taikhoan(request):
    serializer = TaiKhoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.authtoken.models import Token

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response('Email và mật khẩu không được bỏ trống', status=status.HTTP_400_BAD_REQUEST)

    try:
        user = TaiKhoan.objects.get(email=email)
    except TaiKhoan.DoesNotExist:
        return Response('Người dùng không tồn tại', status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, user.password):
        return Response('Mật khẩu không đúng', status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response('Tài khoản này đã bị vô hiệu hóa', status=status.HTTP_400_BAD_REQUEST)
    # if user.is_superuser:
    #     pass
    # elif user.id_quyen not in [1,2]:
    #     return Response('Tài khoản không có quyền đăng nhập', status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)


class AuthCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = TaiKhoanSerializerkkk(user)
        return Response({'detail': 'Access token is valid', 'user': serializer.data}, status=status.HTTP_200_OK)

    
class TopTruyenViewsss(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TruyenSerializer

    def get_queryset(self):
        id_tk = self.kwargs.get('id_tk')
        if id_tk:
            theo_dois = TheoDoi.objects.filter(id_tk=id_tk, tinhtrang=True).values_list('id_truyen', flat=True)
            return Truyen.objects.filter(id__in=theo_dois).distinct()[:5]
        return Truyen.objects.none()  # Return an empty queryset if id_tk is not provided

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from uuid import UUID

class Top5BinhLuanView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BinhLuanSerializersss
    
    def get_queryset(self):
        id_tk = self.kwargs['id_tk']  # Nhận id_tk từ URL
        return BinhLuan.objects.filter(id_tk=id_tk).order_by('-thoi_gian')[:5]  
    
@api_view(['GET'])
def get_id_tk_by_email(request, email):
    try:
        tai_khoan = TaiKhoan.objects.get(email=email)
        serializer = TaiKhoanSerializer(tai_khoan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except TaiKhoan.DoesNotExist:
        return Response({'error': 'Tài khoản không tồn tại'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def id_id_tk(request, *args, **kwargs):
    try:
        users = TaiKhoan.objects.all()
        for user in users:
            user.id = user.id_tk
            user.save()
        return Response({"msg":"DOne"}, status=status.HTTP_200_OK)
    except TaiKhoan.DoesNotExist:
        return Response({'error': 'Tài khoản không tồn tại'}, status=status.HTTP_404_NOT_FOUND)
    

from django.db.models import Sum, F, Case, When, IntegerField, Count
from django.db.models.functions import Coalesce, ExtractMonth, ExtractWeek, ExtractDay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Truyen
from .serializers import TruyenSerializers

class TruyenPaginationx(PageNumberPagination):
    page_size = 36  
    page_size_query_param = 'page_size'
    max_page_size = 10000

@api_view(['GET'])
@permission_classes([AllowAny])
def get_truyen_by_theloai(request, id_theloai):
    tinh_trang = request.query_params.get('tinh_trang', None)
    xep = request.query_params.get('xep', None)

    if id_theloai and id_theloai != '0':
        queryset = Truyen.objects.filter(nametl__id=id_theloai)
    else:
        queryset = Truyen.objects.all()


    # Lọc theo tinh_trang
    if tinh_trang is not None:
        if tinh_trang == '1':
            queryset = queryset.filter(tinh_trang='Hoàn thành')
        elif tinh_trang == '2':
            queryset = queryset.filter(tinh_trang='Đang tiến hành')

    print(f"Truyen list after status filter: {queryset.count()} items")

    # Sắp xếp theo tham số xep
    if xep == '1':
        queryset = queryset.annotate(
            latest_chap_date=Coalesce(Max('chapters__chap_ngay'), datetime.min)
        ).order_by('-latest_chap_date')
    elif xep == '2':
        queryset = queryset.order_by('-id')
    elif xep == '3':
        queryset = queryset.annotate(
            total_views=Coalesce(Sum('luot_xems__id'), 0)
        ).order_by('-total_views')
    elif xep == '4':
        queryset = queryset.annotate(
            monthly_views=Sum(
                Case(
                    When(
                        luot_xems__luotxem_ngay__month=ExtractMonth(F('luot_xems__luotxem_ngay')),
                        then=1
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('-monthly_views')
    elif xep == '5':
        queryset = queryset.annotate(
            weekly_views=Sum(
                Case(
                    When(
                        luot_xems__luotxem_ngay__week=ExtractWeek(F('luot_xems__luotxem_ngay')),
                        then=1
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('-weekly_views')
    elif xep == '6':
        queryset = queryset.annotate(
            daily_views=Sum(
                Case(
                    When(
                        luot_xems__luotxem_ngay__day=ExtractDay(F('luot_xems__luotxem_ngay')),
                        then=1
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('-daily_views')
    elif xep == '7':
        queryset = queryset.annotate(
            total_followers=Coalesce(Count('theo_dois'), 0)
        ).order_by('-total_followers')
    elif xep == '8':
        queryset = queryset.annotate(
            total_comments=Coalesce(Count('binh_luans'), 0)
        ).order_by('-total_comments')
    elif xep == '9':
        queryset = queryset.annotate(
            total_chapters=Coalesce(Count('chapters'), 0)
        ).order_by('-total_chapters')

    print(f"Truyen list after sorting: {queryset.count()} items")

    # Phân trang
    paginator = TruyenPaginationx()
    paginated_truyen = paginator.paginate_queryset(queryset, request)
    
    serializer = TruyenSerializers(paginated_truyen, many=True)
    return paginator.get_paginated_response(serializer.data)



class BinhLuanListViews(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = BinhLuanSerializerkkk
    pagination_class = BinhLuanPagination

    def get_queryset(self):
        id_truyen = self.kwargs['id_truyen']
        id_chap = self.kwargs.get('id_chap', None)
        queryset = BinhLuan.objects.filter(id_truyen=id_truyen, key='').order_by('-thoi_gian')
        if id_chap is not None:
            queryset = queryset.filter(id_chap=id_chap)
        return queryset

    def get_most_recent_chapter_view(self, id_tk, id_truyen):
        most_recent_view = LuotXem.objects.filter(id_tk=id_tk, id_truyen=id_truyen).order_by('-luotxem_ngay').first()
        return most_recent_view.id_chap if most_recent_view else None

    def get_like_count(self, comment_id):
        return LikeCmt.objects.filter(td_cmt_id=comment_id).count()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        id_tk = request.user.id
        id_truyen = self.kwargs['id_truyen']
        most_recent_chapter = self.get_most_recent_chapter_view(id_tk, id_truyen)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data

            for comment in serialized_data:
                comment_id = comment['id']
                count = BinhLuan.objects.filter(key=comment_id).count()
                like_count = self.get_like_count(comment_id)
                comment['count_with_specific_key'] = count
                comment['most_recent_chapter_name'] = most_recent_chapter.name if most_recent_chapter else "Unknown Chapter"
                comment['like_count'] = like_count

            response_data = {
                'comments': serialized_data,
                'total_comments': queryset.count(),
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
            }

            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        for comment in serialized_data:
            comment_id = comment['id']
            count = BinhLuan.objects.filter(key=comment_id).count()
            like_count = self.get_like_count(comment_id)
            comment['count_with_specific_key'] = count
            comment['most_recent_chapter_name'] = most_recent_chapter.name if most_recent_chapter else "Unknown Chapter"
            comment['like_count'] = like_count

        response_data = {
            'comments': serialized_data,
            'total_comments': queryset.count(),
            'count': len(serialized_data),
            'next': None,
            'previous': None,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class BinhLuanKeyAndChapterListView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, id, id_chap):
        key = str(id)
        binh_luans = BinhLuan.objects.filter(key=key, id_chap=id_chap)
        serializer = BinhLuanSerializerkkk(binh_luans, many=True)
        return Response(serializer.data)
    
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import string

@csrf_exempt
def update_image(request, id_tk):
    if request.method == 'PATCH':
        user = get_object_or_404(TaiKhoan, id_tk=id_tk)
        if 'img' in request.FILES:
            user.img = request.FILES['img']
            user.save()
            return JsonResponse({'message': 'Hình ảnh đã được cập nhật'})
        return JsonResponse({'error': 'Không có tệp hình ảnh trong yêu cầu'}, status=400)
    
    return JsonResponse({'error': 'Phương thức không hợp lệ'}, status=400)

from django.core.mail import send_mail

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

@api_view(['POST'])
def send_reset_code(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        if not TaiKhoan.objects.filter(email=email).exists():
            return Response({'error': 'No account with this email'}, status=status.HTTP_400_BAD_REQUEST)

        reset_code = generate_code()

        send_mail(
            'Password Reset Code',
            f'Your password reset code is {reset_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Reset code sent'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_code(request):
    serializer = VerifyCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        return Response({'message': 'Code verified'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['newPassword']
        
        # Validate email and reset password
        try:
            user = TaiKhoan.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except TaiKhoan.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    ermission_classes = [IsAuthenticated] 

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()

@csrf_exempt
def check_old_password(request, id_tk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            old_password = data.get('password')
            user = User.objects.get(id_tk=id_tk)
            if user.check_password(old_password):
                return JsonResponse({'valid': True})
            return JsonResponse({'valid': False})
        except User.DoesNotExist:
            return JsonResponse({'valid': False})
        except json.JSONDecodeError:
            return JsonResponse({'valid': False, 'error': 'Invalid JSON'})
    
@csrf_exempt
def change_password(request, id_tk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')
            user = User.objects.get(id_tk=id_tk)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        except User.DoesNotExist:
            return JsonResponse({'success': False})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        

class TopBinhLuanAPIView(APIView):
    def get(self, request, id_tk):
        lay_tat_ca = request.query_params.get('all', 'false').lower() == 'true'
        
        if lay_tat_ca:
            binh_luans = BinhLuan.objects.filter(nhac=id_tk, da_doc=False).order_by('-thoi_gian')
        else:
            binh_luans = BinhLuan.objects.filter(nhac=id_tk, da_doc=False).order_by('-thoi_gian')[:10]
        
        serializer = BinhLuanSerializerkkk(binh_luans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TatCaBinhLuanAPIView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, id_tk):
        lay_tat_ca = request.query_params.get('all', 'false').lower() == 'true'
        
        if lay_tat_ca:
            binh_luans = BinhLuan.objects.filter(nhac=id_tk).order_by('-thoi_gian')
        else:
            binh_luans = BinhLuan.objects.filter(nhac=id_tk).order_by('-thoi_gian')[:10]
        
        serializer = BinhLuanSerializerkkk(binh_luans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StoryListByChapter(generics.ListAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        chapter_id = self.kwargs['id_chapter']
        return Story.objects.filter(id_chapter=chapter_id)
    
from django.views.decorators.http import require_GET
@require_GET
@permission_classes([AllowAny])
def check_chapter_exists(request):
    name = request.GET.get('name', '').strip()
    id_truyen = request.GET.get('id_truyen', '').strip()
    
    if not name or not id_truyen:
        return JsonResponse({'error': 'Both name and id_truyen are required'}, status=400)
    
    try:
        id_truyen = int(id_truyen)
    except ValueError:
        return JsonResponse({'error': 'Invalid id_truyen format'}, status=400)
    
    exists = Chapter.objects.filter(name=name, id_truyen=id_truyen).exists()
    return JsonResponse({'exists': exists})




class DangKyKhuonMatView(APIView):
    def patch(self, request):
        id_user = request.query_params.get('id_user')  # Lấy id_user từ query parameters
        face_encoding = request.data.get('face_encoding')  # Lấy face_encoding từ request

        # Kiểm tra id_user có hợp lệ không
        if not id_user:
            return Response({"error": "Thiếu id_user trong request."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra face_encoding
        if face_encoding is None:
            return Response({"error": "Thiếu face_encoding trong request."}, status=status.HTTP_400_BAD_REQUEST)

        # Tìm tài khoản theo id_user
        try:
            tai_khoan = TaiKhoan.objects.get(id_tk=id_user)
        except TaiKhoan.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        # Chuyển Float32Array thành list rồi lưu vào JSONField
        try:
            encoding_list = list(face_encoding)  # Chuyển Float32Array sang list
            tai_khoan.face_encoding = encoding_list
        except TypeError:
            return Response({"error": "face_encoding không đúng định dạng Float32Array."}, status=status.HTTP_400_BAD_REQUEST)

        tai_khoan.save()
        return Response({"message": "Cập nhật thành công!"}, status=status.HTTP_200_OK)
    
class KiemTraKhuonMatView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        id = request.data.get('id') 
        
        try:
            users = TaiKhoan.objects.get(id=id)
        except TaiKhoan.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
                
        if not users.is_superuser:
            return Response({'error': 'Tài khoản không có quyền đăng nhập'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo token cho người dùng
        refresh = RefreshToken.for_user(users)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    
class face_encodingListView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    serializer_class = face_encodingSerializer

    def get_queryset(self):
        return TaiKhoan.objects.filter(is_superuser=True)
    
from django.utils import timezone

class LuotXemStatisticsView(APIView):
    def get(self, request):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        start_of_week = today - timedelta(days=today.weekday())
        last_week = start_of_week - timedelta(weeks=1)
        start_of_month = today.replace(day=1)
        last_month = (start_of_month - timedelta(days=1)).replace(day=1)

        # Daily views
        today_views = LuotXem.objects.filter(luotxem_ngay__date=today).aggregate(total=Sum('so_luot_xem'))['total'] or 0
        yesterday_views = LuotXem.objects.filter(luotxem_ngay__date=yesterday).aggregate(total=Sum('so_luot_xem'))['total'] or 0
        daily_percentage_change = ((today_views - yesterday_views) / yesterday_views * 100) if yesterday_views else 0

        # Weekly views
        current_week_views = LuotXem.objects.filter(luotxem_ngay__date__gte=start_of_week).aggregate(total=Sum('so_luot_xem'))['total'] or 0
        last_week_views = LuotXem.objects.filter(luotxem_ngay__date__gte=last_week, luotxem_ngay__date__lt=start_of_week).aggregate(total=Sum('so_luot_xem'))['total'] or 0
        weekly_percentage_change = ((current_week_views - last_week_views) / last_week_views * 100) if last_week_views else 0

        # Monthly views
        current_month_views = LuotXem.objects.filter(luotxem_ngay__date__gte=start_of_month).aggregate(total=Sum('so_luot_xem'))['total'] or 0
        last_month_views = LuotXem.objects.filter(luotxem_ngay__date__gte=last_month, luotxem_ngay__date__lt=start_of_month).aggregate(total=Sum('so_luot_xem'))['total'] or 0
        monthly_percentage_change = ((current_month_views - last_month_views) / last_month_views * 100) if last_month_views else 0

        data = {
            'daily': {
                'total_views': today_views,
                'percentage_change': daily_percentage_change,
            },
            'weekly': {
                'total_views': current_week_views,
                'percentage_change': weekly_percentage_change,
            },
            'monthly': {
                'total_views': current_month_views,
                'percentage_change': monthly_percentage_change,
            },
        }
        
        return Response(data)
    
from django.shortcuts import render
from django.views.generic.base import TemplateView



class AngularAdminView(TemplateView):
    template_name = "index_admin.html"


class AngularViewClient(TemplateView):
    template_name = "index_layzing_page.html"

class CustomRedirectView(View):
    def get(self, request, path):
        static_file_path = os.path.join(settings.STATIC_ROOT, "admin/assets", path)

        if os.path.isfile(static_file_path):
            return HttpResponseRedirect(settings.STATIC_URL + "admin/assets/" + path)
        else:
            return HttpResponseRedirect(settings.STATIC_URL + "layzing_page/assets/" + path)