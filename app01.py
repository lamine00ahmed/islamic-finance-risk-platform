

import streamlit as st

# ============================
# الفرضيات الثلاثة للأوزان
# ============================
hypotheses = {
    "الفرضية 1": {
        "contract_type": 0.20,
        "loan_amount": 0.15,
        "duration": 0.10,
        "profitability": 0.18,
        "cashflow": 0.18,
        "equity_share": 0.05,
        "sector_risk": 0.05,
        "startup_age": 0.03,
        "debt_ratio": 0.06
    },
    "الفرضية 2": {
        "contract_type": 0.10,
        "loan_amount": 0.15,
        "duration": 0.08,
        "profitability": 0.25,
        "cashflow": 0.20,
        "equity_share": 0.05,
        "sector_risk": 0.05,
        "startup_age": 0.05,
        "debt_ratio": 0.07
    },
    "الفرضية 3": {
        "contract_type": 0.08,
        "loan_amount": 0.10,
        "duration": 0.06,
        "profitability": 0.20,
        "cashflow": 0.25,
        "equity_share": 0.05,
        "sector_risk": 0.05,
        "startup_age": 0.05,
        "debt_ratio": 0.15
    }
}

# ============================
# القيم القصوى لكل متغير (Min-Max Scaling)
# ============================
max_values = {
    "contract_type": 4,
    "loan_amount": 100000,
    "duration": 60,
    "profitability": 50000,
    "cashflow": 50000,
    "equity_share": 50000,
    "sector_risk": 10,
    "startup_age": 60,
    "debt_ratio": 50000
}

# ============================
# دالة حساب المخاطر
# ============================
def calculate_risk(weights, contract_type, amount, duration, profit, cashflow, equity, sector, age, debt):
    # تطبيع باستخدام Min-Max
    contract_norm = contract_type / max_values["contract_type"]
    amount_norm = amount / max_values["loan_amount"]
    duration_norm = duration / max_values["duration"]
    profit_norm = profit / max_values["profitability"]
    cashflow_norm = cashflow / max_values["cashflow"]
    equity_norm = equity / max_values["equity_share"]
    sector_norm = sector / max_values["sector_risk"]
    age_norm = age / max_values["startup_age"]
    debt_norm = debt / max_values["debt_ratio"]

    # حساب درجة المخاطر
    risk_score = (
        contract_norm * weights["contract_type"] +
        amount_norm * weights["loan_amount"] +
        duration_norm * weights["duration"] +
        profit_norm * weights["profitability"] +
        cashflow_norm * weights["cashflow"] +
        equity_norm * weights["equity_share"] +
        sector_norm * weights["sector_risk"] +
        age_norm * weights["startup_age"] +
        debt_norm * weights["debt_ratio"]
    )

    # تصنيف المخاطر
    if risk_score < 0.30:
        level = "🔵 منخفض"
    elif risk_score < 0.60:
        level = "🟡 متوسط"
    else:
        level = "🔴 مرتفع"

    return f"درجة المخاطر: {risk_score:.3f}\nالتصنيف: {level}"

# ============================
# ============================
# واجهة Streamlit - العنوان مع خلفية زرقاء فاتحة
# ============================
st.markdown("""
<div style='
    background-color: #ADD8E6;  /* أزرق فاتح */
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: #4B0082;
    font-size: 32px;
    font-weight: bold;
'>
منصة تقييم مخاطر التمويل الإسلامي في الشركات الناشئة
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================
# الشريط الجانبي
# ============================
st.sidebar.header("معلومات المنصة")
st.sidebar.markdown("**البنك:** البنك الأول")
st.sidebar.markdown("**رقم الإصدار:** 0.1.3")
st.sidebar.markdown("---")
st.sidebar.header("اختيار الفرضية")
selected_hypothesis = st.sidebar.radio("اختر الفرضية:", list(hypotheses.keys()))
st.sidebar.markdown("---")
st.sidebar.markdown("**ملاحظات:**")
st.sidebar.markdown(
    "نسخة أولية تجريبية\n"
)
st.sidebar.markdown(
    "المنصة جاهزة للتجربة الأولى لكنها ليست نهائية، مخصصة لاختبار الفكرة والمزايا.\n"
)
# ============================
# الأعمدة للإدخالات
# ============================
col1, col2 = st.columns(2)

with col1:
    contract = st.selectbox("نوع العقد", ["مرابحة", "مشاركة", "مضاربة", "إيجارة"])
    amount = st.number_input("قيمة التمويل (دينار)", step=1000)
    duration = st.number_input("مدة التمويل (شهور)", step=1)
    profit = st.number_input("الأرباح المتوقعة (دينار)", step=1000)
    cashflow = st.number_input("التدفقات النقدية المتوقعة (دينار)", step=1000)

with col2:
    equity = st.number_input("قيمة مساهمة صاحب المشروع (دينار)", step=1000)
    sector = st.slider("مخاطر القطاع", 1, 10)
    age = st.number_input("عمر الشركة (أشهر)", step=1)
    debt = st.number_input("الدين الحالي (دينار)", step=1000)

# تحويل نوع العقد إلى رقم
def convert_contract(x):
    return {"مرابحة":1,"مشاركة":2,"مضاربة":3,"إيجارة":4}[x]

# ============================
# حساب وعرض النتائج
# ============================
if st.button("احسب المخاطر"):
    result = calculate_risk(
        hypotheses[selected_hypothesis],
        convert_contract(contract), amount, duration, profit, cashflow, equity, sector, age, debt
    )
    # تحديد اللون حسب المخاطر
    if "منخفض" in result:
        color = "#00BFFF"
    elif "متوسط" in result:
        color = "#FFA500"
    else:
        color = "#FF0000"

    st.markdown(f"<h3 style='color: {color};'>{result}</h3>", unsafe_allow_html=True)



