# serializers.py

from rest_framework import serializers
from .models import *

class TruyenSerializerbb(serializers.ModelSerializer):
    class Meta:
        model = Truyen
        fields = '__all__'
class TheLoaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheLoai
        fields = '__all__'

class EmojSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoj
        fields = '__all__'


class TruyenSerializer(serializers.ModelSerializer):
    nametl = TheLoaiSerializer(many=True, read_only=True)
    newest_chapter = serializers.SerializerMethodField()
    oldest_chapter = serializers.SerializerMethodField()
    latest_viewed_chapter = serializers.SerializerMethodField()
    diem_trung_binh = serializers.SerializerMethodField()
    tong_so_danh_gia = serializers.SerializerMethodField()
    tong_so_theo_doi = serializers.SerializerMethodField()

    class Meta:
        model = Truyen
        fields = '__all__'

    def get_diem_trung_binh(self, obj):
        danh_gias = DanhGia.objects.filter(id_truyen=obj)
        if danh_gias.count() == 0:
            return 0  
        return danh_gias.aggregate(Avg('diem'))['diem__avg']

    def get_tong_so_danh_gia(self, obj):
        return DanhGia.objects.filter(id_truyen=obj).count()

    def get_newest_chapter(self, obj):
        newest_chapter = obj.chapters.order_by('-chap_ngay').first()
        return ChapterSerializer(newest_chapter).data if newest_chapter else None

    def get_oldest_chapter(self, obj):
        oldest_chapter = obj.chapters.order_by('chap_ngay').first()
        return ChapterSerializer(oldest_chapter).data if oldest_chapter else None

    def get_latest_viewed_chapter(self, obj):
        latest_viewed_chapter = obj.chapters.filter(luot_xems__isnull=False).order_by('-luot_xems__luotxem_ngay').first()
        return ChapterSerializer(latest_viewed_chapter).data if latest_viewed_chapter else None

    def get_tong_so_theo_doi(self, obj):
        return TheoDoi.objects.filter(id_truyen=obj, tinhtrang=True).count()


class TheoDoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheoDoi
        fields = '__all__'

class DanhGiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGia
        fields = '__all__'

