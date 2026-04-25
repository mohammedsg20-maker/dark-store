import streamlit as st
import random

# --- 1. التصميم الاحترافي (CSS المطور) ---
st.set_page_config(page_title="DARK STORE | DK", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif; text-align: right; }
    .stApp { background-color: #0b0b0e; color: #ffffff; }
    
    /* الهيدر العلوي */
    .main-header {
        background: #16161a; padding: 20px; border-bottom: 2px solid #8A2BE2;
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 15px 15px; margin-bottom: 30px;
    }
    .dk-logo { background: #8A2BE2; color: #000; padding: 10px 20px; border-radius: 12px; font-weight: 900; font-size: 24px; }
    
    /* كروت المنتجات */
    .game-card {
        background: #1c1c24; border-radius: 20px; padding: 15px;
        border: 1px solid #333; transition: 0.4s;
    }
    .game-card:hover { border-color: #8A2BE2; transform: translateY(-10px); }
    
    /* الفوتر (مثل المواقع العالمية) */
    .footer {
        background: #0d0d0f; padding: 50px 20px; border-top: 1px solid #2d2d35;
        margin-top: 80px; text-align: center;
    }
    .payment-icons img { width: 45px; margin: 0 8px; filter: grayscale(20%); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات (Session State) ---
if 'user' not in st.session_state: st.session_state.user = None
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'currency' not in st.session_state: st.session_state.currency = "SAR"
if 'wallet' not in st.session_state: st.session_state.wallet = 0.0
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "game": "فورت نايت", "title": "حساب OG نادر", "price": 450, "img": "https://img.youtube.com/vi/jS8XU_pG_a0/maxresdefault.jpg"},
        {"id": 2, "game": "روكيت ليق", "title": "حساب تيتانيوم وايت", "price": 130, "img": "https://i.ytimg.com/vi/qY_3m6_7_pE/maxresdefault.jpg"}
    ]

# --- 3. نظام الدخول المتطور (Email) ---
def login_screen():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align:center;'><div class='dk-logo' style='display:inline-block;'>DK</div><h1>DARK STORE</h1></div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["تسجيل دخول", "حساب جديد"])
        with tab1:
            email = st.text_input("البريد الإلكتروني")
            pw = st.text_input("كلمة المرور", type="password")
            if st.button("دخول ✨", use_container_width=True):
                if email == "admin@dk.com" and pw == "BOSS":
                    st.session_state.user, st.session_state.is_admin = "ADMIN", True
                else: st.session_state.user = email
                st.rerun()
            st.divider()
            st.button("🔵 الدخول عبر Google", use_container_width=True)
        with tab2:
            st.text_input("إيميلك")
            if st.button("إرسال كود التحقق 📧"):
                st.info("تم إرسال كود لبريدك")

# --- 4. القائمة الجانبية (الأيقونات والأقسام) ---
def sidebar():
    with st.sidebar:
        st.markdown("<div class='dk-logo' style='text-align:center;'>DK</div>", unsafe_allow_html=True)
        st.write(f"مرحباً: **{st.session_state.user}**")
        
        st.divider()
        st.subheader("☰ الأقسام")
        # اختيار الأقسام بصور حقيقية
        st.markdown("![FN](https://i.imgur.com/vHq0A6r.png) **فورت نايت**", unsafe_allow_html=True)
        fn = st.checkbox("عرض فورت نايت", value=True)
        st.markdown("![RL](https://i.imgur.com/K3pS05M.png) **روكيت ليق**", unsafe_allow_html=True)
        rl = st.checkbox("عرض روكيت ليق", value=True)
        
        st.divider()
        with st.expander("💳 المحفظة والعملة"):
            st.session_state.currency = st.selectbox("العملة", ["SAR", "USD", "EUR"])
            st.write(f"الرصيد: {st.session_state.wallet} {st.session_state.currency}")
            st.button("إضافة بطاقة بنكية")

        if st.session_state.is_admin:
            st.button("🛠️ لوحة القائد", on_click=lambda: st.session_state.update({"view": "admin"}))
            st.button("🏠 عرض المتجر", on_click=lambda: st.session_state.update({"view": "store"}))
        
        if st.button("خروج 🚪"):
            st.session_state.user = None
            st.rerun()

# --- 5. لوحة التحكم (الأدمن) ---
def admin_panel():
    st.header("🛠️ إدارة منتجات DARK STORE")
    with st.form("add_product"):
        t = st.text_input("اسم المنتج")
        p = st.number_input("السعر", min_value=1.0)
        g = st.selectbox("القسم", ["فورت نايت", "روكيت ليق", "ديسكورد"])
        img = st.text_input("رابط الصورة")
        if st.form_submit_button("إضافة للمتجر ✅"):
            st.session_state.inventory.append({"id": random.randint(10,99), "game": g, "title": t, "price": p, "img": img})
            st.rerun()

    st.subheader("📦 إدارة الأسعار والمنتجات")
    for idx, item in enumerate(st.session_state.inventory):
        col1, col2 = st.columns([3, 1])
        item['price'] = col1.number_input(f"سعر {item['title']}", value=float(item['price']), key=f"p_{idx}")
        if col2.button("حذف ❌", key=f"d_{idx}"):
            st.session_state.inventory.pop(idx); st.rerun()

# --- 6. واجهة المتجر والدفع ---
def store_view():
    st.markdown(f"""
    <div class="main-header">
        <div style="font-size:26px; font-weight:bold;">DARK STORE | {st.session_state.currency}</div>
        <div class="dk-logo">DK</div>
    </div>
    """, unsafe_allow_html=True)

    items = st.session_state.inventory
    cols = st.columns(3)
    for idx, item in enumerate(items):
        # تحويل العملة
        price = item['price']
        if st.session_state.currency == "USD": price = round(price / 3.75, 2)
        
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="game-card">
                <img src="{item['img']}" style="width:100%; border-radius:15px; height:160px; object-fit:cover;">
                <h3>{item['title']}</h3>
                <h2 style="color:#8A2BE2;">{price} {st.session_state.currency}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            pay_type = st.selectbox("وسيلة الدفع", ["مدى", "Apple Pay", "VISA"], key=f"pay_{idx}")
            if st.button(f"شراء بـ {pay_type}", key=f"btn_{idx}", use_container_width=True):
                msg = f"طلب شراء من DK STORE%0Aالمنتج: {item['title']}%0Aالسعر: {price}%0Aالدفع: {pay_type}"
                st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/9665XXXXXXXX?text={msg}">', unsafe_allow_html=True)

    # الفوتر (طبق الأصل من الصور)
    st.markdown("""
    <div class="footer">
        <div style="display:flex; justify-content:space-around; flex-wrap:wrap; gap:30px; margin-bottom:40px;">
            <div><h5>خدمة العملاء</h5><p>واتساب 🟢</p></div>
            <div><h5>روابط تهمك</h5><p>الشروط والأحكام | سياسة الحسابات</p></div>
            <div><h5>توثيق المتجر</h5><p>✅ موثق في المركز السعودي للأعمال</p></div>
        </div>
        <div class="payment-icons">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Apple_Pay_logo.svg">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg">
            <span style="background:white; color:black; padding:4px 10px; border-radius:4px; font-weight:bold; font-size:12px;">mada</span>
        </div>
        <p style="color:gray; margin-top:20px;">الحقوق محفوظة لمتجر يووكس | 2026</p>
    </div>
    """, unsafe_allow_html=True)

# --- التشغيل ---
if not st.session_state.user:
    login_screen()
else:
    sidebar()
    if st.session_state.is_admin and st.session_state.get('view') == 'admin':
        admin_panel()
    else:
        store_view()
