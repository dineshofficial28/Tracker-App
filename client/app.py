import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_tasks, add_task, update_task

# Page Config
st.set_page_config(page_title="Task Tracker", layout="wide", page_icon="📝")

# Title and Header
st.markdown(
    "<h1 style='text-align:center; color: #4CAF50;'>📝 Tracker App</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# Sidebar: Add New Task
st.sidebar.header("➕ Add New Task")
with st.sidebar.form("add_task_form"):
    title = st.text_input("Task Title")
    description = st.text_area("Description")
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
    submitted = st.form_submit_button("Add Task")
    if submitted and title:
        tasks = get_tasks()
        new_task = {
            "id": max([t["id"] for t in tasks], default=0) + 1,
            "title": title,
            "description": description,
            "frequency": frequency,
            "completed": False
        }
        if add_task(new_task):
            st.success(f"Task '{title}' added successfully!")
        else:
            st.error("Failed to add task")

st.markdown("---")

# Load tasks
tasks = get_tasks()

# Columns Layout
col1, col2 = st.columns([3,2])

# Left Column: Tasks List
with col1:
    st.subheader("📋 Your Tasks")
    if not tasks:
        st.info("No tasks found. Add tasks from the sidebar!")
    else:
        # Iterate tasks
        for t in tasks:
            card_bg = "#192D1B" if t["completed"] else "#381919"
            st.markdown(
                f"""
                <div style="background-color:{card_bg}; padding:10px; margin-bottom:10px; border-radius:10px;">
                    <h4>{t['title']} {'✅' if t['completed'] else '❌'}</h4>
                    <p>{t['description']}</p>
                    <small>Frequency: {t['frequency']}</small>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Complete Button
            if not t["completed"]:
                if st.button(f"Mark Complete", key=t["id"]):
                    t["completed"] = True
                    update_task(t["id"], t)
                    # Reload tasks immediately
                    tasks = get_tasks()
                    st.experimental_rerun = None  # removed call completely

# Right Column: Progress Visualization
with col2:
    st.subheader("📊 Progress Dashboard")
    if tasks:
        df = pd.DataFrame(tasks)
        completed_count = df['completed'].sum()
        pending_count = len(df) - completed_count

        # Pie Chart for Completed vs Pending
        fig, ax = plt.subplots()
        ax.pie([completed_count, pending_count], labels=["Completed", "Pending"],
               autopct='%1.1f%%', colors=['#4CAF50','#FF4C4C'], startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Frequency Bar Chart
        freq_chart = df.groupby(['frequency','completed']).size().reset_index(name='count')
        # Color mapping: Completed green, Pending red
        status_color = {True:'#4CAF50', False:'#FF4C4C'}
        fig2, ax2 = plt.subplots()
        for status in [True, False]:
            data = freq_chart[freq_chart['completed'] == status]
            ax2.bar(data['frequency'], data['count'], 
                    color=status_color[status], label='Completed' if status else 'Pending', alpha=0.7)
        ax2.set_ylabel("Task Count")
        ax2.set_title("Tasks by Frequency & Status")
        ax2.legend()
        st.pyplot(fig2)
