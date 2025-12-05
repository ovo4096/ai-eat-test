#!/usr/bin/env python3
"""
批量测试食谱生成
读取 test_menu_name.txt 中的食谱名称，调用 Ark API 生成食谱，并保存到 Excel 和 CSV
支持中断恢复功能
"""
import os
import time
import csv
from datetime import datetime
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark
import openpyxl
from openpyxl import Workbook

# 加载环境变量
load_dotenv()


def read_menu_names(file_path, limit=None):
    """读取食谱名称列表"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if limit:
        lines = lines[:limit]
    
    return lines


def get_completed_menus(csv_path):
    """从CSV文件中读取已完成的食谱名称"""
    completed = set()
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('状态') == 'success':
                        completed.add(row.get('食谱名', ''))
        except Exception as e:
            print(f"⚠️ 读取已完成记录时出错: {e}")
    return completed


def save_to_csv(result, csv_path, is_new_file=False):
    """逐条保存结果到CSV"""
    fieldnames = ['食谱名', 'AI思考过程', 'AI结果', '状态', '请求耗时(秒)']
    
    mode = 'w' if is_new_file else 'a'
    with open(csv_path, mode, encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if is_new_file:
            writer.writeheader()
        
        writer.writerow({
            '食谱名': result['menu_name'],
            'AI思考过程': result['thinking'],
            'AI结果': result['result'],
            '状态': result['status'],
            '请求耗时(秒)': result['request_time']
        })


def generate_recipe(client, menu_name):
    """调用 API 生成食谱"""
    # 从环境变量读取提示词模板，如果没有则使用默认值
    prompt_template = os.getenv(
        'RECIPE_PROMPT',
        '请生成3天的{menu_name}，每天至少包含8种不同的食物。食物的选择必须严格符合需求'
    )
    prompt = prompt_template.format(menu_name=menu_name)
    
    print(f"正在生成: {menu_name}")
    print(f"提示词: {prompt}")
    
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model="deepseek-v3-1-terminus",
            messages=[
                {"role": "user", "content": prompt}
            ],
            thinking={
                "type": "enabled"  # 使用深度思考能力
            },
        )
        
        elapsed_time = round(time.time() - start_time, 2)
        
        # 提取思考过程和结果
        thinking_content = ""
        result_content = ""
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
            choice = response.choices[0]
            message = choice.message
            
            # 提取思考过程（在 reasoning_content 字段中）
            if hasattr(message, 'reasoning_content') and message.reasoning_content:
                thinking_content = message.reasoning_content
            
            # 提取结果内容
            if hasattr(message, 'content') and message.content:
                result_content = message.content
        
        print(f"✅ 生成成功: {menu_name} (耗时: {elapsed_time}秒)\n")
        
        return {
            'menu_name': menu_name,
            'thinking': thinking_content,
            'result': result_content,
            'status': 'success',
            'request_time': elapsed_time
        }
        
    except Exception as e:
        elapsed_time = round(time.time() - start_time, 2)
        print(f"❌ 生成失败: {menu_name} (耗时: {elapsed_time}秒)")
        print(f"错误: {str(e)}\n")
        
        return {
            'menu_name': menu_name,
            'thinking': '',
            'result': f"错误: {str(e)}",
            'status': 'failed',
            'request_time': elapsed_time
        }


def csv_to_excel(csv_path, excel_path):
    """从CSV转换为Excel"""
    wb = Workbook()
    ws = wb.active
    ws.title = "食谱生成结果"
    
    # 读取CSV并写入Excel
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)
    
    # 设置列宽
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 80
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 20
    
    # 保存文件
    wb.save(excel_path)
    print(f"✅ Excel 文件已保存到: {excel_path}")


def main():
    # 配置
    menu_file = os.path.join(os.path.dirname(__file__), 'test_menu_name.txt')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ 创建输出目录: {output_dir}\n")
    
    csv_file = os.path.join(output_dir, 'recipe_results.csv')
    excel_file = os.path.join(output_dir, 'recipe_results.xlsx')
    test_limit = None  # 获取全部食谱
    
    # 检查 API Key
    api_key = os.getenv('ARK_API_KEY')
    if not api_key:
        raise ValueError("请设置 ARK_API_KEY 环境变量")
    
    # 创建 Ark 客户端
    client = Ark(
        api_key=api_key,
        timeout=1800,  # 30分钟超时
    )
    
    # 读取食谱名称
    print(f"正在读取食谱列表: {menu_file}")
    menu_names = read_menu_names(menu_file, limit=test_limit)
    print(f"共读取 {len(menu_names)} 个食谱")
    
    # 检查已完成的食谱
    completed_menus = get_completed_menus(csv_file)
    if completed_menus:
        print(f"发现已完成 {len(completed_menus)} 个食谱，将跳过")
        menu_names = [name for name in menu_names if name not in completed_menus]
        print(f"剩余待处理: {len(menu_names)} 个食谱")
    
    if not menu_names:
        print("\n✅ 所有食谱已完成！")
        # 生成Excel文件
        if os.path.exists(csv_file):
            csv_to_excel(csv_file, excel_file)
        return
    
    print()
    
    # 判断是否为首次创建CSV
    is_new_file = not os.path.exists(csv_file) or len(completed_menus) == 0
    
    # 批量生成食谱
    success_count = 0
    failed_count = 0
    
    try:
        for i, menu_name in enumerate(menu_names, 1):
            print(f"[{i}/{len(menu_names)}] ", end='')
            result = generate_recipe(client, menu_name)
            
            # 立即保存到CSV
            save_to_csv(result, csv_file, is_new_file=(is_new_file and i == 1))
            
            if result['status'] == 'success':
                success_count += 1
            else:
                failed_count += 1
            
            # 避免请求过快，适当延迟
            if i < len(menu_names):
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断执行")
        print("已保存的进度会在下次运行时自动恢复")
    
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        print("已保存的进度会在下次运行时自动恢复")
    
    finally:
        # 生成Excel文件
        if os.path.exists(csv_file):
            print("\n正在生成 Excel 文件...")
            csv_to_excel(csv_file, excel_file)
        
        # 统计
        total_completed = len(get_completed_menus(csv_file))
        
        print("\n" + "=" * 70)
        print("📊 测试统计")
        print("=" * 70)
        print(f"本次成功: {success_count}")
        print(f"本次失败: {failed_count}")
        print(f"累计完成: {total_completed}")
        print(f"\nCSV 文件: {csv_file}")
        print(f"Excel 文件: {excel_file}")


if __name__ == "__main__":
    main()
