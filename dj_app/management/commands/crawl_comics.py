import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from dj_app.models import Truyen, Chapter, Story, TheLoai
from urllib.parse import urljoin
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time



def print_progress_bar(iteration, total, prefix='', length=40):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '=' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% Complete')
    sys.stdout.flush()

class Command(BaseCommand):
    help = 'Lấy thông tin từ trang web'

    def handle(self, *args, **kwargs):
        base_url = 'https://www.nettruyenac.com/?page='
        total_pages = 1215
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1'
        }



        for page_number in range(1, total_pages + 1):
            page_url = f'{base_url}{page_number}'

            print_progress_bar(page_number, total_pages, prefix='Đang lấy dữ liệu từ các trang', length=40)

            all_item_links = []
            existing_detail_urls = set(Truyen.objects.values_list('id_tk', flat=True))
            existing_chapter_links = set(Chapter.objects.values_list('id_tk', flat=True))

            try:
                response = requests.get(page_url, headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Yêu cầu HTTP không thành công. Lỗi: {e}"))
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            items_container = soup.find('div', class_='items')
            if items_container:
                item_elements = items_container.find_all('div', class_='item')
                item_links = [item.find('a', href=True)['href'] for item in item_elements if item.find('a', href=True)]
                all_item_links.extend([urljoin(base_url, link) for link in item_links])

            total_items = len(all_item_links)
            chunk_size = 36

            def process_chunk(chunk):

                base_urls = [
                    "https://nettruyenha.com/",
                    "https://nettruyenhq.com/",
                    "https://nettruyenac.com/"
                ]
                for idx, detail_url in enumerate(chunk):
                    print_progress_bar(idx + 1, len(chunk), prefix='Xử lý liên kết', length=36)

                    relative_url = detail_url
                    for base_url in base_urls:
                        if detail_url.startswith(base_url):
                            relative_url = detail_url[len(base_url):]
                            break

                    if relative_url in existing_detail_urls:
                        self.stdout.write(self.style.WARNING(f"Liên kết đã có: {detail_url}"))
                        self.update_missing_chapters(Truyen.objects.get(id_tk=relative_url), relative_url, base_url, existing_chapter_links)
                        time.sleep(2)
                        continue

                    self.stdout.write(self.style.SUCCESS(f"Đang xử lý liên kết: {detail_url}"))

                    try:
                        response = requests.get(detail_url, headers=headers)
                        response.raise_for_status()
                    except requests.RequestException as e:
                        self.stdout.write(self.style.ERROR(f"Yêu cầu HTTP không thành công. Lỗi: {e}"))
                        time.sleep(2)
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')
                    detail_info = {}

                    h1_tag = soup.find('h1', class_='title-detail')
                    if h1_tag:
                        detail_info['name'] = h1_tag.get_text(strip=True)

                    img_tag = soup.find('img', class_='lozad')
                    if img_tag and 'src' in img_tag.attrs:
                        detail_info['img_url'] = img_tag['src']

                    h2_tag = soup.find('h2', class_='other-name col-xs-8')
                    if h2_tag:
                        detail_info['ten_khac'] = h2_tag.get_text(strip=True)

                    li_author_tag = soup.find('li', class_='author row')
                    if li_author_tag:
                        author_p_tag = li_author_tag.find('p', class_='col-xs-8')
                        if author_p_tag:
                            detail_info['tac_gia'] = author_p_tag.get_text(strip=True)

                    li_status_tag = soup.find('li', class_='status row')
                    if li_status_tag:
                        status_p_tag = li_status_tag.find('p', class_='col-xs-8')
                        if status_p_tag:
                            detail_info['tinh_trang'] = status_p_tag.get_text(strip=True)

                    li_kind_tag = soup.find('li', class_='kind row')
                    if li_kind_tag:
                        kind_p_tag = li_kind_tag.find('p', class_='col-xs-8')
                        if kind_p_tag:
                            kind_links = kind_p_tag.find_all('a')
                            kind_list = [link.get_text(strip=True) for link in kind_links]
                            detail_info['nametl'] = kind_list

                    detail_content_div = soup.find('div', class_='detail-content')
                    if detail_content_div:
                        list_title_tag = detail_content_div.find('h3', class_='list-title')
                        if list_title_tag:
                            title_text = list_title_tag.get_text(strip=True)
                            title_text = title_text.replace("TopTruyen", "KTruyen").replace("NetTruyen", "KTruyen").replace("truyen", "KTruyen")
                            detail_info['gioi_thieu'] = title_text

                        paragraphs = detail_content_div.find_all('p')
                        paragraph_texts = [para.get_text(strip=True).replace("TopTruyen", "KTruyen").replace("NetTruyen", "KTruyen").replace("truyen", "KTruyen") for para in paragraphs]
                        detail_info['gioi_thieu'] = "\n".join(paragraph_texts)

                    truyen, created = Truyen.objects.update_or_create(
                        id_tk=detail_url,
                        defaults={
                            'name': detail_info.get('name', 'Tên chưa có'),
                            'tinh_trang': detail_info.get('tinh_trang', 'Chưa có tình trạng'),
                            'gioi_thieu': detail_info.get('gioi_thieu', 'Chưa có giới thiệu'),
                            'tac_gia': detail_info.get('tac_gia', 'Chưa có tác giả'),
                            'ten_khac': detail_info.get('ten_khac', 'Chưa có tên khác'),
                            'img_url': detail_info.get('img_url', 'Chưa có hình ảnh'),
                        }
                    )

                    if 'nametl' in detail_info:
                        kind_names = detail_info['nametl']
                        kinds = [TheLoai.objects.get_or_create(name=name)[0] for name in kind_names]
                        truyen.nametl.set(kinds)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Đã tạo mới Truyen: {detail_url}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Đã cập nhật Truyen: {detail_url}"))

                    nav_desc = soup.find('div', id='nt_listchapter')
                    if nav_desc:
                        chapter_links = nav_desc.select('.row .chapter a')
                        if chapter_links:
                            for chapter_link in reversed([a for a in chapter_links]):
                                chapter_url = urljoin(base_url, chapter_link['href'])
                                chapter_title = chapter_link.get_text(strip=True)

                                if chapter_url not in existing_chapter_links:
                                    self.stdout.write(self.style.SUCCESS(f"Đang xử lý chương: {chapter_url}"))

                                    try:
                                        response = requests.get(chapter_url, headers=headers)
                                        response.raise_for_status()
                                    except requests.RequestException as e:
                                        self.stdout.write(self.style.ERROR(f"Yêu cầu HTTP không thành công. Lỗi: {e}"))
                                        continue

                                    soup = BeautifulSoup(response.content, 'html.parser')
                                    containers = soup.select('div.reading-detail.box_doc div.page-chapter')

                                    images = []
                                    for container in containers:
                                        img = container.find('img')
                                        if img:
                                            img_data_src = img.get('data-src')
                                            if img_data_src:
                                                images.append(img_data_src)

                                    chapter, created = Chapter.objects.update_or_create(
                                        id_tk=chapter_url,
                                        defaults={
                                            'id_truyen': truyen,
                                            'name': chapter_title,
                                        }
                                    )

                                    if created:
                                        self.stdout.write(self.style.SUCCESS(f"Đã tạo mới Chapter: {chapter_url}"))
                                    else:
                                        self.stdout.write(self.style.SUCCESS(f"Đã cập nhật Chapter: {chapter_url}"))

                                    for img_url in images:
                                        Story.objects.update_or_create(
                                            id_chapter=chapter,
                                            img_url=img_url,
                                            defaults={'id_truyen': truyen}
                                        )

                                    self.stdout.write(self.style.SUCCESS(f"Đã lưu ảnh cho Chapter: {chapter_url}"))
                                time.sleep(2)

            # Use ThreadPoolExecutor to process chunks of item links
            with ThreadPoolExecutor(max_workers=36) as executor:
                futures = [executor.submit(process_chunk, all_item_links[i:i + chunk_size]) for i in range(0, len(all_item_links), chunk_size)]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Xảy ra lỗi khi xử lý dữ liệu: {e}"))

        self.stdout.write(self.style.SUCCESS('Xong việc!'))

    def update_missing_chapters(self, truyen, detail_url, base_url, existing_chapter_links):
        # Function to update chapters for a specific truyen if it exists
        response = requests.get(detail_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        nav_desc = soup.find('div', id='nt_listchapter')

        if nav_desc:
            chapter_links = nav_desc.select('.row .chapter a')
            if chapter_links:
                for chapter_link in reversed([a for a in chapter_links]):
                    chapter_url = urljoin(base_url, chapter_link['href'])
                    if chapter_url not in existing_chapter_links:
                        self.stdout.write(self.style.SUCCESS(f"Đang xử lý chương mới: {chapter_url}"))
                        time.sleep(2)

                        try:
                            response = requests.get(chapter_url, headers={'User-Agent': 'Mozilla/5.0'})
                            response.raise_for_status()
                        except requests.RequestException as e:
                            self.stdout.write(self.style.ERROR(f"Yêu cầu HTTP không thành công. Lỗi: {e}"))
                            time.sleep(2)
                            continue

                        soup = BeautifulSoup(response.content, 'html.parser')
                        containers = soup.select('div.reading-detail.box_doc div.page-chapter')

                        images = []
                        for container in containers:
                            img = container.find('img')
                            print("Container:", container)  # In ra container để kiểm tra
                            if img and img.has_attr('src'):
                                img_data_src = img['src']
                                images.append(img_data_src)
                            else:
                                print("Không tìm thấy ảnh hoặc không có thuộc tính src. Dừng vòng lặp.")
                                break


                        chapter, created = Chapter.objects.update_or_create(
                            id_tk=chapter_url,
                            defaults={
                                'id_truyen': truyen,
                                'name': chapter_link.get_text(strip=True),
                            }
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Đã tạo mới Chapter: {chapter_url}"))
                            time.sleep(2)
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Đã cập nhật Chapter: {chapter_url}"))
                            time.sleep(2)

                        for img_url in images:
                            Story.objects.update_or_create(
                                id_chapter=chapter,
                                img_url=img_url,
                                defaults={'id_truyen': truyen}
                            )

                        self.stdout.write(self.style.SUCCESS(f"Đã lưu ảnh cho Chapter: {chapter_url}"))

