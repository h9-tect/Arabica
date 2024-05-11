import streamlit as st
import logging
import os
from octopus import octopus  # This should match your import statement for the octopus library

# Initialize logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
)
logger = logging.getLogger("octopus")

# Initialize the Octopus object with a cache directory
cache_dir = "./octopus_cache/"
oct_obj = octopus.octopus(logger, cache_dir)  # Adjust based on your library's structure

# Streamlit layout setup
st.title('🐙 أداة توليد اللغة العربية')

st.markdown("""
اختر المهمة من القائمة، اكتب نصك في المساحة المخصصة، ثم اضغط على **معالجة** لرؤية النتيجة.
""", unsafe_allow_html=True)

task = st.selectbox(
    'اختر المهمة:',
    [
        'تشكيل النص',
        'التصحيح النحوي',
        'توليد العناوين',
        'إعاده الصياغه',
        'الإجابة على الأسئلة',
        'توليد الأسئلة',
        'الترجمة'
    ],
    index=0
)

input_text = st.text_area("أدخل النص هنا:", height=150)

task_prefix_map = {
    'تشكيل النص': "diacritize",
    'التصحيح النحوي': "correct_grammar",
    'توليد العناوين': "generate_title",
    'إعاده الصياغه': "paraphrase",
    'الإجابة على الأسئلة': "answer_question",
    'توليد الأسئلة': "generate_question",
    'الترجمة': "transliterate"  # Make sure this is correct
}

if st.button('معالجة'):
    with st.spinner('جارٍ معالجة النص...'):
        prefix = task_prefix_map[task]
        text_with_prefix = f"{prefix}: {input_text}"
        gen_options = {"search_method": "beam", "seq_length": 300, "num_beams": 5, "no_repeat_ngram_size": 2, "max_outputs": 1}
        output = oct_obj.do_generate(text_with_prefix, **gen_options)
        st.text_area("النتيجة:", output, height=300)

st.sidebar.header("معلومات")
st.sidebar.info("هذه الأداة مصممة لتوفير وظائف متقدمة لمعالجة اللغة العربية باستخدام مكتبة الأخطبوط.")
