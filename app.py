import streamlit as st
import pandas as pd
import random

# --- 1. إعدادات التصميم والهوية (DK) ---
st.set_page_config(page_title="DARK STORE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0b0e; color: #ffffff; }
    .header-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 30px; background: #16161a; border-bottom: 2px solid #8A2BE2;
        border-radius: 12px; margin-bottom: 25px;
    }
    .logo-dk {
        background: #8A2BE2; color: #000; padding: 5px 12px; 
        border-radius: 8px; font-weight: 900; font-size: 24px;
        box-shadow: 0 0 15px #8A2BE2;
    }
    .product-card {
        background: #16161a; border: 1px solid #2d2d35; border-radius: 15px;
        padding: 15px; text-align: center; margin-bottom: 15px;
    }
    .whatsapp-btn {
        background-color: #25d366; color: white; padding: 12px; 
        border-radius: 10px; text-decoration: none; font-weight: bold; 
        display: block; text-align: center; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات (الأدمن والمخزن) ---
# هنا حددنا 2 أدمن برموز سرية مختلفة
ADMIN_KEYS = {
    "admin1": "DARK_BOSS_99", 
    "admin2": "KH_PARTNER_2026"
}

if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "game": "فورت نايت", "title": "حساب بنت الطيارة OG", "price": 450, "img": "https://i.ytimg.com/vi/sS_Xm-F4lZ8/maxresdefault.jpg"},
        {"id": 2, "game": "روكيت ليق", "title": "حساب جراند شامبيون", "price": 130, "img": "https://rocketleague.media.zestyio.com/rl_cross-play_asset_p9_16by9.jpg"}
    ]

if 'cart' not in st.session_state: st.session_state.cart = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'verifying' not in st.session_state: st.session_state.verifying = False
if 'sent_code' not in st.session_state: st.session_state.sent_code = None
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'view' not in st.session_state: st.session_state.view = "store"

MY_WHATSAPP = "9665XXXXXXXX" 

# --- 3. نظام الدخول المتطور (مستخدمين لا محدود + 2 أدمن) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🌌 DARK STORE LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        if not st.session_state.verifying:
            phone_input = st.text_input("رقم الجوال (05xxxxxxx)")
            admin_key_input = st.text_input("رمز الإدارة (اختياري للأدمن)", type="password")
            
            if st.button("دخول / إرسال الكود"):
                # التحقق إذا كان الداخل أحد الأدمين الاثنين
                if admin_key_input in ADMIN_KEYS.values():
                    st.session_state.is_admin = True
                    st.session_state.logged_in = True
                    st.session_state.user_phone = "BOSS 👑"
                    st.rerun()
                # التحقق إذا كان مستخدم عادي برقم سعودي
                elif phone_input.startswith("05") and len(phone_input) == 10:
                    st.session_state.sent_code = str(random.randint(1000, 9999))
                    st.session_state.verifying = True
                    st.session_state.user_phone = phone_input
                    st.rerun()
                else:
                    st.error("تأكد من الرقم (05) أو رمز الإدارة")
        else:
            st.success(f"📩 كود التحقق المرسل للمستخدم: {st.session_state.sent_code}")
            input_code = st.text_input("أدخل كود التحقق")
            if st.button("تأكيد الدخول ✅"):
                if input_code == st.session_state.sent_code:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("الكود خطأ!")
    st.stop()

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown(f"<div class='logo-dk' style='text-align:center;'>DK</div>", unsafe_allow_html=True)
    st.title("القائمة")
    st.write(f"👤 متصل الآن: {st.session_state.user_phone}")
    
    # خيارات الأدمن
    if st.session_state.is_admin:
        st.divider()
        st.subheader("🛠️ أدوات القائد")
        if st.button("⚙️ تعديل المنتجات"):
            st.session_state.view = "admin"
            st.rerun()
        if st.button("🛒 عرض المتجر"):
            st.session_state.view = "store"
            st.rerun()
    
    st.divider()
    page_select = st.radio("الأقسام:", ["الرئيسية", "فورت نايت", "روكيت ليق", "ديسكورد"])
    
    if st.button("تسجيل الخروج 🚪"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.verifying = False
        st.rerun()

# --- 5. واجهة تعديل المنتجات (للأدمن فقط) ---
def admin_panel():
    st.header("🛠️ لوحة تعديل المتجر")
    with st.expander("➕ إضافة منتج جديد لمتجرك"):
        with st.form("new_product"):
            g = st.selectbox("القسم", ["فورت نايت", "روكيت ليق", "ديسكورد"])
            t = st.text_input("اسم المنتج")
            p = st.number_input("السعر بالريال", min_value=0)
            img_url = st.text_input("رابط صورة المنتج")
            if st.form_submit_button("إضافة الآن"):
                st.session_state.inventory.append({"id": random.randint(100, 999), "game": g, "title": t, "price": p, "img": img_url})
                st.success("تمت الإضافة بنجاح!")
                st.rerun()

    st.subheader("📦 إدارة المنتجات الحالية")
    for idx, item in enumerate(st.session_state.inventory):
        with st.expander(f"تعديل: {item['title']}"):
            item['title'] = st.text_input("تغيير الاسم", item['title'], key=f"title_{idx}")
            item['price'] = st.number_input("تغيير السعر", item['price'], key=f"price_{idx}")
            item['img'] = st.text_input("تغيير رابط الصورة", item['img'], key=f"img_{idx}")
            if st.button(f"حذف هذا المنتج ❌", key=f"del_{idx}"):
                st.session_state.inventory.pop(idx)
                st.rerun()

# --- 6. واجهة المتجر (للكل) ---
def main_store(category):
    st.markdown(f"""
    <div class="header-bar">
        <div style="display:flex; align-items:center; gap:10px;">
            <div class="logo-dk">DK</div>
            <div style="font-size: 24px; font-weight: bold; color: #8A2BE2;">DARK STORE</div>
        </div>
        <div style="font-size: 16px;">🛒 ({len(st.session_state.cart)}) | 👤 حسابي</div>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_cart = st.columns([3, 1])

    with col_main:
        filtered_items = [i for i in st.session_state.inventory if category == "الرئيسية" or i['game'] == category]
        cols = st.columns(2)
        for idx, item in enumerate(filtered_items):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{item['img']}" style="width:100%; height:180px; object-fit:cover; border-radius:10px;">
                        <h4>{item['title']}</h4>
                        <p style="color:#8A2BE2; font-size:20px; font-weight:bold;">{item['price']} ريال</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"أضف للسلة 🛒", key=f"btn_{item['id']}"):
                    st.session_state.cart.append(item)
                    st.toast("تمت الإضافة!")

    with col_cart:
        st.subheader("🛒 السلة")
        total_sum = 0
        if not st.session_state.cart:
            st.info("سلتك فارغة")
        else:
            for i, c_item in enumerate(st.session_state.cart):
                st.write(f"**{c_item['title']}** ({c_item['price']} ريال)")
                if st.button("حذف ❌", key=f"rm_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
                total_sum += c_item['price']
            st.divider()
            st.markdown(f"### المجموع: {total_sum} ريال")
            st.markdown(f'<a href="https://wa.me/{MY_WHATSAPP}?text=أرغب+بشراء+منتجات" class="whatsapp-btn">إتمام الطلب 💬</a>', unsafe_allow_html=True)

# --- التشغيل ---
if st.session_state.view == "admin" and st.session_state.is_admin:
    admin_panel()
else:
    main_store(page_select)