class TaiKhoanSerializer(serializers.ModelSerializer):
    total_views = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    display_level = serializers.SerializerMethodField()
    next_level = serializers.SerializerMethodField()
    percentage_to_next_level = serializers.SerializerMethodField()
    level_system = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = TaiKhoan
        fields = '__all__'

    def get_total_views(self, obj):
        total_views = LuotXem.objects.filter(id_tk=obj.id_tk).aggregate(total_views=Sum('so_luot_xem'))
        exp = (total_views['total_views'] or 0) * 100
        return exp

    def get_level(self, obj):
        total_views = self.get_total_views(obj)
        points_per_level = 1000
        if total_views > 0:
            level = math.log2(total_views / points_per_level) + 1
            return f"Level {int(level)}"
        return "Level 0"

    def get_display_level(self, obj):
        level_system = obj.level_system or 'level'
        total_views = self.get_total_views(obj)
        points_per_level = 1000

        if level_system == 'level':
            if total_views > 0:
                level = math.log2(total_views / points_per_level) + 1
                return f"Level {int(level)}"
            return "Level 0"

        elif level_system == 'tien_dao':
            levels = [
                "Luyện Khí", "Trúc Cơ", "Kim Đan", "Nguyên Anh", "Hóa Thần", 
                "Luyện Hư", "Hợp Thể", "Độ Kiếp", "Chân Tiên", "Kim Tiên", 
                "Thái Ất Kim Tiên", "Đại La Kim Tiên", "Hỗn Nguyên Kim Tiên", "Thiên Đạo"
            ]
            if total_views > 0:
                index = int(math.log2(total_views / points_per_level))
            else:
                index = 0
            return levels[min(index, len(levels) - 1)]

        elif level_system == 'vo_dao':
            if total_views <= 1000:
                levels = ["Hậu Thiên Nhất Trọng", "Hậu Thiên Nhị Trọng", "Hậu Thiên Tam Trọng", "Hậu Thiên Tứ Trọng", "Hậu Thiên Ngũ Trọng"]
                index = int(total_views / 200) 
                return levels[min(index, len(levels) - 1)]
            elif total_views <= 2000:
                levels = ["Hậu Thiên Lục Trọng", "Hậu Thiên Thất Trọng", "Hậu Thiên Bát Trọng", "Hậu Thiên Cửu Trọng"]
                index = int((total_views - 1000) / 250)  
                return levels[min(index, len(levels) - 1)]
            elif total_views < 8000:
                return "Tiên Thiên Nhất Trọng"
            elif total_views < 17000:
                return "Tiên Thiên Nhị Trọng"
            elif total_views < 32000:
                return "Tiên Thiên Tam Trọng"
            elif total_views < 64000:
                return "Tiên Thiên Tứ Trọng"
            elif total_views < 120000:
                return "Tiên Thiên Ngũ Trọng"
            elif total_views < 180000:
                return "Tiên Thiên Lục Trọng"
            elif total_views < 240000:
                return "Tiên Thiên Thất Trọng"
            elif total_views < 500000:
                return "Tiên Thiên Bát Trọng"
            elif total_views < 3000000:
                return "Tiên Thiên Cửu Trọng"
            elif total_views < 10000000:
                return "Trọng Thiên"
            else:
                return "Trùng Thiên Chi Thượng"

        else:
            return "Unknown Level System"

    def get_next_level(self, obj):
        level_system = obj.level_system or 'level'
        total_views = self.get_total_views(obj)
        points_per_level = 1000

        def get_next_level_index(index, levels):
            if index < len(levels) - 1:
                return levels[index + 1]
            return None

        if level_system == 'level':
            if total_views > 0:
                current_level = math.log2(total_views / points_per_level) + 1
                next_level_index = int(current_level)
                return f"Level {next_level_index + 1}"
            return "Level 1"

        elif level_system == 'tien_dao':
            levels = [
                "Luyện Khí", "Trúc Cơ", "Kim Đan", "Nguyên Anh", "Hóa Thần", 
                "Luyện Hư", "Hợp Thể", "Độ Kiếp", "Chân Tiên", "Kim Tiên", 
                "Thái Ất Kim Tiên", "Đại La Kim Tiên", "Hỗn Nguyên Kim Tiên", "Thiên Đạo"
            ]
            if total_views > 0:
                index = int(math.log2(total_views / points_per_level))
            else:
                index = 0
            next_level = get_next_level_index(index, levels)
            return next_level if next_level else "No Further Levels"

        elif level_system == 'vo_dao':
            if total_views <= 1000:
                levels = ["Hậu Thiên Nhất Trọng", "Hậu Thiên Nhị Trọng", "Hậu Thiên Tam Trọng", "Hậu Thiên Tứ Trọng", "Hậu Thiên Ngũ Trọng"]
                index = int(total_views / 200) 
                next_level = get_next_level_index(index, levels)
                return next_level if next_level else "No Further Levels"
            elif total_views <= 2000:
                levels = ["Hậu Thiên Lục Trọng", "Hậu Thiên Thất Trọng", "Hậu Thiên Bát Trọng", "Hậu Thiên Cửu Trọng"]
                index = int((total_views - 1000) / 250)  
                next_level = get_next_level_index(index, levels)
                return next_level if next_level else "No Further Levels"
            elif total_views < 8000:
                return "Tiên Thiên Nhất Trọng"
            elif total_views < 17000:
                return "Tiên Thiên Nhị Trọng"
            elif total_views < 32000:
                return "Tiên Thiên Tam Trọng"
            elif total_views < 64000:
                return "Tiên Thiên Tứ Trọng"
            elif total_views < 120000:
                return "Tiên Thiên Ngũ Trọng"
            elif total_views < 180000:
                return "Tiên Thiên Lục Trọng"
            elif total_views < 240000:
                return "Tiên Thiên Thất Trọng"
            elif total_views < 500000:
                return "Tiên Thiên Bát Trọng"
            elif total_views < 3000000:
                return "Tiên Thiên Cửu Trọng"
            elif total_views < 10000000:
                return "Trọng Thiên"
            else:
                return "Trùng Thiên Chi Thượng"

        else:
            return "Unknown Level System"

    def get_percentage_to_next_level(self, obj):
        level_system = self.context.get('level_system', 'level')
        total_views = self.get_total_views(obj)
        
        def get_next_level_data(total_views, levels, thresholds):
            for i, threshold in enumerate(thresholds):
                if total_views < threshold:
                    current_level = levels[i - 1] if i > 0 else levels[0]
                    next_level = levels[i]
                    return current_level, next_level, thresholds[i]
            return levels[-1], "No Further Levels", None

        def calculate_percentage(current_views, next_level_threshold):
            if next_level_threshold is not None and next_level_threshold > current_views:
                return min(100, (current_views / next_level_threshold) * 100)
            return 100

        if total_views <= 0:
            return "0.00%"

        if level_system == 'level':
            current_level = math.log2(total_views / 1000) + 1
            next_level_threshold = 1000 * (2 ** int(current_level))
            return f"{calculate_percentage(total_views, next_level_threshold):.2f}%"

        elif level_system == 'tien_dao':
            levels = [
                "Luyện Khí", "Trúc Cơ", "Kim Đan", "Nguyên Anh", "Hóa Thần", 
                "Luyện Hư", "Hợp Thể", "Độ Kiếp", "Chân Tiên", "Kim Tiên", 
                "Thái Ất Kim Tiên", "Đại La Kim Tiên", "Hỗn Nguyên Kim Tiên", "Thiên Đạo"
            ]
            thresholds = [1000 * (2 ** i) for i in range(len(levels) + 1)]
            current_level, next_level, next_level_threshold = get_next_level_data(total_views, levels, thresholds)
            return f"{calculate_percentage(total_views, next_level_threshold):.2f}%"

        elif level_system == 'vo_dao':
            levels = ["Hậu Thiên Nhất Trọng", "Hậu Thiên Nhị Trọng", "Hậu Thiên Tam Trọng", "Hậu Thiên Tứ Trọng", "Hậu Thiên Ngũ Trọng"]
            thresholds = [200 * (i + 1) for i in range(len(levels))] + [1000, 2000, 8000, 17000, 32000, 64000, 120000, 180000, 240000, 500000, 3000000, 10000000]
            
            if total_views <= 1000:
                current_level, next_level, next_level_threshold = get_next_level_data(total_views, levels, thresholds)
            else:
                thresholds = [1000, 2000, 8000, 17000, 32000, 64000, 120000, 180000, 240000, 500000, 3000000, 10000000]
                levels = [
                    "Hậu Thiên Nhất Trọng", "Hậu Thiên Nhị Trọng", "Hậu Thiên Tam Trọng", "Hậu Thiên Tứ Trọng", "Hậu Thiên Ngũ Trọng",
                    "Hậu Thiên Lục Trọng", "Hậu Thiên Thất Trọng", "Hậu Thiên Bát Trọng", "Hậu Thiên Cửu Trọng", "Tiên Thiên Nhất Trọng",
                    "Tiên Thiên Nhị Trọng", "Tiên Thiên Tam Trọng", "Tiên Thiên Tứ Trọng", "Tiên Thiên Ngũ Trọng", "Tiên Thiên Lục Trọng",
                    "Tiên Thiên Thất Trọng", "Tiên Thiên Bát Trọng", "Tiên Thiên Cửu Trọng", "Trọng Thiên", "Trùng Thiên Chi Thượng"
                ]
                current_level, next_level, next_level_threshold = get_next_level_data(total_views, levels, thresholds)
            
            return f"{calculate_percentage(total_views, next_level_threshold):.2f}%"

        else:
            return "Unknown Level System"




class QuyenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quyen
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    tinhtrang = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = '__all__'
    
    def get_total_views(self, obj):
        return obj.luot_xems.count()
    
    def get_tinhtrang(self, obj):
        id_tk = self.context.get('id_tk')
        if id_tk and LuotXem.objects.filter(id_tk=id_tk, id_chap=obj.id, tinhtrang=True).exists():
            return True
        return False
    



class TheLoaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheLoai
        fields = '__all__'

class LuotXemSerializer(serializers.ModelSerializer):
    truyen = TruyenSerializer(source='id_truyen', read_only=True)
    chapter = ChapterSerializer(source='id_chap', read_only=True)
    class Meta:
        model = LuotXem
        fields = '__all__'



class BinhLuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinhLuan
        fields = '__all__'

class BinhLuanSerializersss(serializers.ModelSerializer):
    truyen_info = serializers.SerializerMethodField()

    class Meta:
        model = BinhLuan
        fields = ['id', 'text', 'thoi_gian', 'key', 'nhac', 'id_tk', 'id_chap', 'id_truyen', 'truyen_info', 'url']

    def get_truyen_info(self, obj):
        try:
            truyen = Truyen.objects.get(id=obj.id_truyen.id)
            return {
                'name': truyen.name,
                'img_url': truyen.img_url
            }
        except Truyen.DoesNotExist:
            return None

