import json
import csv
import pandas as pd

def json_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file, open(output_file, 'w', encoding='utf-8',
                                                                    newline='') as csv_file:
        writer = csv.writer(csv_file)
        # 写入表头
        writer.writerow(['user_id', 'mblogid', 'created_at', 'reposts_count', 'comments_count', 'attitudes_count',
                         'content', 'pic_urls', 'pic_num', 'isLongText', 'url', 'crawl_time'])

        for line in json_file:
            data = json.loads(line)
            user_id = data['_id']
            mblogid = data['mblogid']
            created_at = data['created_at']
            reposts_count = data['reposts_count']
            comments_count = data['comments_count']
            attitudes_count = data['attitudes_count']
            content = data['content'].replace('\n', ' ')  # 将换行符替换为空格，避免输出时自动换行
            pic_urls = data['pic_urls']
            pic_num = data['pic_num']
            islongtext = data['isLongText']
            url = data['url']
            crawl_time = data['crawl_time']

            writer.writerow([user_id, mblogid, created_at, reposts_count, comments_count, attitudes_count,
                             content, pic_urls, pic_num, islongtext, url, crawl_time])


if __name__ == '__main__':
    json_to_csv('gongqt.json', 'gqt_output.csv')
    df = pd.read_csv('gqt_output.csv')
    total_rows = df.shape[0]
    df.drop_duplicates(inplace=True) #当inplace=True，原数据在操作之后会直接修改
    removed_rows = total_rows - df.shape[0]
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
    df = df.sort_values('created_at', ascending=False)  #ascending=False代表一个字段的排序
    df.to_csv('gqt_output.csv', index=False)
    print(f"删除了 {removed_rows} 行重复数据。")
