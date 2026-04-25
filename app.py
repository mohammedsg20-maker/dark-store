import streamlit as st
import random

# --- 1. إعدادات الهوية والتصميم ---
st.set_page_config(page_title="DARK STORE | DK", layout="wide")

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
    
    /* الزر السري للوقو */
    .dk-logo { 
        background: #8A2BE2; color: #000; padding: 10px 20px; 
        border-radius: 12px; font-weight: 900; font-size: 22px;
        cursor: pointer; border: none; box-shadow: 0 0 10px #8A2BE2;
    }
    
    /* كروت المنتجات */
    .product-card {
        background: #1c1c24; border-radius: 15px; padding: 15px;
        border: 1px solid #333; text-align: center; transition: 0.3s;
    }
    .product-card:hover { border-color: #8A2BE2; transform: translateY(-5px); }
    
    /* صندوق الدفع ببرق */
    .payment-box {
        background: #16161a; border: 2px dashed #8A2BE2;
        padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والجلسة ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 1, "game": "فورت نايت", "title": "حساب شيطون كامل", "price": 450, "img": "https://img.youtube.com/vi/jS8XU_pG_a0/maxresdefault.jpg"},
        {"id": 2, "game": "روكيت ليق", "title": "حساب وايت زومبا", "price": 130, "img": "https://i.ytimg.com/vi/qY_3m6_7_pE/maxresdefault.jpg"}
    ]

if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'admin_clicks' not in st.session_state: st.session_state.admin_clicks = 0
if 'currency' not in st.session_state: st.session_state.currency = "SAR"
if 'barq_info' not in st.session_state: st.session_state.barq_info = "سيتم تزويدك برابط الدفع عند الشراء"

MY_WHATSAPP = "9665XXXXXXXX" # حط رقمك هنا

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#8A2BE2;'>القائمة</h2>", unsafe_allow_html=True)
    cat = st.radio("اختر القسم:", ["الرئيسية", "⚽ روكيت ليق", "🔫 فورت نايت", "💬 ديسكورد"])
    
    st.divider()
    st.session_state.currency = st.selectbox("العملة", ["SAR", "USD"])
    
    if st.session_state.is_admin:
        st.success("وضع القائد مفعل 👑")
        if st.button("🛠️ لوحة التحكم"): st.session_state.view = "admin"
        if st.button("🛒 المتجر"): st.session_state.view = "store"
        if st.button("🚪 خروج"):
            st.session_state.is_admin = False
            st.session_state.admin_clicks = 0
            st.rerun()

# --- 4. لوحة التحكم السرية (تفتح بـ 5 ضغطات على اللوقو) ---
def admin_panel():
    st.header("🛠️ لوحة تحكم القائد")
    
    # إعدادات بطاقة برق
    st.subheader("💳 إعدادات الدفع (برق / Barq)")
    st.session_state.barq_info = st.text_area("أدخل رقم الآيبان أو رابط طلب الدفع الخاص بك:", st.session_state.barq_info)
    
    st.divider()
    # إضافة منتجات
    with st.form("add_item"):
        st.subheader("➕ إضافة حساب جديد")
        t = st.text_input("اسم الحساب")
        p = st.number_input("السعر بالريال")
        g = st.selectbox("القسم", ["فورت نايت", "روكيت ليق", "ديسكورد"])
        img = st.text_input("رابط الصورة المباشر")
        if st.form_submit_button("حفظ"):
            st.session_state.inventory.append({"id": random.randint(10,99), "game": g, "title": t, "price": p, "img": img})
            st.rerun()

    # تعديل المنتجات الحالية
    st.subheader("📦 إدارة المخزون")
    for idx, item in enumerate(st.session_state.inventory):
        col1, col2 = st.columns([3, 1])
        item['price'] = col1.number_input(f"سعر {item['title']}", value=float(item['price']), key=f"edit_p_{idx}")
        if col2.button("حذف ❌", key=f"del_{idx}"):
            st.session_state.inventory.pop(idx); st.rerun()