class StorySerializer(serializers.ModelSerializer):
    id_truyen = TruyenSerializer()
    id_chapter = ChapterSerializer()
    class Meta:
        model = Story
        fields = '__all__'

class StorySerializerbb(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

class TopTruyenSerializer(serializers.ModelSerializer):
    latest_chap = serializers.DateTimeField()

    class Meta:
        model = Truyen
        fields = ['id', 'name','img', 'total_views', 'latest_chap']
        
from rest_framework.pagination import PageNumberPagination

class TruyenSerializers(serializers.ModelSerializer):
    total_views = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    total_follows = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    recent_chapters = serializers.SerializerMethodField()
    previous_week_start = serializers.SerializerMethodField()
    previous_week_end = serializers.SerializerMethodField()
    week_before_previous_week_start = serializers.SerializerMethodField()
    week_before_previous_week_end = serializers.SerializerMethodField()
    views_previous_week = serializers.SerializerMethodField()
    views_week_before_previous_week = serializers.SerializerMethodField()
    view_growth_rate = serializers.SerializerMethodField()
    viewed_status = serializers.SerializerMethodField()
    follow_id = serializers.SerializerMethodField()
    tinhtrang = serializers.SerializerMethodField()  # Add this field
    views_current_week = serializers.SerializerMethodField() 

    class Meta:
        model = Truyen
        fields = [
            'id', 'name', 'tinh_trang', 'gioi_thieu','img_url' ,'tac_gia', 'Limit', 'ten_khac', 'img', 
            'total_views', 'total_comments', 'total_follows', 'categories', 'recent_chapters',
            'previous_week_start', 'previous_week_end', 'week_before_previous_week_start', 
            'week_before_previous_week_end', 'views_previous_week', 'views_week_before_previous_week',
            'view_growth_rate', 'viewed_status', 'follow_id', 'tinhtrang', 'views_current_week'
        ]

    def get_total_views(self, obj):
        return LuotXem.objects.filter(id_truyen=obj.id).count()

    def get_total_comments(self, obj):
        return BinhLuan.objects.filter(id_truyen=obj.id).count()

    def get_total_follows(self, obj):
        return TheoDoi.objects.filter(id_truyen=obj.id, tinhtrang=True).count()

    def get_categories(self, obj):
        return TheLoaiSerializer(obj.nametl.all(), many=True).data

    def get_recent_chapters(self, obj):
        recent_chapters = Chapter.objects.filter(id_truyen=obj.id).order_by('-chap_ngay')[:3]
        return ChapterSerializer(recent_chapters, many=True, context={'id_tk': self.context.get('id_tk')}).data

    def get_previous_week_start(self, obj):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_previous_week = start_of_week - timedelta(days=7)
        return start_of_previous_week.strftime('%Y-%m-%d')

    def get_previous_week_end(self, obj):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_previous_week = start_of_week - timedelta(days=1)
        return end_of_previous_week.strftime('%Y-%m-%d')

    def get_week_before_previous_week_start(self, obj):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_previous_week = start_of_week - timedelta(days=7)
        start_of_week_before_previous_week = start_of_previous_week - timedelta(days=7)
        return start_of_week_before_previous_week.strftime('%Y-%m-%d')

    def get_week_before_previous_week_end(self, obj):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_previous_week = start_of_week - timedelta(days=7)
        end_of_week_before_previous_week = start_of_previous_week - timedelta(days=1)
        return end_of_week_before_previous_week.strftime('%Y-%m-%d')

    def get_views_previous_week(self, obj):
        start_date = datetime.strptime(self.get_previous_week_start(obj), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.get_previous_week_end(obj), '%Y-%m-%d').date()
        return LuotXem.objects.filter(id_truyen=obj.id, luotxem_ngay__date__range=[start_date, end_date]).count()

    def get_views_week_before_previous_week(self, obj):
        start_date = datetime.strptime(self.get_week_before_previous_week_start(obj), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.get_week_before_previous_week_end(obj), '%Y-%m-%d').date()
        return LuotXem.objects.filter(id_truyen=obj.id, luotxem_ngay__date__range=[start_date, end_date]).count()
    
    def get_view_growth_rate(self, obj):
        views_week_before_previous_week = self.get_views_week_before_previous_week(obj)
        views_previous_week = self.get_views_previous_week(obj)
        
        if views_week_before_previous_week == 0:
            return 0 if views_previous_week == 0 else 100
        
        growth_rate = ((views_previous_week - views_week_before_previous_week) / views_week_before_previous_week) * 100
        return growth_rate
    
    def get_viewed_status(self, obj):
        id_tk = self.context.get('id_tk')
        if LuotXem.objects.filter(id_tk=id_tk, id_truyen=obj.id).exists():
            return "Đã Đọc"
        return "Chưa Đọc"
    
    def get_follow_id(self, obj):
        id_tk = self.context.get('id_tk')
        theo_doi = TheoDoi.objects.filter(id_tk=id_tk, id_truyen=obj.id, tinhtrang=True).first()
        return theo_doi.id if theo_doi else None

    def get_tinhtrang(self, obj):
        id_tk = self.context.get('id_tk')
        if id_tk and LuotXem.objects.filter(id_tk=id_tk, id_truyen=obj.id, tinhtrang=True).exists():
            return True
        return False
    
    def get_views_current_week(self, obj):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        return LuotXem.objects.filter(id_truyen=obj.id, luotxem_ngay__date__gte=start_of_week).count()

    
    
from django.db.models import Avg, Sum
from datetime import datetime, timedelta

class TruyenSerializersss(serializers.ModelSerializer):
    diem_trung_binh = serializers.SerializerMethodField()

    class Meta:
        model = Truyen
        fields = ['id','name','img','img_url','diem_trung_binh']

    def get_diem_trung_binh(self, obj):
        danh_gias = DanhGia.objects.filter(id_truyen=obj)
        if danh_gias.count() == 0:
            return None
        return danh_gias.aggregate(Avg('diem'))['diem__avg']



class ChapterSerializerSTO(serializers.ModelSerializer):
    tinhtrang = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'tinhtrang']

    def get_tinhtrang(self, obj):
        id_truyen = self.context.get('id_truyen') 
        if not id_truyen:
            return False

        latest_luot_xem = LuotXem.objects.filter(id_chap=obj.id, id_truyen=id_truyen).order_by('-luotxem_ngay').first()
        if latest_luot_xem:
            return latest_luot_xem.tinhtrang
        return False

