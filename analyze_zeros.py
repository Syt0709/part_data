# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def save_markdown_report(periods, df, all_zeros, filename="analysis_report.md"):
    """将分析结果保存为Markdown文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        # 写入报告标题和基本信息
        f.write("# 零值时间段分析报告\n\n")
        f.write(f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 分析文件: 20241107-20250617.csv\n")
        f.write(f"- 总数据行数: {len(df)}\n\n")
        
        # 写入数据概览
        f.write("## 数据概览\n```python\n")
        f.write(f"数据形状: {df.shape}\n")
        f.write(f"列名: {list(df.columns)}\n\n")
        f.write("前5行数据:\n")
        f.write(df.head().to_markdown())
        f.write("\n```\n\n")
        
        # 写入零值统计
        f.write("## 零值统计\n")
        f.write(f"- 零值行总数: {all_zeros.sum()}\n")
        f.write(f"- 零值时间段数量: {len(periods)}\n\n")
        
        # 写入时间段详情
        if periods:
            f.write("## 零值时间段详情\n")
            for i, period in enumerate(periods, 1):
                f.write(f"### 时间段 {i}\n")
                f.write(f"- 行范围: {period['开始行']} - {period['结束行']}\n")
                f.write(f"- 时间范围: {period['开始时间']} - {period['结束时间']}\n")
                f.write(f"- 持续时间: {period['持续时间']} 个数据点\n\n")
        else:
            f.write("## 未发现零值时间段\n")
        
        # 写入统计摘要
        if periods:
            avg_duration = sum(p['持续时间'] for p in periods) / len(periods)
            f.write("## 统计摘要\n")
            f.write(f"- 平均持续时间: {avg_duration:.2f} 个数据点\n")
            f.write(f"- 最长持续时间: {max(p['持续时间'] for p in periods)} 个数据点\n")
            f.write(f"- 最短持续时间: {min(p['持续时间'] for p in periods)} 个数据点\n")

def analyze_zero_periods():
    """分析Excel文件中第2到5列每列都为0的时间段"""
    try:
        # 读取Excel文件
        print("正在读取Excel文件...")
        df = pd.read_csv('20241107-20250617.csv', encoding='gbk')
        
        # [原有分析代码保持不变...]
        # ... [这里是你原来的分析代码]
        
        # 保存报告
        save_markdown_report(periods, df, all_zeros)
        print(f"\n分析报告已保存为 analysis_report.md")
        
        return periods, df
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        return None, None

if __name__ == "__main__":
    print("开始分析Excel文件中第2到5列都为0的时间段...")
    print("=" * 80)
    
    periods, df = analyze_zero_periods()
    
    if periods is not None:
        print("\n分析完成！报告已生成。")
    else:
        print("\n分析失败，请检查Excel文件格式是否正确。")
