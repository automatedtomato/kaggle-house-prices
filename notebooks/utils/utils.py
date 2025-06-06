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
    
def plot_feature_importance(model, feature_names, type='coef', title="Importance of Features"):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 図のサイズ設定
    plt.figure(figsize=(12, 8))
    
    
    # 係数を取得
    if type == 'coef':
        
        coef = model.coef_
    
        # 係数の絶対値でソート
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': np.abs(coef),
            'coefficient': coef
        }).sort_values('importance', ascending=False)
        
        # プロット（係数の符号で色分け）
        colors = ['red' if c < 0 else 'blue' for c in importance['coefficient']]
        sns.barplot(x='importance', y='feature', data=importance, palette=colors)
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', label='positive influence'),
            Patch(facecolor='red', label='negative influence')
        ]
        plt.legend(handles=legend_elements, loc='lower right')
        

        
    elif type == 'feature_importances':
        
        feature_importances = model.feature_importances_
        
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importances
        }).sort_values('importance', ascending=False)
        sns.barplot(x='importance', y='feature', data=importance)
        
        # 軸ラベルとタイトル
        plt.xlabel('Importance')
        plt.ylabel('Features')
        plt.title(title)
        
    else:
        raise ValueError('type must be "coef" or "feature_importances"')
    
    plt.tight_layout()
    
    return importance.reset_index(drop=True)


def plot_learning_curve(estimator, X, y, title="Learning Curve"):
    from sklearn.model_selection import learning_curve
    import matplotlib.pyplot as plt
    
    # 学習曲線の計算
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5,
        scoring='neg_mean_squared_error',
        n_jobs=-1
    )
    
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)
    
    
    # プロット作成
    plt.plot(train_sizes, train_mean, 
                marker='o', label='Training')
    plt.plot(train_sizes, val_mean, ls='--',
                marker='o', label='Validation')
    
    # 信頼区間の追加
    plt.fill_between(train_sizes, 
                     train_mean - train_std,
                     train_mean + train_std, 
                     alpha=0.1)
    plt.fill_between(train_sizes,
                     val_mean - val_std,
                     val_mean + val_std,
                     alpha=0.1)
    
    # グラフの装飾
    plt.title(title)
    plt.xlabel('Training Examples')
    plt.ylabel('Neg Mean Squared Error')
    plt.legend()
    plt.tight_layout()