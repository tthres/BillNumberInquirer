import os
import pandas as pd
from terminal_service import fetch_terminal_times_second
from terminal_service_first import fetch_dates

def update_excel_with_dates(excel_file):
    # 读取所有工作表
    all_sheets = pd.read_excel(excel_file, sheet_name=None)

    # 遍历每个工作表
    for sheet_name, df in all_sheets.items():
        print(f"处理工作表: {sheet_name}")
        print("列名: ", df.columns.tolist()) 

        if '柜号' not in df.columns or '提单号' not in df.columns:
            print(f"跳过工作表: {sheet_name}，因为缺少 '柜号' 或 '提单号' 列")
            continue  # 如果不包含，则跳过这个工作表

        # 确保 '进港时间' 和 '出港时间' 列格式正确
        df['进港时间'] = df['进港时间'].astype(str)
        df['出港时间'] = df['出港时间'].astype(str)

        # 遍历每一行
        for index, row in df.iterrows():
            # 确保柜号和提单号是字符串类型
            container_no = str(row['柜号']).strip() if pd.notna(row['柜号']) else None
            bill_no = str(row['提单号']).strip() if pd.notna(row['提单号']) else None

            # 确保柜号和提单号都是有效的
            if not container_no or not bill_no:
                print(f"跳过第 {index + 1} 行，缺少柜号或提单号")
                continue

            # 调用 fetch_dates 函数获取到达和离开日期
            in_date, out_date = fetch_dates(container_number=container_no, bill_of_lading=bill_no)
            if not in_date or not out_date:
                in_date, out_date = fetch_terminal_times_second(bill_no, container_no)

            # 更新 DataFrame 中的相应列
            df.at[index, '进港时间'] = str(in_date)  # 确保是字符串类型
            df.at[index, '出港时间'] = str(out_date)  # 确保是字符串类型

        # 保持空列的原始列名，直接写入原始数据
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    # 查找执行目录下的所有.xlsx文件
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    for excel_file in excel_files:
        update_excel_with_dates(excel_file)

if __name__ == "__main__":
    main()
