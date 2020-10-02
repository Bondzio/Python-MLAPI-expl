import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder
import gc
gc.enable()


dtypes = {
    'MachineIdentifier': 'category',
    'ProductName': 'category',
    'EngineVersion': 'category',
    'AppVersion': 'category',
    'AvSigVersion': 'category',
    'IsBeta': 'int8',
    'RtpStateBitfield': 'float16',
    'IsSxsPassiveMode': 'int8',
    'DefaultBrowsersIdentifier': 'float16',
    'AVProductStatesIdentifier': 'float32',
    'AVProductsInstalled': 'float16',
    'AVProductsEnabled': 'float16',
    'HasTpm': 'int8',
    'CountryIdentifier': 'int16',
    'CityIdentifier': 'float32',
    'OrganizationIdentifier': 'float16',
    'GeoNameIdentifier': 'float16',
    'LocaleEnglishNameIdentifier': 'int8',
    'Platform': 'category',
    'Processor': 'category',
    'OsVer': 'category',
    'OsBuild': 'int16',
    'OsSuite': 'int16',
    'OsPlatformSubRelease': 'category',
    'OsBuildLab': 'category',
    'SkuEdition': 'category',
    'IsProtected': 'float16',
    'AutoSampleOptIn': 'int8',
    'PuaMode': 'category',
    'SMode': 'float16',
    'IeVerIdentifier': 'float16',
    'SmartScreen': 'category',
    'Firewall': 'float16',
    'UacLuaenable': 'float32',
    'Census_MDC2FormFactor': 'category',
    'Census_DeviceFamily': 'category',
    'Census_OEMNameIdentifier': 'float16',
    'Census_OEMModelIdentifier': 'float32',
    'Census_ProcessorCoreCount': 'float16',
    'Census_ProcessorManufacturerIdentifier': 'float16',
    'Census_ProcessorModelIdentifier': 'float16',
    'Census_ProcessorClass': 'category',
    'Census_PrimaryDiskTotalCapacity': 'float32',
    'Census_PrimaryDiskTypeName': 'category',
    'Census_SystemVolumeTotalCapacity': 'float32',
    'Census_HasOpticalDiskDrive': 'int8',
    'Census_TotalPhysicalRAM': 'float32',
    'Census_ChassisTypeName': 'category',
    'Census_InternalPrimaryDiagonalDisplaySizeInInches': 'float16',
    'Census_InternalPrimaryDisplayResolutionHorizontal': 'float16',
    'Census_InternalPrimaryDisplayResolutionVertical': 'float16',
    'Census_PowerPlatformRoleName': 'category',
    'Census_InternalBatteryType': 'category',
    'Census_InternalBatteryNumberOfCharges': 'float32',
    'Census_OSVersion': 'category',
    'Census_OSArchitecture': 'category',
    'Census_OSBranch': 'category',
    'Census_OSBuildNumber': 'int16',
    'Census_OSBuildRevision': 'int32',
    'Census_OSEdition': 'category',
    'Census_OSSkuName': 'category',
    'Census_OSInstallTypeName': 'category',
    'Census_OSInstallLanguageIdentifier': 'float16',
    'Census_OSUILocaleIdentifier': 'int16',
    'Census_OSWUAutoUpdateOptionsName': 'category',
    'Census_IsPortableOperatingSystem': 'int8',
    'Census_GenuineStateName': 'category',
    'Census_ActivationChannel': 'category',
    'Census_IsFlightingInternal': 'float16',
    'Census_IsFlightsDisabled': 'float16',
    'Census_FlightRing': 'category',
    'Census_ThresholdOptIn': 'float16',
    'Census_FirmwareManufacturerIdentifier': 'float16',
    'Census_FirmwareVersionIdentifier': 'float32',
    'Census_IsSecureBootEnabled': 'int8',
    'Census_IsWIMBootEnabled': 'float16',
    'Census_IsVirtualDevice': 'float16',
    'Census_IsTouchEnabled': 'int8',
    'Census_IsPenCapable': 'int8',
    'Census_IsAlwaysOnAlwaysConnectedCapable': 'float16',
    'Wdft_IsGamer': 'float16',
    'Wdft_RegionIdentifier': 'float16',
    'HasDetections': 'int8'
}

