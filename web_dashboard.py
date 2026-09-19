#!/usr/bin/env python3
"""
多机器人系统 - Streamlit Web 仪表板
统一入口，可视化管理和对话所有机器人
"""

import streamlit as st
import requests
import json

st.set_page_config(page_title="多机器人 AI 系统", page_icon="🤖", layout="wide")

MANAGER_URL = "http://localhost:5000"

BOT_ENDPOINTS = {
    "总结助手": {"port": 8006, "path": "/summarize", "field": "text"},
    "法律顾问": {"port": 8007, "path": "/analyze", "field": "text"},
    "医疗健康助手": {"port": 8008, "path": "/symptom", "field": "symptom"},
    "财务顾问": {"port": 8009, "path": "/budget", "field": None},
}

st.title("🤖 多机器人 AI 系统")
st.caption("统一管理和对话界面")

# 侧边栏：系统状态
with st.sidebar:
    st.header("📊 系统状态")
    if st.button("🔄 刷新状态"):
        st.rerun()

    try:
        resp = requests.get(f"{MANAGER_URL}/status", timeout=2)
        data = resp.json()
        st.success(f"管理中心在线 ({data['timestamp']})")
        for bot_id, info in data["bots"].items():
            icon = "🟢" if info["status"] == "running" else "🔴"
            st.write(f"{icon} {info['name']} (:{info['port']})")
    except Exception as e:
        st.error(f"管理中心离线: {e}")

# 主区域：Tab 切换不同机器人
tab1, tab2, tab3, tab4 = st.tabs(["📝 总结助手", "⚖️ 法律顾问", "🏥 医疗助手", "💰 财务顾问"])

with tab1:
    st.subheader("文本总结")
    text = st.text_area("输入要总结的文本", height=150, key="summarize_input")
    if st.button("生成摘要", key="btn_summarize"):
        try:
            resp = requests.post(
                "http://localhost:8006/summarize",
                json={"text": text}, timeout=5
            )
            st.json(resp.json())
        except Exception as e:
            st.error(f"请求失败: {e}")

with tab2:
    st.subheader("合同/文本法律分析")
    text = st.text_area("粘贴需要分析的合同或法律文本", height=150, key="legal_input")
    if st.button("分析", key="btn_legal"):
        try:
            resp = requests.post(
                "http://localhost:8007/analyze",
                json={"text": text}, timeout=5
            )
            st.json(resp.json())
        except Exception as e:
            st.error(f"请求失败: {e}")

with tab3:
    st.subheader("症状咨询")
    symptom = st.text_input("描述你的症状", key="medical_input")
    if st.button("查询", key="btn_medical"):
        try:
            resp = requests.post(
                "http://localhost:8008/symptom",
                json={"symptom": symptom}, timeout=5
            )
            st.json(resp.json())
        except Exception as e:
            st.error(f"请求失败: {e}")
    st.warning("⚠️ 仅供参考，不能替代专业医疗诊断")

with tab4:
    st.subheader("预算分析")
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("月收入", min_value=0.0, step=100.0)
    with col2:
        expenses = st.number_input("月支出", min_value=0.0, step=100.0)
    if st.button("分析预算", key="btn_finance"):
        try:
            resp = requests.post(
                "http://localhost:8009/budget",
                json={"income": income, "expenses": expenses}, timeout=5
            )
            st.json(resp.json())
        except Exception as e:
            st.error(f"请求失败: {e}")

st.divider()
st.caption("多机器人系统 · Linux + Windows 双网关 · Kubernetes 就绪")