from rest_framework import serializers
from .models import Truyen, Chapter

class TruyenSerializerSTO(serializers.ModelSerializer):
    id_chap = serializers.SerializerMethodField()
    name_chap = serializers.SerializerMethodField()
    chap_ngay = serializers.SerializerMethodField()

    class Meta:
        model = Truyen
        fields = ['id', 'name', 'id_chap', 'name_chap', 'chap_ngay']  

    def get_id_chap(self, obj):
        id_chapter = self.context.get('id_chapter')
        if id_chapter is None:
            return None
        chapter = Chapter.objects.filter(id_truyen=obj.id, id=id_chapter).first()
        return chapter.id if chapter else None

    def get_name_chap(self, obj):
        id_chapter = self.context.get('id_chapter')
        if id_chapter is None:
            return None
        chapter = Chapter.objects.filter(id_truyen=obj.id, id=id_chapter).first()
        return chapter.name if chapter else None

    def get_chap_ngay(self, obj):
        id_chapter = self.context.get('id_chapter')
        if id_chapter is None:
            return None
        chapter = Chapter.objects.filter(id_truyen=obj.id, id=id_chapter).first()
        return chapter.chap_ngay if chapter else None



class StorySerializerSTO(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ['id','img','img_url']


class TaiKhoanSerializerkkk(serializers.ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = '__all__'

class BinhLuanSerializerkkk(serializers.ModelSerializer):
    tai_khoan = TaiKhoanSerializer(source='id_tk', read_only=True)
    chapter_name = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    truyen_name = serializers.SerializerMethodField()

    class Meta:
        model = BinhLuan
        fields = ['id', 'id_tk', 'text', 'thoi_gian', 'id_chap', 'da_doc','id_truyen', 'key', 'nhac', 'tai_khoan', 'chapter_name', 'total_likes', 'truyen_name']

    def get_chapter_name(self, obj):
        return obj.id_chap.name if obj.id_chap else "Unknown Chapter"

    def get_total_likes(self, obj):
        return LikeCmt.objects.filter(td_cmt=obj).count()

    def get_truyen_name(self, obj):
        return obj.id_truyen.name if obj.id_truyen else "Unknown Truyen"

class LikeCmtSerializer(serializers.ModelSerializer):
    td_cmt = BinhLuanSerializer(read_only=True) 
    id_tk = TaiKhoanSerializer(read_only=True)
    class Meta:
        model = LikeCmt
        fields = '__all__'


class LikeCmtSerializerb(serializers.ModelSerializer):
    class Meta:
        model = LikeCmt
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Thiếu tên đăng nhập hoặc mật khẩu.")
        
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Tên đăng nhập hoặc mật khẩu không chính xác.")
        
        return {'user': user}

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    newPassword = serializers.CharField(min_length=6)


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__' 

class TaiKhoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = '__all__' 

    

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Thêm thuộc tính `id_tk` vào token
        token['id_tk'] = str(user.id_tk)  # Sử dụng id_tk thay vì id

        return token

import numpy as np

import ast

class face_encodingSerializer(serializers.ModelSerializer):
    face_encoding = serializers.SerializerMethodField()  

    class Meta:
        model = TaiKhoan
        fields = ['id', 'face_encoding','username']  

    def get_face_encoding(self, obj):
        # Lấy dữ liệu face_encoding từ đối tượng
        encoding_list = obj.face_encoding  
        
        # Nếu có dữ liệu, trả về ngay mà không cần xử lý
        if encoding_list:
            return encoding_list  # Trả về dữ liệu như đã lưu trong cơ sở dữ liệu
        
        return None  # Trả về None nếu không có dữ liệu