continuous_columns = [  # All the columns which have a real continuous data
    'Census_ProcessorCoreCount',
    'Census_PrimaryDiskTotalCapacity',
    'Census_SystemVolumeTotalCapacity',
    'Census_TotalPhysicalRAM',
    'Census_InternalPrimaryDiagonalDisplaySizeInInches',
    'Census_InternalPrimaryDisplayResolutionHorizontal',
    'Census_InternalPrimaryDisplayResolutionVertical',
    'Census_InternalBatteryNumberOfCharges',
    'Census_OSBuildNumber',
    'Census_OSBuildRevision',
    'Census_ThresholdOptIn',
    'OsBuild'
]

bool_columns = [
    'IsBeta',
    'IsSxsPassiveMode',
    'Census_IsPortableOperatingSystem',
    'Census_IsSecureBootEnabled',
    'Census_IsTouchEnabled',
    'Census_IsPenCapable',
    'HasTpm',
    'Census_HasOpticalDiskDrive'
]

print('Download Train and Test Data.\n')
train = pd.read_csv('../input/train.csv', dtype=dtypes, low_memory=True)
train['MachineIdentifier'] = train.index.astype('uint32')
test = pd.read_csv('../input/test.csv', dtype=dtypes, low_memory=True)
test['MachineIdentifier'] = test.index.astype('uint32')
del dtypes

gc.collect()

print('Transform all features to category.\n')
categorical_feature = []
col_number = -1
for col_name in train.columns.tolist()[1:-1]:
    col_number = col_number+1
    if col_name in bool_columns:
        continue
    elif col_name in continuous_columns:
        nan_val = train[col_name].astype('float32').mean()
        train[col_name].fillna(nan_val, inplace=True)
        test[col_name].fillna(nan_val, inplace=True)
        del nan_val
        continue
    categorical_feature.append(col_number)
    train[col_name] = train[col_name].astype('str')
    test[col_name] = test[col_name].astype('str')

    # Fit LabelEncoder
    le = LabelEncoder().fit(
        np.unique(train[col_name].unique().tolist() +
                  test[col_name].unique().tolist()))

    # At the end 0 will be used for dropped values
    train[col_name] = le.transform(train[col_name]) + 1
    test[col_name] = le.transform(test[col_name]) + 1

    agg_tr = (train
              .groupby([col_name])
              .aggregate({'MachineIdentifier': 'count'})
              .reset_index()
              .rename({'MachineIdentifier': 'Train'}, axis=1))
    agg_te = (test
              .groupby([col_name])
              .aggregate({'MachineIdentifier': 'count'})
              .reset_index()
              .rename({'MachineIdentifier': 'Test'}, axis=1))

    agg = pd.merge(agg_tr, agg_te, on=col_name, how='outer').replace(np.nan, 0)
    # Select values with more than 1000 observations
    agg = agg[(agg['Train'] > 1000)].reset_index(drop=True)
    agg['Total'] = agg['Train'] + agg['Test']
    # Drop unbalanced values
    agg = agg[(agg['Train'] / agg['Total'] > 0.2) & (agg['Train'] / agg['Total'] < 0.8)]
    agg[col_name + 'Copy'] = agg[col_name]

    train[col_name] = (pd.merge(train[[col_name]], agg[[col_name, col_name + 'Copy']],
                                on=col_name, how='left')[col_name + 'Copy'].replace(np.nan, 0).astype('str'))

    test[col_name] = (pd.merge(test[[col_name]], agg[[col_name, col_name + 'Copy']],
                               on=col_name, how='left')[col_name + 'Copy'].replace(np.nan, 0).astype('str'))

    # Fit LabelEncoder again to make the all the category to have continues numbers
    le = LabelEncoder().fit(
        np.unique(train[col_name].unique().tolist() +
                  test[col_name].unique().tolist()))
    train[col_name] = le.transform(train[col_name])
    test[col_name] = le.transform(test[col_name])

    del le, agg_tr, agg_te, agg
    gc.collect()

    mx = max(train[col_name].max(), test[col_name].max())
    if mx < 2**7:
        train[col_name] = train[col_name].astype('int8')
        test[col_name] = test[col_name].astype('int8')
    elif mx < 2**15:
        train[col_name] = train[col_name].astype('int16')
        test[col_name] = test[col_name].astype('int16')
    else:
        train[col_name] = train[col_name].astype('int32')
        test[col_name] = test[col_name].astype('int32')
    del col_name, mx

