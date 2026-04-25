import streamlit as st
import json
import os
import random

# --- 1. إعدادات قاعدة البيانات (للمزامنة مع ولد عمك) ---
DB_FILE = "database.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "inventory": [
            {"id": 1, "game": "فورت نايت", "title": "حساب شيطون OG", "price": 450, "img": "https://img.youtube.com/vi/jS8XU_pG_a0/maxresdefault.jpg"},
            {"id": 2, "game": "روكيت ليق", "title": "حساب وايت زومبا", "price": 130, "img": "https://i.ytimg.com/vi/qY_3m6_7_pE/maxresdefault.jpg"}
        ],
        "barq_info": "ضع آيبان برق هنا"
    }

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'db' not in st.session_state:
    st.session_state.db = load_data()

# --- 2. تصميم CSS الخرافي (Dark & Neon Purple) ---
st.set_page_config(page_title="DARK STORE", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background: radial-gradient(circle, #1a1a2e 0%, #0b0b0e 100%); color: #ffffff; }
    
    /* كرت المنتج */
    .product-card {
        background: rgba(28, 28, 36, 0.8);
        border: 1px solid #8A2BE2;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        transition: 0.4s;
    }
    .product-card:hover { transform: scale(1.05); box-shadow: 0 0 20px #8A2BE2; }
    
    /* اللوقو السري */
    .dk-logo {
        background: linear-gradient(45deg, #8A2BE2, #4B0082);
        color: white; padding: 15px 30px;
        border-radius: 15px; font-weight: 900; font-size: 24px;
        cursor: pointer; border: none; box-shadow: 0 0 15px #8A2BE2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الحالة ---
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'clicks' not in st.session_state: st.session_state.clicks = 0
MY_WHATSAPP = "966555525316" # حط رقمك الحقيقي هنا

# --- 4. الهيدر والزر السري ---
col_logo, col_space = st.columns([1, 4])
with col_logo:
    if st.button("DK ⚡", key="secret_master"):
        st.session_state.clicks += 1
        if st.session_state.clicks >= 5:
            st.session_state.show_login = True

if st.session_state.get('show_login') and not st.session_state.is_admin:
    with st.form("admin_login"):
        u = st.text_input("يوزر القائد")
        p = st.text_input("باسورد القائد", type="password")
        if st.form_submit_button("دخول"):
            if u == "admin" and p == "BOSS":
                st.session_state.is_admin = True
                st.session_state.show_login = False
                st.rerun()

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h1 style='color:#8A2BE2;'>DARK STORE</h1>", unsafe_allow_html=True)
    cat = st.selectbox("الأقسام", ["الكل", "فورت نايت", "روكيت ليق", "ديسكورد"])
    st.divider()
    if st.session_state.is_admin:
        st.success("وضع القائد مفعل 👑")
        if st.button("🚪 خروج"):
            st.session_state.is_admin = False
            st.session_state.clicks = 0
            st.rerun()

# --- 6. لوحة الإدارة (تعديل الأقسام والأسعار) ---
if st.session_state.is_admin:
    with st.expander("🛠️ لوحة تحكم القائد (اضغط للتوسيع)"):
        st.subheader("💳 إعدادات برق")
        st.session_state.db['barq_info'] = st.text_input("آيبان برق أو رابط الدفع:", st.session_state.db['barq_info'])
        
        st.divider()
        st.subheader("➕ إضافة حساب جديد")
        with st.form("new_item"):
            t = st.text_input("اسم المنتج")
            p = st.number_input("السعر")
            g = st.selectbox("القسم", ["فورت نايت", "روكيت ليق", "ديسكورد"])
            img = st.text_input("رابط الصورة")
            if st.form_submit_button("حفظ وإضافة للموقع ✅"):
                st.session_state.db['inventory'].append({"id": random.randint(10,99), "game": g, "title": t, "price": p, "img": img})
                save_data(st.session_state.db)
                st.success("تم الحفظ!")
                st.rerun()

# --- 7. واجهة عرض المنتجات ---
st.markdown("<h2 style='text-align:center;'>🔥 أحدث الحسابات النادرة 🔥</h2>", unsafe_allow_html=True)

display_items = [i for i in st.session_state.db['inventory'] if cat == "الكل" or i['game'] == cat]

cols = st.columns(3)
for idx, item in enumerate(display_items):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="product-card">
            <img src="{item['img']}" style="width:100%; border-radius:15px; height:200px; object-fit:cover; margin-bottom:15px;">
            <h3>{item['title']}</h3>
            <h2 style="color:#8A2BE2;">{item['price']} ريال</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"شراء الآن ✅", key=f"buy_{idx}", use_container_width=True):
            st.markdown(f"""
            <div style="background:#16161a; border:2px dashed #8A2BE2; padding:15px; border-radius:10px; margin-top:10px; text-align:center;">
                <p>حول المبلغ لبطاقة برق:</p>
                <h4 style="color:#8A2BE2;">{st.session_state.db['barq_info']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            wa_link = f"https://wa.me/{MY_WHATSAPP}?text=أبي أشتري {item['title']} بـ {item['price']} ريال"
            st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">إرسال إيصال الدفع واتساب ✅</button></a>', unsafe_allow_html=True)

# --- 8. الفوتر (Footer) ---
st.markdown("""
<div style="text-align:center; margin-top:100px; padding:40px; border-top:1px solid #333;">
    <div style="margin-bottom:20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Apple_Pay_logo.svg" width="50" style="margin:0 10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" width="50" style="margin:0 10px;">
        <span style="background:white; color:black; padding:3px 10px; border-radius:5px; font-weight:bold; vertical-align:middle;">mada</span>
    </div>
    <p style="color:gray;">جميع الحسابات مضمونة مدى الحياة من DARK STORE ✅</p>
    <p>2026 © جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
