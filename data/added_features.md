# 0000_EDA

    - log_price: 'SalePrice'を自然対数変換したもの。

    - neighbor_price_mmscaled: 'Neighborhood'ごとに'SalePrice'の平均を集計し、min-max法により立地を係数化したもの。

    - neighbor_log_price_stdscaled: 'Neighborhood'ごとに'LogPrice'の平均を集計し、標準化により立地を係数化したもの。

    - total_sf = 1stFlrSF + 2ndFlrSF (nan = 0) + TotalBsmtSF (nan = 0)

    - 下記のそれぞれを重みづけ: log_は対数価格に対する標準化指標
                'OverallQual', 'OverallCond', 'ExterQual', 'ExterCond', 
                'BsmtQual', 'BsmtCond', 'BsmtFinType1', 'BsmtFinType2',
                'HeatingQC', 'KitchenQual', 'FireplaceQu',
                'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC',
                'Fence', 'Functional'

    - has_2nd: ２階の有無フラグ

    - has_bsmt: 地下室の有無フラグ

    - has_garage: ガレージの有無フラグ

    - has_pool: プールの有無フラグ

    - house_age: 販売年 - 建築年

    - 以下の特徴量に対し、対数変換した特徴量を追加: log_
                 '1stFlrSF', '2ndFlrSF', 'TotalBsmtSF',
                'GrLivArea', 'LotArea', 'total_sf'

    - remod_age: 販売年 - 改築年

    - yrs_before_remod: 改築年 - 建築年

    - is_remodeled: 改築の有無フラグ

    - built_era: 1900年以前、1900~1940年、以降20年区切り、2000年以降で建築年代をカテゴライズ

    - year_price:　建築年ごとの住宅価格のローリング平均