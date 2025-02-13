import os
import pandas as pd
from terminal_service import fetch_terminal_times_second
from terminal_service_first import fetch_dates

def check_file_write_permission(file_path):
    """检查文件是否为只读，如果是则提示用户修改为可写"""
    if not os.access(file_path, os.W_OK):  # 使用 os.access 检查写权限
        print(f"文件 '{file_path}' 是只读的，请修改文件属性为非只读模式后重新运行脚本。")
        print("右键单击文件，选择“属性”，取消“只读”选项，然后单击‘确定’。")
        print("程序因此中断，但命令行窗口将保持打开状态。")
        return False  # 返回 False 表示权限问题
    return True  # 返回 True 表示权限正常

def update_excel_with_dates(excel_file):
    if not check_file_write_permission(excel_file):  # 检查文件的写权限
        return  # 如果没有写权限，则终止该文件的处理

    # 读取所有工作表
    all_sheets = pd.read_excel(excel_file, sheet_name=None)
    total_sheets = len(all_sheets)  # 工作表总数
    print(f"文件 '{excel_file}' 包含 {total_sheets} 个工作表。")

    sheet_count = 0  # 已处理工作表计数
    # 遍历每个工作表
    for sheet_name, df in all_sheets.items():
        sheet_count += 1
        print(f"\n正在处理工作表 ({sheet_count}/{total_sheets}): {sheet_name}")
        print("列名: ", df.columns.tolist())

        if '柜号' not in df.columns or '提单号' not in df.columns:
            print(f"跳过工作表: {sheet_name}，因为缺少 '柜号' 或 '提单号' 列")
            continue  # 如果不包含，则跳过这个工作表

        # 确保 '进港时间' 和 '出港时间' 列格式正确
        df['进港时间'] = df['进港时间'].astype(str)
        df['出港时间'] = df['出港时间'].astype(str)

        rows_count = len(df)  # 总行数
        print(f"工作表 '{sheet_name}' 包含 {rows_count} 行数据。")

        # 遍历每一行
        for index, row in df.iterrows():
            # 打印处理进度
            print(f"  正在处理第 {index + 1}/{rows_count} 行...", end="\r")

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

        print(f"\n完成工作表 '{sheet_name}' 的处理。")

        # 保持空列的原始列名，直接写入原始数据
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"已更新写入工作表 '{sheet_name}' 到文件 '{excel_file}'。")

def main():
    # 查找执行目录下的所有 .xlsx 文件
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if not excel_files:
        print("未找到任何 .xlsx 文件，请将文件放置在当前目录后重新运行脚本。")
        return

    print(f"找到 {len(excel_files)} 个文件需要处理：{', '.join(excel_files)}")

    for excel_file in excel_files:
        print(f"\n正在处理文件: {excel_file}")
        update_excel_with_dates(excel_file)
        print(f"完成文件 '{excel_file}' 的处理！")

    print("所有文件处理完成，感谢使用本程序！")
    input("按任意键关闭...")

if __name__ == "__main__":
    main()