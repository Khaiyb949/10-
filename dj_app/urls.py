from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_app import views
from .views import *
from django.urls import re_path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'truyenbb', views.TruyenViewSetbb, basename='truyenbb')
router.register(r'truyen', views.TruyenViewSet, basename='truyen')
router.register(r'theodoi', views.TheoDoiViewSet, basename='theodoi')
router.register(r'danhgia', views.DanhGiaViewSet, basename='danhgia')
router.register(r'taikhoan', views.TaiKhoanViewSet, basename='taikhoan')
router.register(r'quyen', views.QuyenViewSet, basename='quyen')
router.register(r'chapter', views.ChapterViewSet, basename='chapter')
router.register(r'theloai', views.TheLoaiViewSet, basename='theloai')
router.register(r'luotxem', views.LuotXemViewSet, basename='luotxem')
router.register(r'binhluan', views.BinhLuanViewSet, basename='binhluan')
router.register(r'story', views.StoryViewSet, basename='story')
router.register(r'emoj', views.EmojViewSet, basename='emoj')
router.register(r'likecmt', views.LikeCmtViewSet, basename='likecmt')
router.register(r'level', views.LevelViewSet, basename='level')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/luotxem/id_truyen/<int:id_truyen>/', views.LuotXemListAPIView.as_view(), name='luotxem-list'),
    path('api/binhluan/id_truyen/<int:id_truyen>/', views.BinhLuanListAPIView.as_view(), name='BinhLuan-list'),
    path('api/theodoi/id_truyen/<int:id_truyen>/', views.TheoDoiListAPIView.as_view(), name='TheoDoi-list'),
    path('api/chapter/id_truyen/<int:id_truyen>/', views.ChapterListAPIView.as_view(), name='Chapter-list'),
    path('api/story/id_truyen/<int:id_truyen>/id_chapter/<int:id_chapter>/', StoryListAPIView.as_view(), name='story-list'),
    path('api/sum/id_truyen/<int:id_truyen>/', SumLuotXemView.as_view(), name='sum_luotxem'),
    path('api/sum_bl/id_truyen/<int:id_truyen>/', SumBinhLuanView.as_view(), name='sum_bl'),
    path('api/sum_td/id_truyen/<int:id_truyen>/', SumTheoDoiView.as_view(), name='sum_td'),
    path('api/sum/id_truyen/<int:id_truyen>/id_chap/<int:id_chap>/', SumLuotXemByChapView.as_view(), name='sum_luotxem_by_chap'),
    path('api/top3_chapter/<int:id_truyen>/', views.top3_chapter, name='top3_chapter'),
    path('api/top-truyen-thang/', TopTruyenAPI.as_view(), name='top-truyen-thang'),
    path('api/top-truyen-tuan/', TopTruyenTuanAPI.as_view(), name='top-truyen-tuan'),
    path('api/top-truyen-ngay/', TopTruyenNgayAPI.as_view(), name='top-truyen-ngay'),
    path('api/<str:id_tk>/top-truyen/', top_truyen_api, name='top-truyen'),
    path('api/truyens/<str:id_tk>/all/', TruyenListView.as_view(), name='truyen-list'),
    path('api/lichsu_xem_truyen/<str:id_tk>/', LichSuXemTruyenView.as_view(), name='lichsu_xem_truyen'),
    path('truyen/<int:id>/', TruyenDetailView.as_view(), name='truyen-detail'),
    path('api/random-truyen/', RandomTruyenView.as_view(), name='random-truyen'),
    path('api/chapters/<int:id_truyen>/', ChapterListView.as_view(), name='chapter-list'),
    path('api/danhgia/id_tk/<str:id_tk>/id_truyen/<int:id_truyen>/', DanhGiaDetailView.as_view(), name='danhgia-detail'),
    path('api/theodoi/td_tk/<str:id_tk>/td_truyen/<int:id_truyen>/', TheoDoiListView.as_view(), name='theodoi-list'),
    path('api/binh-luan/<int:id_truyen>/', BinhLuanListView.as_view(), name='binh-luan-list'),
    path('api/binh-luan/<int:id>/keys/', BinhLuanKeyListView.as_view(), name='binh-luan-keys'),
    path('api/like/id_tk/<str:id_tk>/id_truyen/<int:id_truyen>/check/', CheckLikeAPIView.as_view(), name='check-like'),
    path('api/hot-truyens/', HotTruyenListView.as_view(), name='hot-truyens-list'),
    path('api/followed-truyen/<str:id_tk>/', FollowedTruyenListView.as_view(), name='followed-truyen-list'),
    path('api/unviewed-truyen-list/<str:id_tk>/', UnviewedTruyenListView.as_view(), name='unviewed-truyen-list'),
    path('api/view-history/<str:id_tk>/', ViewHistoryAPIView.as_view(), name='view-history'),
    path('api/view-history-by-ip/<str:ip>/', ViewHistoryByIPAPIView.as_view(), name='view-history-by-ip'),
    path('api/Search-truyens/', TruyenListViews.as_view(), name='truyen-list'),
    path('api/taikhoanpost/', views.create_taikhoan, name='create_taikhoan'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/top-truyensss/<str:id_tk>/', TopTruyenViewsss.as_view(), name='top-truyen'),
    path('api/top-5-binh-luan/<str:id_tk>/', Top5BinhLuanView.as_view(), name='top-5-binh-luan'),
    path('api/get-id-tk-by-email/<str:email>/', get_id_tk_by_email, name='get_id_tk_by_email'),
    path('api/xx/<int:id_theloai>/go/', get_truyen_by_theloai, name='get_truyen_by_theloai'),
    path('api/binh-luan/<int:id_truyen>/<int:id_chap>/', BinhLuanListViews.as_view(), name='binh-luan-list-with-chap'),
    path('api/binh-luan/<int:id>/keys/<int:id_chap>/', BinhLuanKeyAndChapterListView.as_view(), name='binh-luan-key-chapter-list'),
    path('api/taikhoans/<uuid:id_tk>/', update_image, name='update_image'),
    path('api/send-reset-code/', send_reset_code, name='send-reset-code'),
    path('api/verify-code/', verify_code, name='verify-code'),
    path('api/reset-password/', reset_password, name='reset-password'),
    path('api/check-old-password/<uuid:id_tk>/', check_old_password, name='check_old_password'),
    path('api/change-password/<uuid:id_tk>/', change_password, name='change_password'),
    path('api/bl_false/<uuid:id_tk>/', TopBinhLuanAPIView.as_view(), name='top-binh-luan'),
    path('api/bl_all/<uuid:id_tk>/', TatCaBinhLuanAPIView.as_view(), name='top-binh-luan'),
    path('api/stories/<int:id_chapter>/', StoryListByChapter.as_view(), name='story-list-by-chapter'),
    path('api/chapter/check/', check_chapter_exists, name='check_chapter_exists'),
    path('api/dangky/', DangKyKhuonMatView.as_view(), name='dang_ky_khuon_mat'),
    path('api/kiemtra', KiemTraKhuonMatView.as_view(), name='kiem_tra_khuon_mat'),
    path('api/view/statistics/', LuotXemStatisticsView.as_view(), name='luotxem_statistics'),

    path('api/logins/', login_view, name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/check/', AuthCheckView.as_view(), name='token_check'),
    path('api/tool/',id_id_tk, name='id_id_tk'),
    path('api/face_encoding/', face_encodingListView.as_view(), name='tai-khoan-list'),

    re_path(
        r"^(?!admin|admins|truyen_images|assets|api).*$",
        ensure_csrf_cookie(AngularViewClient.as_view()),
        name="client",
    ),
    re_path(
        r"^admin/.*$",
        ensure_csrf_cookie(AngularAdminView.as_view()),
        name="admin",
    ),
    re_path(
        r"^admins/.*$",
        ensure_csrf_cookie(AngularAdminView.as_view()),
        name="admins",
    ),
    path("assets/<path:path>", CustomRedirectView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
