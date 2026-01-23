from django.shortcuts import render, get_object_or_404

# 1. TẠO KHO DỮ LIỆU GIẢ (MOCK DATA)
products_data = [
    {
        'id': 1,
        'name': 'Đèn lồng đỏ truyền thống',
        'price': '150.000', # Để dạng chuỗi cho dễ hiển thị
        'image': 'https://salt.tikicdn.com/cache/750x750/ts/product/d0/20/7a/12a86847c2310137452d921356247c18.jpg.webp',
        'category': 'Đèn lồng',
        'icon': '🏮',
        'desc': 'Đèn lồng vải nhung đỏ thắm, khung thép chắc chắn, mang lại may mắn.'
    },
    {
        'id': 2,
        'name': 'Cành hoa mai vàng',
        'price': '180.000',
        'image': 'https://bizweb.dktcdn.net/100/443/076/products/trang-tri-tet-hoa-dao-dong.jpg',
        'category': 'Hoa mai/đào',
        'icon': '🌸',
        'desc': 'Cành hoa mai giả cao cấp, màu sắc tươi tắn, bền đẹp suốt mùa Tết.'
    },
    {
        'id': 3,
        'name': 'Bao lì xì hoa mai vàng',
        'price': '25.000',
        'image': 'https://salt.tikicdn.com/cache/w1200/ts/product/6e/c8/10/7c462744d03d09a06655c65b5302636a.jpg',
        'category': 'Bao lì xì',
        'icon': '🧧',
        'desc': 'Combo 10 bao lì xì giấy cứng, in họa tiết rồng vàng sang trọng.'
    },
    {
        'id': 4,
        'name': 'Dây treo chữ Phúc',
        'price': '45.000',
        'image': 'https://vn-test-11.slatic.net/p/3c73499427b20387498c89599d14620f.jpg',
        'category': 'Dây trang trí',
        'icon': '🎊',
        'desc': 'Dây treo trang trí cửa nhà, mang ý nghĩa Phúc Lộc Thọ toàn gia.'
    }
]

# Hàm hiển thị trang chủ
def index(request):
    return render(request, 'index.html')

# Hàm hiển thị chi tiết sản phẩm (ĐÃ SỬA: Nhận tham số product_id)
def product_detail(request, product_id):
    # Tìm sản phẩm trong danh sách dựa vào ID
    product = None
    for item in products_data:
        if item['id'] == product_id:
            product = item
            break
    
    # Nếu không tìm thấy sản phẩm nào (ví dụ ID=99) thì vẫn render trang nhưng product là None
    # Thực tế sau này sẽ dùng get_object_or_404
    
    context = {'product': product}
    return render(request, 'product_detail.html', context)