# --- 5. واجهة المتجر والدفع الآلي ---
def store_view(category):
    # الهيدر مع الزر السري
    col_h1, col_h2 = st.columns([5, 1])
    with col_h1:
        st.markdown(f"<h1 style='margin-top:10px;'>🌌 DARK STORE | {st.session_state.currency}</h1>", unsafe_allow_html=True)
    with col_h2:
        if st.button("DK", key="secret_dk_btn"):
            st.session_state.admin_clicks += 1
            if st.session_state.admin_clicks >= 5:
                # إظهار فورم الدخول عند الوصول لـ 5 ضغطات
                st.session_state.show_login = True
    
    # فورم الدخول السري
    if st.session_state.get('show_login') and not st.session_state.is_admin:
        with st.form("admin_login"):
            u = st.text_input("يوزر القائد")
            p = st.text_input("باسورد القائد", type="password")
            if st.form_submit_button("دخول"):
                if u == "admin" and p == "BOSS":
                    st.session_state.is_admin = True
                    st.session_state.show_login = False
                    st.rerun()
                else: st.error("خطأ!")

    # عرض المنتجات
    items = [i for i in st.session_state.inventory if category == "الرئيسية" or i['game'] in category]
    cols = st.columns(3)
    for idx, item in enumerate(items):
        # تحويل السعر للدولار لو اختار العميل
        p_display = item['price']
        if st.session_state.currency == "USD": p_display = round(item['price'] / 3.75, 2)
        
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{item['img']}" style="width:100%; border-radius:10px; height:150px; object-fit:cover;">
                <h3>{item['title']}</h3>
                <h2 style="color:#8A2BE2;">{p_display} {st.session_state.currency}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"شراء {item['title']}", key=f"buy_{idx}", use_container_width=True):
                st.session_state.active_buy = item
                st.rerun()

    # نافذة الدفع (برق)
    if 'active_buy' in st.session_state:
        st.markdown(f"""
        <div class="payment-box">
            <h3>💳 إتمام الدفع عبر برق (Barq)</h3>
            <p>لشراء: <b>{st.session_state.active_buy['title']}</b></p>
            <p>حول المبلغ ({st.session_state.active_buy['price']} ريال) إلى الحساب التالي:</p>
            <div style="background:#262730; padding:15px; border-radius:10px; color:#8A2BE2; font-size:18px; font-weight:bold;">
                {st.session_state.barq_info}
            </div>
            <p style="margin-top:10px; font-size:14px; color:gray;">بعد التحويل، اضغط الزر لإرسال إيصال الدفع للقائد</p>
        </div>
        """, unsafe_allow_html=True)
        
        wa_msg = f"تم تحويل المبلغ لحسابك في برق لشراء {st.session_state.active_buy['title']}. مرفق إيصال الدفع:"
        if st.button("إرسال الإيصال عبر واتساب ✅", use_container_width=True):
            st.markdown(f'<meta http-equiv="refresh" content="0;url=https://wa.me/{MY_WHATSAPP}?text={wa_msg}">', unsafe_allow_html=True)

    # الفوتر
    st.markdown("""
    <div style="text-align:center; margin-top:50px; padding:30px; border-top:1px solid #222;">
        <div style="margin-bottom:15px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Apple_Pay_logo.svg" width="40">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" width="40">
            <span style="background:white; color:black; padding:2px 8px; border-radius:4px; font-weight:bold; margin-left:10px;">mada</span>
        </div>
        <p>✅ متجر موثق | جميع الحقوق محفوظة لـ DK 2026</p>
    </div>
    """, unsafe_allow_html=True)

# --- التشغيل ---
if st.session_state.is_admin and st.session_state.get('view') == 'admin':
    admin_panel()
else:
    store_view(cat)
