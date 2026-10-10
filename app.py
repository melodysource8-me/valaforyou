import os
import secrets

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

PRODUCTS = [
    {
        "id": 1, 
        "nama": "Easy-Grip Liquid Foundation", 
        "kategori": "Foundation", 
        "harga": 185000, 
        "deskripsi": "Dilengkapi dengan botol bertali fleksibel dan tutup beralur taktil yang mudah dibuka tanpa memerlukan genggaman kuat.",
        "fitur_aksesibilitas": "Tutup Taktil & Tali Silikon Easy-Hold"
    },
    {
        "id": 2, 
        "nama": "Braille-Marked Velvet Lipstick", 
        "kategori": "Lipstik", 
        "harga": 120000, 
        "deskripsi": "Lipstik dengan label huruf Braille di bagian luar kemasan dan mekanisme tutup magnetik yang langsung terkunci presisi.",
        "fitur_aksesibilitas": "Label Braille & Tutup Magnetik Otomatis"
    },
    {
        "id": 3, 
        "nama": "Single-Touch Glow Palette", 
        "kategori": "Palette", 
        "harga": 250000, 
        "deskripsi": "Palet kosmetik dengan tekstur permukaan timbul (embossed) untuk membedakan eyeshadow, blush, dan highlighter secara indrawi.",
        "fitur_aksesibilitas": "Tekstur Taktil & Pengunci Magnetik"
    },
    {
        "id": 4, 
        "nama": "Ergonomic Brow Definer", 
        "kategori": "Mata", 
        "harga": 95000, 
        "deskripsi": "Pensil alis dengan pegangan bentuk segitiga ergonomis yang stabil untuk genggaman dengan kemampuan motorik terbatas.",
        "fitur_aksesibilitas": "Pegangan Segitiga Ergonomis Anti-Slip"
    }
]

# Rute Beranda Utama (HANYA Beranda & About VALA)
@app.route('/')
def home():
    return render_template('index.html', show_products=False)

# Rute Khusus Koleksi Produk
@app.route('/koleksi')
def koleksi():
    query = request.args.get('q', '').lower()
    if query:
        hasil = [p for p in PRODUCTS if query in p['nama'].lower() or query in p['kategori'].lower() or query in p['fitur_aksesibilitas'].lower()]
    else:
        hasil = PRODUCTS
    return render_template('index.html', produk=hasil, pencarian=query, show_products=True)

@app.route('/tambah-keranjang/<int:product_id>', methods=['POST'])
def tambah_keranjang(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    produk = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if produk:
        session['cart'].append(produk)
        session.modified = True
        
    return redirect(url_for('lihat_keranjang'))

@app.route('/keranjang')
def lihat_keranjang():
    cart = session.get('cart', [])
    total_harga = sum(item['harga'] for item in cart)
    return render_template('keranjang.html', cart=cart, total=total_harga)

@app.route('/hapus-keranjang/<int:index>', methods=['POST'])
def hapus_keranjang(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('lihat_keranjang'))

if __name__ == '__main__':
    app.run(debug=True)