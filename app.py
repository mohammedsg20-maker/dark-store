import streamlit as st
import random

# --- 1. إعدادات التصميم والهوية ---
st.set_page_config(page_title="DARK STORE | DK", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background-color: #0b0b0e; color: #ffffff; }
    
    /* الهيدر العلوي */
    .main-header {
        background: #16161a; padding: 20px; border-bottom: 3px solid #8A2BE2;
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 20px 20px; margin-bottom: 30px;
    }
    .dk-logo { background: #8A2BE2; color: #000; padding: 10px 20px; border-radius: 12px; font-weight: 900; font-size: 24px; box-shadow: 0 0 15px #8A2BE2; }
    
    /* كروت المنتجات */
    .product-card {
        background: #1c1c24; border-radius: 15px; padding: 15px;
        border: 1px solid #333; transition: 0.3s; text-align: center;
    }
    .product-card:hover { border-color: #8A2BE2; transform: translateY(-5px); }
    
    /* الفوتر */
    .footer-container {
        background: #09090b; padding: 40px 20px; border-top: 1px solid #222;
        margin-top: 50px; text-align: center;
    }
    .payment-badge img { width: 45px; margin: 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والجلسة (Session State) ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "game": "فورت نايت", "title": "حساب شيطون كامل", "price": 450, "img": "https://img.youtube.com/vi/jS8XU_pG_a0/maxresdefault.jpg"},
        {"id": 2, "game": "روكيت ليق", "title": "حساب وايت زومبا", "price": 130, "img": "https://i.ytimg.com/vi/qY_3m6_7_pE/maxresdefault.jpg"}
    ]

if 'user' not in st.session_state: st.session_state.user = "ضيف"
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'currency' not in st.session_state: st.session_state.currency = "SAR"
if 'view' not in st.session_state: st.session_state.view = "store"

MY_WHATSAPP = "9665XXXXXXXX" # ضع رقمك هنا

# --- 3. القائمة الجانبية (الأقسام + دخول الإدارة) ---
with st.sidebar:
    st.markdown("<div class='dk-logo' style='text-align:center;'>DK</div>", unsafe_allow_html=True)
    st.write(f"👤 مرحباً: **{st.session_state.user}**")
    
    st.divider()
    st.subheader("☰ الأقسام")
    cat = st.radio("اختر القسم:", ["الرئيسية", "⚽ روكيت ليق", "🔫 فورت نايت", "💬 ديسكورد"])
    
    st.divider()
    # نظام دخول الإدارة (القائد)
    if not st.session_state.is_admin:
        with st.expander("🔑 دخول القائد"):
            u = st.text_input("اليوزر")
            p = st.text_input("الباسوورد", type="password")
            if st.button("دخول الإدارة"):
                if u == "admin" and p == "BOSS":
                    st.session_state.is_admin = True
                    st.session_state.user = "القائد 👑"
                    st.rerun()
    else:
        st.success("أهلاً يا BOSS")
        if st.button("🛠️ لوحة التحكم"): st.session_state.view = "admin"
        if st.button("🛒 عرض المتجر"): st.session_state.view = "store"
        if st.button("🚪 خروج"): 
            st.session_state.is_admin = False
            st.session_state.user = "ضيف"
            st.rerun()

# --- 4. لوحة تحكم القائد (تعديل الأسعار والمنتجات) ---
def admin_panel():
    st.header("🛠️ لوحة تحكم DARK STORE")
    with st.form("add_new"):
        st.subheader("➕ إضافة منتج")
        t = st.text_input("اسم المنتج")
        p = st.number_input("السعر", min_value=0.0)
        g = st.selectbox("القسم", ["فورت نايت", "روكيت ليق", "ديسكورد"])
        img = st.text_input("رابط الصورة")
        if st.form_submit_button("حفظ المنتج ✅"):
            st.session_state.inventory.append({"id": random.randint(10,99), "game": g, "title": t, "price": p, "img": img})
            st.rerun()

    st.subheader("📦 إدارة المنتجات الحالية")
    for idx, item in enumerate(st.session_state.inventory):
        c1, c2 = st.columns([3, 1])
        item['price'] = c1.number_input(f"سعر {item['title']}", value=float(item['price']), key=f"p_{idx}")
        if c2.button("حذف ❌", key=f"d_{idx}"):
            st.session_state.inventory.pop(idx); st.rerun()

# --- 5. واجهة المتجر والدفع ---
def store_view(category):
    st.markdown(f"""
    <div class="main-header">
        <div style="font-size:28px; font-weight:bold; color:#8A2BE2;">DARK STORE</div>
        <div>🇸🇦 ريال سعودي</div>
    </div>
    """, unsafe_allow_html=True)

    items = [i for i in st.session_state.inventory if category == "الرئيسية" or i['game'] in category]
    
    cols = st.columns(3)
    for idx, item in enumerate(items):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{item['img']}" style="width:100%; border-radius:10px; height:150px; object-fit:cover;">
                <h3>{item['title']}</h3>
                <h2 style="color:#8A2BE2;">{item['price']} ريال</h2>
            </div>
            """, unsafe_allow_html=True)
            
            method = st.selectbox("الدفع عبر:", ["مدى", "Apple Pay", "VISA"], key=f"m_{idx}")
            if st.button(f"شراء الآن", key=f"b_{idx}", use_container_width=True):
                msg = f"طلب شراء من DK%0Aالمنتج: {item['title']}%0Aالسعر: {item['price']}%0Aالوسيلة: {method}"
                st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/{MY_WHATSAPP}?text={msg}">', unsafe_allow_html=True)

    # الفوتر
    st.markdown("""
    <div class="footer-container">
        <div style="display:flex; justify-content:space-around; flex-wrap:wrap; margin-bottom:30px;">
            <div><h4>خدمة العملاء</h4><p>تواصل عبر الواتساب</p></div>
            <div><h4>روابط تهمك</h4><p>سياسة الحسابات | الشروط</p></div>
            <div><h4>توثيق المتجر</h4><p>✅ موثق في المركز السعودي</p></div>
        </div>
        <div class="payment-badge">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Apple_Pay_logo.svg">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg">
            <span style="background:white; color:black; padding:5px; border-radius:4px; font-weight:bold;">mada</span>
        </div>
        <p style="color:gray; margin-top:20px;">جميع الحقوق محفوظة لمتجر DK © 2026</p>
    </div>
    """, unsafe_allow_html=True)

# --- التشغيل ---
if st.session_state.view == "admin" and st.session_state.is_admin:
    admin_panel()
else:
    store_view(cat)
