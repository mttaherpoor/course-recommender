import re

class TextUtils:

    @staticmethod
    def fa_to_en(text):
        fa = "۰۱۲۳۴۵۶۷۸۹"
        en = "0123456789"
        for f, e in zip(fa, en):
            text = text.replace(f, e)
        return text

    @staticmethod
    def extract_number(text):
        text = TextUtils.fa_to_en(text)
        nums = re.findall(r"[\d.]+", text)
        return float(nums[0]) if nums else 0

    @staticmethod
    def parse_hours_lessons(element):
        from selenium.webdriver.common.by import By

        hours = 0
        lessons = 0

        try:
            meta = element.find_element(
                By.CSS_SELECTOR,
                "div.d-flex.flex-wrap.align-items-center.small.mb-2"
            )
            text = meta.text

            h = re.search(r"([\d.]+)\s*ساعت", text)
            l = re.search(r"([\d,]+)\s*درس", text)

            if h:
                hours = float(TextUtils.fa_to_en(h.group(1)))

            if l:
                lessons = int(TextUtils.fa_to_en(l.group(1)).replace(",", ""))

        except:
            pass

        return hours, lessons
    
    @staticmethod
    def parse_level(element):
        from selenium.webdriver.common.by import By

        try:
            spans = element.find_elements(
                By.CSS_SELECTOR,
                "div.d-flex.flex-wrap.align-items-center.small.mb-2 span"
            )

            for span in spans:
                text = span.text.strip()

                if any(word in text for word in ["مقدماتی", "متوسط", "پیشرفته","همه سطوح"]):
                    return text

        except:
            pass

        return None