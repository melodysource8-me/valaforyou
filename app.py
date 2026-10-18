from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'vala_secret_key_2026'

# Data Produk Inklusif VALA
PRODUK_VALA = [
    {
        "id": 1,
        "nama": "Braille-Marked Velvet Lipstick",
        "kategori": "Lipstick",
        "harga": 120000,
        "fitur_aksesibilitas": "Label Braille & Tutup Magnetik Otomatis",
        "deskripsi": "Lipstick dengan label huruf Braille di bagian luar kemasan dan mekanisme tutup magnetik yang langsung terkunci presisi.",
        "gambar": "images/lipstick.jpg"
    },
    {
        "id": 2,
        "nama": "Matte Shea Foundation",
        "kategori": "Foundation",
        "harga": 185000,
        "fitur_aksesibilitas": "Tombol Tekan Lebar & Indikator Klik",
        "deskripsi": "Foundation dengan tombol tekan luas ramah motorik tangan dan bunyi klik pengaman untuk memastikan wadah tertutup rapat.",
        "gambar": "images/foundation.png"
    },
    {
        "id": 3,
        "nama": "Easy-Grip Eyebrow Pencil",
        "kategori": "Eyebrow",
        "harga": 85000,
        "fitur_aksesibilitas": "Gagang Segi Enam Anti-Slip & Label Braille",
        "deskripsi": "Pensil alis berdesain geometris agar tidak mudah menggelinding serta dilengkapi tekstur kesat untuk genggaman stabil.",
        "gambar": "images/eyebrow.jpg"
    },
    {
        "id": 4,
        "nama": "Magnetic Palette Eyeshadow",
        "kategori": "Eyeshadow",
        "harga": 210000,
        "fitur_aksesibilitas": "Sistem Magnetik & Buka-Tutup Satu Tangan",
        "deskripsi": "Palet perona mata dengan magnet kuat yang mudah dibuka menggunakan satu tangan oleh penyandang disabilitas fisik.",
        "gambar": "images/eyeshadow.jpg"
    }
]

@app.route('/')
def home():
    return render_template('index.html', show_products=False)

@app.route('/koleksi')
def koleksi():
    query = request.args.get('q', '').lower().strip()
    
    if query:
        hasil_pencarian = [
            p for p in PRODUK_VALA 
            if query in p['nama'].lower() 
            or query in p['kategori'].lower() 
            or query in p['fitur_aksesibilitas'].lower()
        ]
    else:
        hasil_pencarian = PRODUK_VALA

    return render_template(
        'index.html', 
        show_products=True, 
        produk=hasil_pencarian, 
        pencarian=request.args.get('q', '')
    )

@app.route('/tambah-keranjang/<int:product_id>', methods=['POST'])
def tambah_keranjang(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True
    
    return redirect(url_for('koleksi'))

@app.route('/keranjang')
def lihat_keranjang():
    cart_ids = session.get('cart', [])
    items_di_keranjang = [p for p in PRODUK_VALA if p['id'] in cart_ids]
    total_harga = sum(item['harga'] for item in items_di_keranjang)
    
    return render_template(
        'keranjang.html', 
        items=items_di_keranjang, 
        total=total_harga
    )

if __name__ == '__main__':
    app.run(debug=True)