del col_number, continuous_columns, bool_columns
gc.collect()

y_train = np.array(train['HasDetections'])
test_ids = test.index

del train['HasDetections'], train['MachineIdentifier'], test['MachineIdentifier']
gc.collect()

train.to_pickle('train.pcl')
test.to_pickle('test.pcl')
np.save('y_train.npy', y_train)
del train, test

lgb_test_probs = np.zeros(test_ids.shape[0], dtype=np.float32)
lgb_test_result = np.zeros(test_ids.shape[0], dtype=np.float32)

n_train_elements = y_train.shape[0]
w = np.ones(n_train_elements, dtype=np.float32)
del n_train_elements, test_ids

print('\nadaBoost with LightGBM:\n')
w_sum = 0
n_iterations = 5
m = 200000
for i in range(n_iterations):
    print('iteration {}:\n'.format(i+1))
    print('The average of w is {}'. format(np.mean(w)))
    print('The std of w is {}'. format(np.std(w)))

    train = pd.read_pickle('train.pcl')
    y_train = np.load('y_train.npy')

    lgb_model = lgb.LGBMClassifier(max_depth=-1,
                                   n_estimators=100,
                                   learning_rate=0.05,
                                   num_leaves=2 ** 12 - 1,
                                   colsample_bytree=0.28,
                                   objective='binary',
                                   n_jobs=-1,
                                   categorical_feature=categorical_feature,
                                   cat_l2=50,
                                   cat_smooth=0)
    lgb_model.fit(train, y_train, sample_weight=w)

    # Find the iteration weight
    train_res = [lgb_model.predict(train.iloc[j*m:(j+1)*m]) for j in range(int(np.ceil(len(y_train)/m)))]
    del train
    gc.collect()
    train_res = np.hstack(train_res)
    dff = np.abs(train_res - y_train)
    err = np.dot(w, dff) / np.sum(w)
    iter_w = 0.5*np.log((1-err)/err)
    print('The iteration error is {}', format(err))
    print('The iteration weight is {}', format(iter_w))

    # Update w
    dff[dff == 1] = -1
    dff[dff == 0] = 1
    w *= np.exp(-iter_w*dff)

    del train_res, y_train
    gc.collect()

    test = pd.read_pickle('test.pcl')
    test_res = [lgb_model.predict_proba(test.iloc[j*m:(j+1)*m])[:, 1] for j in range(int(np.ceil(len(lgb_test_probs)/m)))]
    test_res = np.hstack(test_res)
    lgb_test_probs += iter_w*test_res
    test_res = test_res > 0.5
    lgb_test_result += iter_w*test_res
    w_sum += iter_w

    del test, dff, err, iter_w, lgb_model, test_res
    gc.collect()

submission = pd.read_csv('../input/sample_submission.csv')
submission['HasDetections'] = lgb_test_result / w_sum
filename = 'adaBoost_lgb_absolute_res.csv'
submission.to_csv(filename, index=False)
submission['HasDetections'] = lgb_test_probs / w_sum
filename = 'adaBoost_lgb_prob_res.csv'
submission.to_csv(filename, index=False)

print('\nDone.')
