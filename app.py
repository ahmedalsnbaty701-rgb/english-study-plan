import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="خطة الإنجليزي", page_icon="📘", layout="centered")
FILE=Path("english_progress.json")
DEFAULT=[{"name":f"المحاضرة {i}","parts":3} for i in range(1,18)]

def load():
    try:
        x=json.loads(FILE.read_text(encoding="utf-8"))
        if isinstance(x,dict): return x
    except (OSError,ValueError): pass
    return {"old":DEFAULT.copy(),"new":[],"done":{}}

if "data" not in st.session_state: st.session_state.data=load()
d=st.session_state.data
d.setdefault("old",DEFAULT.copy()); d.setdefault("new",[]); d.setdefault("done",{})

st.markdown("""
<style>
.stApp{direction:rtl}
h1,h2,h3,p,label,div{text-align:right}
.block-container{max-width:850px;padding-top:1.4rem}
.hero{background:linear-gradient(135deg,#172554,#155e75);padding:1rem;border-radius:16px;color:white}
.hero h1,.hero p{color:white;text-align:right}
</style>
""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>📘 خطة لمّ متراكم الإنجليزي</h1><p>الجديد نتابعه أولًا، والقديم نقلّله بالتدريج — من غير ساعات إجبارية.</p></div>',unsafe_allow_html=True)
st.info("كل محاضرة من 3 إلى 5 أجزاء. وقت مذاكرتك الفعلي للجزء تقديريًا 2.5–3 ساعات، ويمكن تقسيمه على جلسات.")
def k(t,i,p): return f"{t}_{i}_{p}"
def stats():
    total=done=0
    for t in ("old","new"):
        for i,l in enumerate(d[t]):
            for p in range(int(l["parts"])):
                total+=1
                done+=bool(d["done"].get(k(t,i,p),False))
    return done,total
done,total=stats()
a,b=st.columns(2)
a.metric("الأجزاء المكتملة",f"{done} / {total}")
b.metric("نسبة الإنجاز",f"{round(done*100/total) if total else 0}%")
st.progress(done/total if total else 0)

st.header("🟠 المسار الأول: المحاضرات القديمة — 17 محاضرة")
st.caption("مش لازم تخلص محاضرة كاملة في يوم. خُد جزءًا، وكمّل باقي موادك، وارجع للجزء التالي.")
for i,l in enumerate(d["old"]):
    finished=sum(bool(d["done"].get(k("old",i,p),False)) for p in range(l["parts"]))
    with st.expander(f'{l["name"]} — {finished}/{l["parts"]} أجزاء',expanded=(i==0)):
        n=st.selectbox("عدد الأجزاء",[3,4,5],index=[3,4,5].index(int(l["parts"])),key=f"oldn{i}")
        if n!=l["parts"]:
            l["parts"]=n
            st.rerun()
        for p in range(l["parts"]):
            kk=k("old",i,p)
            d["done"][kk]=st.checkbox(f"الجزء {p+1} — 2.5 إلى 3 ساعات مذاكرة فعلية (على فترات)",value=bool(d["done"].get(kk,False)),key=f"oldc{i}_{p}")

st.header("🟢 المسار الثاني: المحاضرات الجديدة")
st.caption("أضف أي محاضرة جديدة فور نزولها حتى لا تتحول إلى متراكم.")
with st.form("add",clear_on_submit=True):
    name=st.text_input("اسم المحاضرة الجديدة",placeholder="مثال: المحاضرة الجديدة الأولى")
    parts=st.selectbox("عدد الأجزاء",[3,4,5])
    submit=st.form_submit_button("➕ إضافة المحاضرة")
    if submit:
        if name.strip():
            d["new"].append({"name":name.strip(),"parts":parts})
            st.rerun()
        else: st.warning("اكتب اسم المحاضرة.")
for i,l in enumerate(d["new"]):
    finished=sum(bool(d["done"].get(k("new",i,p),False)) for p in range(l["parts"]))
    with st.expander(f'{l["name"]} — {finished}/{l["parts"]} أجزاء'):
        n=st.selectbox("عدد الأجزاء",[3,4,5],index=[3,4,5].index(int(l["parts"])),key=f"newn{i}")
        if n!=l["parts]:
            l["parts"]=n
            st.rerun()
        for p in range(l["parts"]):
            kk=k("new",i,p)
            d["done"][kk]=st.checkbox(f"الجزء {p+1} — 2.5 إلى 3 ساعات مذاكرة فعلية (على فترات)",value=bool(d["done"].get(kk,False)),key=f"newc{i}_{p}")

st.markdown("---")
st.subheader("🧭 طريقة استخدام الخطة")
st.write("١. تابع المحاضرة الجديدة أول ما تنزل.")
st.write("٢. اشتغل على القديم بالتوازي، من غير عدد ساعات يومي ثابت.")
st.write("٣. الجزء ممكن يتقسم على أكثر من جلسة؛ علّم عليه بعد إتمامه.")
st.write("٤. لو خلصت الجزء، انتقل لمادة ثانية. ولو ما خلصتوش، كمّله لاحقًا.")
if st.button("حفظ التقدم الآن"):
    try:
        FILE.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
        st.success("تم حفظ التقدم في ملف التشغيل الحالي.")
    except OSError: st.error("تعذر حفظ التقدم.")
if st.button("إعادة ضبط علامات الإنجاز",type="secondary"):
    d["done"]={}
    st.rerun()
st.caption("تنبيه: حفظ JSON مناسب للتشغيل المحلي. الاستضافة المجانية قد لا تحتفظ بالملف بعد إعادة التشغيل أو إعادة النشر.")
