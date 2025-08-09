import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_zero_periods():
    """
    分析Excel文件中第2到5列每列都为0的时间段
    """
    try:
        # 读取Excel文件
        print("正在读取Excel文件...")
        df = pd.read_excel('部分数据.xlsx')
        
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        print("\n前5行数据:")
        print(df.head())
        
        # 检查是否有时间列
        time_column = None
        for col in df.columns:
            if '时间' in str(col) or 'time' in str(col).lower() or 'date' in str(col).lower():
                time_column = col
                break
        
        if time_column is None:
            print("\n未找到时间列，使用行索引作为时间")
            df['时间'] = range(len(df))
            time_column = '时间'
        
        # 获取第2到5列（索引1到4，因为从0开始计数）
        # 排除时间列，确保我们只分析数据列
        data_columns = [col for col in df.columns if col != time_column and col != '序号']
        target_columns = data_columns[1:5]  # 第2到5列（排除时间列后）
        
        print(f"\n数据列（排除时间列）: {data_columns}")
        print(f"分析的目标列: {list(target_columns)}")
        
        # 显示目标列的数据
        print(f"\n目标列的数据样本:")
        print(df[target_columns].head(10))
        
        # 检查这些列是否都为0
        all_zeros = (df[target_columns] == 0).all(axis=1)
        
        print(f"\n总共有 {len(df)} 行数据")
        print(f"其中 {all_zeros.sum()} 行满足第2到5列都为0的条件")
        
        # 显示哪些行满足条件
        zero_rows = df[all_zeros]
        if len(zero_rows) > 0:
            print(f"\n满足条件的行:")
            print(zero_rows[['序号', time_column] + list(target_columns)])
        
        # 找出连续的时间段
        periods = []
        start_idx = None
        
        for i, is_zero in enumerate(all_zeros):
            if is_zero and start_idx is None:
                # 开始一个新的零值段
                start_idx = i
            elif not is_zero and start_idx is not None:
                # 结束一个零值段
                end_idx = i - 1
                start_time = df.iloc[start_idx][time_column]
                end_time = df.iloc[end_idx][time_column]
                periods.append({
                    '开始行': start_idx,
                    '结束行': end_idx,
                    '开始时间': start_time,
                    '结束时间': end_time,
                    '持续时间': end_idx - start_idx + 1
                })
                start_idx = None
        
        # 处理最后一个时间段（如果以零值结束）
        if start_idx is not None:
            end_idx = len(df) - 1
            start_time = df.iloc[start_idx][time_column]
            end_time = df.iloc[end_idx][time_column]
            periods.append({
                '开始行': start_idx,
                '结束行': end_idx,
                '开始时间': start_time,
                '结束时间': end_time,
                '持续时间': end_idx - start_idx + 1
            })
        
        # 输出结果
        print(f"\n找到 {len(periods)} 个时间段，其中第2到5列都为0:")
        print("=" * 80)
        
        if periods:
            for i, period in enumerate(periods, 1):
                print(f"时间段 {i}:")
                print(f"  行范围: {period['开始行']} - {period['结束行']}")
                print(f"  时间范围: {period['开始时间']} - {period['结束时间']}")
                print(f"  持续时间: {period['持续时间']} 个数据点")
                print()
        else:
            print("没有找到第2到5列都为0的时间段")
        
        # 统计信息
        total_zero_rows = all_zeros.sum()
        total_periods = len(periods)
        if total_periods > 0:
            avg_duration = sum(p['持续时间'] for p in periods) / total_periods
            max_duration = max(p['持续时间'] for p in periods)
            min_duration = min(p['持续时间'] for p in periods)
            
            print("统计信息:")
            print(f"  总零值行数: {total_zero_rows}")
            print(f"  零值时间段数: {total_periods}")
            print(f"  平均持续时间: {avg_duration:.2f} 个数据点")
            print(f"  最长持续时间: {max_duration} 个数据点")
            print(f"  最短持续时间: {min_duration} 个数据点")
        
        return periods, df
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        return None, None

if __name__ == "__main__":
    print("开始分析Excel文件中第2到5列都为0的时间段...")
    print("=" * 80)
    
    periods, df = analyze_zero_periods()
    
    if periods is not None:
        print("\n分析完成！")
    else:
        print("\n分析失败，请检查Excel文件格式是否正确。")
