import re
import pandas as pd


def clean_text(text):
    text = re.sub(r'【[^】【]+】', '', text)
    text = re.sub(r'\[[^\]\[]+\]', '', text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    text = re.sub(r'\([^)(]+\)', '', text)
    text = re.sub(r'\（[^）（]+\）', '', text)
    text = re.sub(r"#([^#]+)#", "", text)
    text = re.sub(r"​​​", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"↓↓", "", text)
    text = re.sub(r"(\s)+", r"\1", text)
    link_regex = r'http://t\.cn/[\w]+(,)?(?=[^\w]|,|$)'
    text = re.sub(link_regex, '', text)
    stop_terms = ['展开', '全文', '展开全文', '一个', '网页', '链接', '?【', 'ue627', 'c【', '10', '一下', '一直',
                  'u3000', '24', '12',
                  '30', '?我', '15', '11', '17', '?\\', '显示地图', '原图']
    for x in stop_terms:
        text = text.replace(x, "")
    return text.strip()


if __name__ == '__main__':
    df = pd.read_csv('gqt_output.csv')
    df['content'] = df['content'].apply(clean_text)
    df.to_csv('cleaned_text.csv', index=False)
