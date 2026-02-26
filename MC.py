# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 15:58:18 2026

@author: BusRmutt
"""

import pickle
from streamlit_option_menu import option_menu
import streamlit as st

# Load Models
used_car_model = pickle.load(open('Used_cars_model.sav','rb'))
riding_model = pickle.load(open('RidingMowers_model.sav','rb'))
bmi_model = pickle.load(open('bmi_model.sav','rb'))

# ================== Mapping ==================
fuel_map = {
    'Diesel': 0,
    'Electric': 1,
    'Petrol': 2
}

engine_map = {
    '800': 0,
    '1000': 1,
    '1200': 2,
    '1500': 3,
    '1800': 4,
    '2000': 5,
    '2500': 6,
    '3000': 7,
    '4000': 8,
    '5000': 9
}

brand_map = {
    'BMW': 0,
    'Chevrolet': 1,
    'Ford': 2,
    'Honda': 3,
    'Hyundai': 4,
    'Kia': 5,
    'Nissan': 6,
    'Tesla': 7,
    'Toyota': 8,
    'Volkswagen': 9
}

transmission_map = {
    'Automatic': 0,
    'Manual': 1
}

# ================== Sidebar ==================
with st.sidebar:
    selected = option_menu(
        'Prediction',
        ['Ridingmower','Used_cars','bmi']
    )

# ================== Riding Mower ==================
if selected == 'Ridingmower':
    st.title('Riding Mower Classification')

    Income = st.text_input('Income')
    LotSize = st.text_input('LotSize')

    if st.button('Predict'):
        prediction = riding_model.predict([[
            float(Income),
            float(LotSize)
        ]])

        if prediction[0] == 1:
            st.success('Owner')
        else:
            st.success('Non Owner')

# ================== Used Cars ==================
elif selected == 'Used_cars':
    st.title('ประเมินราคารถมือ 2')

    make_year = st.text_input('ปีที่ผลิต')
    mileage_kmpl = st.text_input('กินน้ำมันกี่ KM/L')
    engine_cc = st.selectbox('ขนาดเครื่องยนต์ (CC)', list(engine_map.keys()))
    fuel_type = st.selectbox('ประเภทน้ำมัน', list(fuel_map.keys()))
    owner_count = st.text_input('จำนวนเจ้าของเดิม')
    brand = st.selectbox('ยี่ห้อรถ', list(brand_map.keys()))
    transmission = st.selectbox('ประเภทเกียร์', list(transmission_map.keys()))
    accidents_reported = st.text_input('จำนวนอุบัติเหตุที่เคยเกิด')

    if st.button('Predict'):
        prediction = used_car_model.predict([[
            float(make_year),
            float(mileage_kmpl),
            engine_map[engine_cc],
            fuel_map[fuel_type],
            float(owner_count),
            brand_map[brand],
            transmission_map[transmission],
            float(accidents_reported)
        ]])

        st.success(f"ราคาประเมิน: {round(prediction[0],2)} บาท")

# ================== BMI ==================
elif selected == 'bmi':
    st.title('🏥 ระบบประเมินภาวะ BMI')
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox('เพศ', ['Female','Male'])
        height = st.number_input('ส่วนสูง (cm)', min_value=100.0, max_value=250.0)
    
    with col2:
        weight = st.number_input('น้ำหนัก (kg)', min_value=20.0, max_value=300.0)

    if st.button('🔍 ประเมินผล'):

        try:
            # -------------------------
            # คำนวณ BMI จริง
            # -------------------------
            height_m = height / 100
            bmi_value = weight / (height_m ** 2)

            # -------------------------
            # encode gender เหมือนตอน train
            # -------------------------
            gender_value = 0 if gender == 'Female' else 1

            prediction = bmi_model.predict([[
                gender_value,
                float(height),
                float(weight)
            ]])

            bmi_class = prediction[0]

            # -------------------------
            # Mapping ผลลัพธ์
            # -------------------------
            bmi_result_map = {
                0: ("ผอมมาก", "ควรพบแพทย์เพื่อประเมินภาวะโภชนาการ"),
                1: ("ผอม", "ควรเพิ่มสารอาหารให้เพียงพอ"),
                2: ("ปกติ", "รักษาสุขภาพให้ดีแบบนี้ต่อไป"),
                3: ("น้ำหนักเกิน", "ควรควบคุมอาหารและออกกำลังกาย"),
                4: ("โรคอ้วน", "เสี่ยงต่อโรคเบาหวานและความดันสูง"),
                5: ("โรคอ้วนรุนแรง", "ควรปรึกษาแพทย์โดยด่วน")
            }

            result_text, advice = bmi_result_map.get(bmi_class, ("ไม่ทราบผล", ""))

            st.markdown("---")
            st.subheader("📊 ผลการวิเคราะห์")

            # -------------------------
            # แสดงค่า BMI ตัวใหญ่
            # -------------------------
            st.metric("ค่า BMI ของคุณ", round(bmi_value, 2))

            # -------------------------
            # แสดงผลตามระดับความเสี่ยง
            # -------------------------
            if bmi_class >= 4:
                st.error(f"🚨 ภาวะ: {result_text}")
            elif bmi_class == 3:
                st.warning(f"⚠️ ภาวะ: {result_text}")
            else:
                st.success(f"✅ ภาวะ: {result_text}")

            # -------------------------
            # คำแนะนำ
            # -------------------------
            st.info(f"💡 คำแนะนำ: {advice}")

        except:
            st.error("กรุณากรอกข้อมูลให้ถูกต้อง")
