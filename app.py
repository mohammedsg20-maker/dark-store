import streamlit as st
import json
import os
import random

# --- 1. نظام الحفظ (Persistence) لضمان التزامن مع ولد عمك ---
DB_FILE = "database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "inventory": [
            {"id": 1, "game": "فورت نايت", "title": "OG حساب بنت الطيارة", "price": 450, "img": "https://img.youtube.com/vi/jS8XU_pG_a0/maxresdefault.jpg"},
            {"id": 2, "game": "روكيت ليق", "title": "حساب جراند شامبيون", "price": 130, "img": "https://i.ytimg.com/vi/qY_3m6_7_pE/maxresdefault.jpg"}
        ],
        "barq_info": "يرجى تزويد العميل برابط دفع برق هنا"
    }

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = load_data()

# --- 2. التصميم CSS (اللون البنفسجي والأسود) ---
st.set_page_config(page_title="DARK STORE | DK", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background-color: #0b0b0e; color: #ffffff; }
    .product-card {
        background: #1c1c24; border: 1px solid #333; border-radius: 15px;
        padding: 15px; text-align: center; transition: 0.3s;
    }
    .product-card:hover { border-color: #8A2BE2; transform: translateY(-5px); }
    .dk-logo-btn { 
        background: #8A2BE2; color: #fff; padding: 10px 20px; 
        border-radius: 12px; font-weight: 900; cursor: pointer; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. المتغيرات والتحكم ---
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'clicks' not in st.session_state: st.session_state.clicks = 0
MY_WHATSAPP = "9665XXXXXXXX" # حط رقمك هنا لإرسال الإيصالات

# --- 4. الهيدر والزر السري (DK) ---
col_logo, col_empty = st.columns([1, 5])
with col_logo:
    # هذا هو الزر السري (اضغط 5 مرات لفتح الإدارة)
    if st.button("DK", key="secret_admin_trigger"):
        st.session_state.clicks += 1
        if st.session_state.clicks >= 5:
            st.session_state.show_login = True

if st.session_state.get('show_login') and not st.session_state.is_admin:
    with st.form("login_admin"):
        u = st.text_input("يوزر القائد")
        p = st.text_input("باسورد القائد", type="password")
        if st.form_submit_button("دخول"):
            if u == "admin" and p == "BOSS":
                st.session_state.is_admin = True
                st.session_state.show_login = False
                st.rerun()

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>القائمة</h2>", unsafe_allow_html=True)
    cat = st.radio("اختر القسم:", ["الرئيسية", "فورت نايت", "روكيت ليق", "ديسكورد"])
    st.divider()
    if st.session_state.is_admin:
        st.success("وضع القائد مفعل 👑")
        if st.button("🚪 خروج"):
            st.session_state.is_admin = False
            st.session_state.clicks = 0
            st.rerun()

# --- 6. لوحة الإدارة (تعديل المنتجات وبطاقة برق) ---
if st.session_state.is_admin:
    st.header("🛠️ لوحة القائد لتعديل المتجر")
    
    # تعديل معلومات برق
    st.subheader("💳 إعدادات الدفع (برق / Barq)")
    st.session_state.db['barq_info'] = st.text_area("أدخل الآيبان أو رابط الدفع الخاص بك:", st.session_state.db['barq_info'])
    
    # إضافة منتج جديد
    with st.form("add_product"):
        st.subheader("➕ إضافة حساب جديد")
        t = st.text_input("اسم الحساب")
        p = st.number_input("السعر")
        g = st.selectbox("القسم", ["فورت نايت", "روكيت ليق", "ديسكورد"])
        img = st.text_input("رابط الصورة المباشر")
        if st.form_submit_button("حفظ المنتج ✅"):
            st.session_state.db['inventory'].append({"id": random.randint(100, 999), "game": g, "title": t, "price": p, "img": img})
            save_data(st.session_state.db) # الحفظ لضمان المزامنة
            st.success("تم الحفظ بنجاح!")
            st.rerun()

    # إدارة المنتجات الحالية
    st.subheader("📦 إدارة المخزون الحالي")
    for idx, item in enumerate(st.session_state.db['inventory']):
        c1, c2 = st.columns([3, 1])
        item['price'] = c1.number_input(f"سعر {item['title']}", value=float(item['price']), key=f"edit_{idx}")
        if c2.button("حذف ❌", key=f"del_{idx}"):
            st.session_state.db['inventory'].pop(idx)
            save_data(st.session_state.db)
            st.rerun()

# --- 7. عرض واجهة المتجر ---
st.markdown("<h1 style='text-align:center;'>🎮 DARK STORE</h1>", unsafe_allow_html=True)
st.divider()

display_items = [i for i in st.session_state.db['inventory'] if cat == "الرئيسية" or i['game'] == cat]
cols = st.columns(3)

for idx, item in enumerate(display_items):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="product-card">
            <img src="{item['img']}" style="width:100%; border-radius:10px; height:180px; object-fit:cover;">
            <h3>{item['title']}</h3>
            <h2 style="color:#8A2BE2;">{item['price']} ريال</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"شراء الآن", key=f"buy_btn_{idx}", use_container_width=True):
            st.markdown(f"""
            <div style="background:#16161a; border:1px solid #8A2BE2; padding:15px; border-radius:10px; margin-top:10px; text-align:center;">
                <p>حول المبلغ لبطاقة برق (Barq):</p>
                <p style="color:#8A2BE2; font-weight:bold;">{st.session_state.db['barq_info']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            msg = f"تم تحويل {item['price']} ريال لشراء {item['title']}. مرفق الإيصال:"
            st.markdown(f'<a href="https://wa.me/{MY_WHATSAPP}?text={msg}" target="_blank"><button style="width:100%; background:green; color:white; border:none; padding:10px; border-radius:5px; margin-top:10px; cursor:pointer;">إرسال إيصال الدفع للقائد ✅</button></a>', unsafe_allow_html=True)

# --- 8. الفوتر الاحترافي ---
st.markdown("""
<div style="text-align:center; margin-top:60px; padding:20px; border-top:1px solid #222;">
    <div style="margin-bottom:15px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Apple_Pay_logo.svg" width="45">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" width="45">
        <span style="background:white; color:black; padding:3px 10px; border-radius:5px; font-weight:bold; margin-left:10px;">mada</span>
    </div>
    <p>موثق في منصة الأعمال ✅ | الحقوق محفوظة لمتجر يووكس/DK 2026</p>
</div>
""", unsafe_allow_html=True)
