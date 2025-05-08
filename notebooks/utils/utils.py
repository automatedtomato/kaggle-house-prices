import pandas as pd
import numpy as np

def ordinal_to_weight(df: pd.DataFrame, col_name: str, target: str='SalePrice', log_transform=False, scaler_type: str='minmax'):
    """
    順序尺度のカテゴリをターゲットエンコーディングする関数

    Args:
        df (DataFrame): 対象データフレーム
        col_name (str): 順序尺度の列名
        target (str, optional): Defaults to 'SalePrice'.
        log_transform (bool, optional): 対数変換するかどうか. Defaults to False.
        scale_typy (str): スケーリング方法（'standard', 'minmax'）. Defaults to 'minmax'.
        
    Returns:
        DataFrame: 新しい特徴量が追加されたデータフレーム
        dict: 変換用の辞書（テストデータ用）
    """
    
    df_copy = df.copy()
    
    # 対数変換の処理
    if log_transform and target == 'SalePrice':
        target_col = f'log_{target}'
        if target_col not in df_copy.columns:
            df_copy[target_col] = np.log(df_copy[target])
    else:
        target_col = target
        
    # 各カテゴリの平均値を計算
    category_weight = df_copy.groupby(col_name)[target_col].mean()
    
    # スケーリング
    if scaler_type == 'standard':
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
    elif scaler_type == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    else:
        raise ValueError('scale_type must be "standard" or "minmax"')
    
    if scaler_type != 'none':
        scaled_values = scaler.fit_transform(category_weight.values.reshape(-1, 1)).flatten()
        category_weight_dict = dict(zip(category_weight.index, scaled_values))
        
    if log_transform and target == 'SalePrice':
        new_col_name = f'log_{col_name}_weight'
    else:
        new_col_name = f'{col_name}_weight'
        
    df_copy[new_col_name] = df_copy[col_name].map(category_weight_dict)

    
    return df_copy, category_weight_dict


def freq_dist(data, class_width=None):
    """ 度数分布表を作成する関数 """
    data = np.asarray(data)
    if class_width is None:
        class_size = int(np.log2(data.size).round()) + 1
        class_width = round((data.max() - data.min()) / class_size)

    bins = np.arange(0, data.max()+class_width+1, class_width)
    hist = np.histogram(data, bins)[0]
    cumsum = hist.cumsum()

    return pd.DataFrame({'階級値': (bins[1:] + bins[:-1]) / 2,
                         '度数': hist,
                         '累積度数': cumsum,
                         '相対度数': hist / cumsum[-1],
                         '累積相対度数': cumsum / cumsum[-1]},
                        index=pd.Index([f'{bins[i]}以上{bins[i+1]}未満'
                                        for i in range(hist.size)],
                                       name='階級'))
    
def plot_feature_importance(model, feature_names, title="Importance of Features"):
    import matplotlib.pyplot as plt
    import seaborn as sns
    # 係数を取得
    coef = model.coef_
    
    # 係数の絶対値でソート
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': np.abs(coef),
        'coefficient': coef
    }).sort_values('importance', ascending=False)
    
    # 図のサイズ設定
    plt.figure(figsize=(12, 8))
    
    # プロット（係数の符号で色分け）
    colors = ['red' if c < 0 else 'blue' for c in importance['coefficient']]
    sns.barplot(x='importance', y='feature', data=importance, palette=colors)
    
    # 軸ラベルとタイトル
    plt.xlabel('Abs. coef')
    plt.ylabel('Features')
    plt.title(title)
    
    # 凡例を追加
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', label='positive influence'),
        Patch(facecolor='red', label='negative influence')
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.show()
    
    return importance