#!/usr/bin/env python3
"""测试 Excel 生成功能"""
import os
import csv
from openpyxl import Workbook

def csv_to_excel(csv_path, excel_path):
    """从CSV转换为Excel"""
    try:
        print(f"正在读取 CSV: {csv_path}")
        print(f"CSV 文件存在: {os.path.exists(csv_path)}")
        
        wb = Workbook()
        ws = wb.active
        ws.title = "食谱生成结果"
        
        # 读取CSV并写入Excel
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            row_count = 0
            for row in reader:
                ws.append(row)
                row_count += 1
                if row_count <= 3:
                    print(f"行 {row_count}: {row[:2]}...")  # 只打印前2列
        
        print(f"共读取 {row_count} 行")
        
        # 设置列宽
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['C'].width = 80
        ws.column_dimensions['D'].width = 10
        ws.column_dimensions['E'].width = 20
        
        # 保存文件
        print(f"正在保存 Excel: {excel_path}")
        wb.save(excel_path)
        print(f"✅ Excel 文件已保存到: {excel_path}")
        print(f"Excel 文件大小: {os.path.getsize(excel_path)} 字节")
        return True
    except Exception as e:
        print(f"❌ Excel 文件生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    csv_file = "outputs/recipe_results.csv"
    excel_file = "outputs/recipe_results.xlsx"
    
    print("开始测试 Excel 生成...")
    print("=" * 50)
    csv_to_excel(csv_file, excel_file)
