from django.db import models
from django.core.validators import MaxValueValidator
import uuid
import os
import json
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import Sum
import math
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from cloudinary_storage.storage import MediaCloudinaryStorage

class Truyen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True)
    tinh_trang = models.CharField(max_length=50)
    gioi_thieu = models.TextField()
    tac_gia = models.TextField()
    ten_khac = models.TextField(null=True)
    img = models.ImageField(upload_to='truyen_images/', null=True, blank=True)
    img_url = models.TextField(null=True, blank=True)
    id_tk = models.CharField( null=True, blank=True)
    nametl = models.ManyToManyField('TheLoai', related_name='truyens')
    Limit = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    #def save(self, *args, **kwargs):
        #if self.img_url and not self.img:
            #response = requests.get(self.img_url)
            #if response.status_code == 200:
                #filename = os.path.basename(self.img_url)
                #file_path = os.path.join('truyen_images/', filename)

                #file_content = ContentFile(response.content, filename)
                #self.img.save(filename, file_content, save=False)

        #super(Truyen, self).save(*args, **kwargs)

class TheoDoi(models.Model):
    id = models.AutoField(primary_key=True)
    id_tk = models.CharField(max_length=255, null=True, blank=True) 
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='theo_dois')
    tinhtrang = models.BooleanField(default=False)

class DanhGia(models.Model):
    id = models.AutoField(primary_key=True)
    id_tk = models.CharField(max_length=255, null=True, blank=True)
    diem = models.IntegerField(null=True, validators=[MaxValueValidator(5)])
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='danh_gias')

import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings

class Quyen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quyen = models.CharField(max_length=255)

    def __str__(self):
        return self.quyen

class TaiKhoanManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Tạo và lưu một người dùng mới với email và password.
        """
        if not email:
            raise ValueError('Email phải được cung cấp')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)  # Không cần username
        user.set_password(password)  # Mã hóa mật khẩu trước khi lưu
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Tạo và lưu một superuser mới với email và password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Đảm bảo superuser luôn hoạt động

        return self.create_user(email, password, **extra_fields)
    

class TaiKhoan(AbstractBaseUser, PermissionsMixin):
    id_tk = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)  
    gioi_tinh = models.CharField(max_length=10, null=True, blank=True)
    noi_sinh = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to='truyen_images/', storage=MediaCloudinaryStorage(), null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    id_quyen = models.ForeignKey('Quyen', related_name='tai_khoans', on_delete=models.CASCADE, null=True, blank=True)
    dharma_name = models.TextField(max_length=20, null=True, blank=True)
    exp = models.PositiveIntegerField(default=0)
    level_system = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    face_encoding = models.JSONField(null=True, blank=True) 
    face_data = models.ImageField(upload_to='truyen_images/', storage=MediaCloudinaryStorage(), null=True, blank=True )  

    groups = models.ManyToManyField(Group, related_name='tai_khoan_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='tai_khoan_permissions', blank=True)

    objects = TaiKhoanManager()

    USERNAME_FIELD = 'email'  

    REQUIRED_FIELDS = [] 

    def save(self, *args, **kwargs):
        if not self.id:  # Nếu id chưa được gán
            self.id = str(self.id_tk)  # Gán giá trị của id_tk cho id
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.id = self.id_tk
        if not self.id_tk:
            self.id_tk = uuid.uuid4()
            self.id = self.id_tk
        if self.password and not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.username

    def set_face_encoding(self, encoding):

        self.face_encoding = json.dumps(encoding)  

    def get_face_encoding(self):

        if self.face_encoding:
            return json.loads(self.face_encoding)  
        return None
    
    def get_user_id(self):
        return str(self.id_tk)
    
class Level(models.Model):
    LEVEL_CHOICES = [
        ('normal', 'Bình Thường'),  
        ('tiendao', 'Tiên Đạo'),
        ('vodao', 'Võ Đạo'),
        ('maphap', 'Ma Pháp'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)  # Tên cấp bậc
    id_tk = models.ForeignKey('TaiKhoan', on_delete=models.CASCADE, related_name='levels')
    display_type = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='normal')  # Loại hiển thị

    def __str__(self):
        return f"Level: {self.name} - {self.display_type}"

class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Token {self.key} for {self.user.username}"


class TopTruyenDay(models.Model):
    date = models.DateField(unique=True)
    truyen_ids = models.JSONField()

    def __str__(self):
        return f"Top Truyens for {self.date}"

class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField()
    id_tk = models.CharField( null=True, blank=True)
    chap_ngay = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Story(models.Model):
    id = models.AutoField(primary_key=True)
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='stories')
    id_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='stories')
    img = models.ImageField(upload_to='truyen_images/', null=True, blank=True) 
    img_url = models.TextField(null=True, blank=True)

    #def save(self, *args, **kwargs):
        #if self.img_url and not self.img:
            #response = requests.get(self.img_url)
            #if response.status_code == 200:
                #filename = os.path.basename(self.img_url)
                #file_path = os.path.join('truyen_images/', filename)

                #file_content = ContentFile(response.content, filename)
                #self.img.save(filename, file_content, save=False)

        #super(Story, self).save(*args, **kwargs)

class TheLoai(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LuotXem(models.Model):
    id = models.AutoField(primary_key=True)
    id_tk = models.CharField(max_length=255, null=True, blank=True)
    tinhtrang = models.BooleanField(default=False)
    id_chap = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='luot_xems')
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='luot_xems')
    luotxem_ngay = models.DateTimeField(auto_now_add=True)
    so_luot_xem = models.IntegerField(default=1)
    ip = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"LuotXem id: {self.id}"


class BinhLuan(models.Model):
    id = models.AutoField(primary_key=True)
    id_tk = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, related_name='binh_luans')
    text = models.TextField()
    thoi_gian = models.DateTimeField(auto_now_add=True)  
    id_chap = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='binh_luans', null=True)
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='binh_luans')
    key = models.TextField(null=True, blank=True) 
    nhac = models.TextField(null=True, blank=True)  
    da_doc = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    




def generate_unique_id():
    return str(uuid.uuid4())

class LikeCmt(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=generate_unique_id)
    like = models.BooleanField(default=True)
    td_cmt = models.ForeignKey(BinhLuan, on_delete=models.CASCADE, related_name='LikeCmts')
    id_tk = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE, related_name='LikeCmts')
    id_truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='LikeCmts', null=True)

    

class Emoj(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField()
    tl = models.TextField()

    def __str__(self):
        return self.text