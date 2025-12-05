#!/usr/bin/env python3
"""
测试响应对象的结构，查看思考过程字段
"""
import os
from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark
import json

load_dotenv()

api_key = os.getenv('ARK_API_KEY')
if not api_key:
    raise ValueError("请设置 ARK_API_KEY 环境变量")

client = Ark(
    api_key=api_key,
    timeout=1800,
)

print("发送测试请求...")
response = client.chat.completions.create(
    model="deepseek-v3-1-terminus",
    messages=[
        {"role": "user", "content": "简单说明一下苹果的营养价值"}
    ],
    thinking={
        "type": "enabled"
    },
)

print("\n" + "="*70)
print("响应对象类型:", type(response))
print("="*70)

print("\n响应对象的所有属性:")
print(dir(response))

print("\n" + "="*70)
print("尝试访问各种可能的字段:")
print("="*70)

# 检查 response 的属性
if hasattr(response, '__dict__'):
    print("\nresponse.__dict__:")
    for key, value in response.__dict__.items():
        print(f"  {key}: {type(value)}")

# 检查 choices
if hasattr(response, 'choices'):
    print(f"\nresponse.choices: {type(response.choices)}")
    if response.choices and len(response.choices) > 0:
        choice = response.choices[0]
        print(f"choice type: {type(choice)}")
        print(f"choice attributes: {dir(choice)}")
        
        if hasattr(choice, '__dict__'):
            print("\nchoice.__dict__:")
            for key, value in choice.__dict__.items():
                print(f"  {key}: {type(value)}")
        
        # 检查 message
        if hasattr(choice, 'message'):
            message = choice.message
            print(f"\nmessage type: {type(message)}")
            print(f"message attributes: {dir(message)}")
            
            if hasattr(message, '__dict__'):
                print("\nmessage.__dict__:")
                for key, value in message.__dict__.items():
                    print(f"  {key}: {type(value)}")
                    if key in ['content', 'thinking', 'reasoning_content']:
                        print(f"    值: {value[:200] if value and len(str(value)) > 200 else value}")

# 尝试转换为字典
print("\n" + "="*70)
print("尝试查看完整响应:")
print("="*70)
try:
    if hasattr(response, 'model_dump'):
        print("\nresponse.model_dump():")
        dump = response.model_dump()
        print(json.dumps(dump, ensure_ascii=False, indent=2)[:2000])
    elif hasattr(response, 'dict'):
        print("\nresponse.dict():")
        print(json.dumps(response.dict(), ensure_ascii=False, indent=2)[:2000])
    else:
        print("\nresponse (str):")
        print(str(response)[:2000])
except Exception as e:
    print(f"转换失败: {e}")
