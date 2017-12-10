# coding=utf-8
#!/usr/bin/env python
# useage:
#
#   python build-ios.py ledo inhouse 3.3.0  (打包某个渠道)
#   python build-ios.py ledo dis 3.3.0 (打包某个渠道)
#
#

import os
import sys
import plistlib


# 设置签名信息,bxzw
signs = {   'ledo_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "fedc8540-50f7-4d5e-8414-8e4f421c4ebc", "anhei2 trunk inhouse 0516",'com.ledo.bxzw.trunk','Y3P36D8Q5L'),
            'ledo_dis':("iPhone Distribution: wei yan (UE2D275WT6)", "834b5f12-9291-408d-9fa5-690b9a6cf43b", "dis",'com.ledo.bxzw1.appledo','UE2D275WT6'),
            'ledo_adhoc':("iPhone Distribution: wei yan (UE2D275WT6)", "0a63b3b8-ef15-4b78-9677-9d640954e5a2", "hoc",'com.ledo.bxzw1.appledo','UE2D275WT6'),
            'tuyoo_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "dee88104-1897-456c-ad2d-e8309f06a4a6", "anhei2 tuyoo inhouse2","com.ledo.bxzw.tuyoo",'Y3P36D8Q5L'),
            'tuyoo_dis':("iPhone Distribution: Qi Qin (DQ9CFP9783)", "3a0275e3-ef0b-4f38-87bf-ff2658b1f639", "ahry_app store",'com.sd.ahry','DQ9CFP9783'),
            'tuyoo_adhoc':("iPhone Distribution: Qi Qin (DQ9CFP9783)", "5b9b67a2-e9a7-4d05-8fa7-74f2d6afc2df", "ahry_app hot",'com.sd.ahry','DQ9CFP9783'),
            'yd_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "073f9d91-2eed-4f5a-a5f5-25ef198e128d", "anhei2 funding","com.ledo.bxzw.tuyoo",'Y3P36D8Q5L'),
            'yd_dis':("iPhone Distribution: dong wu (FK29Q5Y9TC)", "b268a511-40ce-436b-9fc2-653fad6356bc", "dis_xahlm0523",'com.ledao.yd.xahlm','FK29Q5Y9TC'),
            'yd_adhoc':("iPhone Distribution: dong wu (FK29Q5Y9TC)", "75aab6a4-a859-4505-aa0e-5708c91e59a2", "dis_adhoc_xahlm0523",'com.ledao.yd.xahlm','FK29Q5Y9TC'),
            'tuyoo2_dis':("iPhone Distribution: Bo Yuan (P9S5X5H4LP)", "c9a58122-93ce-4275-8e99-7470e84f26c1", "hacs_App Store",'com.shdiao.hacs','P9S5X5H4LP'),
            'tuyoo2_adhoc':("iPhone Distribution: Bo Yuan (P9S5X5H4LP)", "e71c087c-5cf2-44ab-a3eb-276e7426506a", "hacs_Ad Hoc",'com.shdiao.hacs','P9S5X5H4LP'),
            'tuyoo3_dis':("iPhone Distribution: Ce Qian (V893E47E44)", "0ab7c7ca-d1b3-4737-904f-b23fce9090b4", "lmzj_App Store",'com.shediao.lmzj','V893E47E44'),
            'tuyoo3_adhoc':("iPhone Distribution: Ce Qian (V893E47E44)", "756ee0d0-0c04-44a8-adb9-8f6a5e219603", "lmzj_Ad Hoc",'com.shediao.lmzj','V893E47E44'),
            '9377_dis':("iPhone Distribution: piaopiao yang (5WE6M23QQC)", "1b9145be-5877-45c3-a4d0-0d5a3b7da6b6", "agrc_appstore",'com.dxhjsz.rnk.agrc','5WE6M23QQC'),
            '9377_adhoc':("iPhone Distribution: piaopiao yang (5WE6M23QQC)", "4a6c959c-1037-4962-8d35-8becf5d3a4ab", "agrc_adhoc",'com.dxhjsz.rnk.agrc','5WE6M23QQC'),
            's9377_dis':("iPhone Distribution: Najib Fizzer (8B4XMEG688)", "4ec83c71-3572-4998-9aab-0b7454de634f", "aylr_appstore",'com.swkj.an.aylr','8B4XMEG688'),
            's9377_adhoc':("iPhone Distribution: Najib Fizzer (8B4XMEG688)", "be58c21e-6f51-497c-81a9-40a7baa72369", "aylr_adhoc",'com.swkj.an.aylr','8B4XMEG688'),
            'y9377_dev':("iPhone Developer: Makmood Fizzer (CBNPZ7AWMH)", "c6cf5a55-d2e5-411f-8583-a7836fac0d33", "agrc_dev",'com.asybkl.agrc','CBNPZ7AWMH'),
            'y9377_dis':("iPhone Distribution: Makmood Fizzer (92TVL8U6E9)", "79576043-b48f-4042-932e-4d2b757e7a3d", "agrc_appstore",'com.asybkl.agrc','92TVL8U6E9'),
            'y9377_adhoc':("iPhone Distribution: Makmood Fizzer (92TVL8U6E9)", "b14811be-a89e-41ac-ae65-93fd716dcf4d", "agrc_adhoc",'com.asybkl.agrc','92TVL8U6E9'),
            'yom3_dis':("iPhone Distribution: zhang guojing (EZ5H73YC37)", "46923ffa-2fef-4d75-8787-e4f26d110ccc", "anheiemocheng_dis",'com.anheiemocheng','EZ5H73YC37'),
            'yom2_dis':("iPhone Distribution: Jinjun Qiu (FMJPF8Z53G)", "1ecb7057-123c-4e0a-8be4-336ec5930cb9", "appstore_qmsy",'com.guangmingshenyu','FMJPF8Z53G'),
            'yom2_adhoc':("iPhone Distribution: Jinjun Qiu (FMJPF8Z53G)", "5e1e402f-9337-40f7-8882-ead813a5621f", "adhoc_qmsy",'com.guangmingshenyu','FMJPF8Z53G'),
            'yom_dis':("iPhone Distribution: Sigui Wang (KZUK3BQQ8U)", "f580a144-c315-4b92-804d-de68d8719512", "syyh_dis",'com.shenyuyongheng','KZUK3BQQ8U'),
            'yom_adhoc':("iPhone Developer: Sigui Wang (X72U7QHL3G)", "1026c31c-71d8-45b6-9ece-cad95bc41d48", "syyh_dev",'com.shenyuyongheng','X72U7QHL3G'),
            'yom4_dis':("iPhone Distribution: niu le (344BYW57N5)", "f8bd454b-111f-49f4-b425-d820be261a85", "wangzheqiji_dis",'com.wangzheqiji','344BYW57N5'),
            'dxhk_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "40596a49-67d4-41bc-bf14-84597a2e0daa", "anhei2 gangao inhouse201708",'com.ledo.ahlm2.gangao','Y3P36D8Q5L'),
            'dxhk_dis':("iPhone Distribution: EVATAR CO., LTD. (8X79XT88LF)", "2fbe5c4e-a247-4001-9cde-d4e10e670c7e", "dxhk_dist_20171122",'com.baplay.dxhk','8X79XT88LF'),
            'dxhk_adhoc':("iPhone Distribution: EVATAR CO., LTD. (8X79XT88LF)", "9fe37ee2-630c-4f50-89aa-b830d39333ee", "dxhk_adhoc_20171122",'com.baplay.dxhk','8X79XT88LF'),
            'dx_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "f52683f7-81f1-47b1-af60-c97c52c59fa1", "anhei2 tw inhouse201708",'com.ledo.ahlm2.tw','Y3P36D8Q5L'),
            'dx_dis':("iPhone Distribution: EVATAR CO., LTD. (8X79XT88LF)", "ed80ef33-8e85-409b-a460-d014c7d7bc8c", "dx_dist_20171122",'com.baplay.dx','8X79XT88LF'),
            'dx_adhoc':("iPhone Distribution: EVATAR CO., LTD. (8X79XT88LF)", "7918e747-6e8c-4a41-a251-b01f63f305ef", "dx_adhoc_20171122",'com.baplay.dx','8X79XT88LF'),
            'efun_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "a5f4e39d-5497-4ab4-bddf-f1f61a8a1c04", "anhei2 hang inhouse201708",'com.ledo.bxzw.hanguo','Y3P36D8Q5L'),
            'efun_dis':("iPhone Distribution: Efun International Ltd (S5XF4KTL5U)", "05722ec1-97a0-4a32-aa35-12fb0934dbe0", "disahlm20171106",'com.vqw.ahlm','S5XF4KTL5U'),
            'efun_adhoc':("iPhone Distribution: Efun International Ltd (S5XF4KTL5U)", "0fe5622e-a690-442d-99ca-51a236be0966", "adhocahlm20171106",'com.vqw.ahlm','S5XF4KTL5U'),
            'xjp_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "ec298282-f275-443e-a28c-0f413d97563e", "com.ledo.bxzw.xjp",'com.ledo.bxzw.xjp','Y3P36D8Q5L'),
            'xjp_dis':("iPhone Distribution: WISDOM ENTERTAINMENT ONLINE INTERNATIONAL LIMITED (2VFRS7GQXS)", "390deca4-57dc-48e3-bfd1-5bf55180d7a5", "ahlm2_20161101_appstore",'com.ujoy.dawn2.ios','2VFRS7GQXS'),
            'xjp_adhoc':("iPhone Distribution: WISDOM ENTERTAINMENT ONLINE INTERNATIONAL LIMITED (2VFRS7GQXS)", "a26647c6-a2c5-4285-9d62-8aba88370a41", "ahlm2_20161101_adhoc",'com.ujoy.dawn2.ios','2VFRS7GQXS'),
            'vietnam_inhouse':("iPhone Distribution: Tianjin Ledo Interactive Technology Co., Ltd.", "cc5afa1c-e626-4725-9d88-33d78a241ef5", "com.ledo.bxzw.yn",'com.ledo.bxzw.yn','Y3P36D8Q5L'),
            'vietnam_dis':("iPhone Distribution: Li Li (EDC2UD24UG)", "89bb9578-2da2-4e83-bd80-396a3b4c4a31", "hamv_20170329_appstore",'com.ujoy.hamv.ios','EDC2UD24UG'),
            'vietnam_adhoc':("iPhone Distribution: Li Li (EDC2UD24UG)", "c2d30944-bec5-4708-920d-936d8c407ea2", "hamv_20170329_adhoc",'com.ujoy.hamv.ios','EDC2UD24UG'),
            'xgao_dis':("iPhone Distribution: chang xiao (44XC3446VT)", "e8f950ef-9311-4a23-98fb-1be908c901b5", "shenyuqiyue_appsto",'com.changxiao.syqy','44XC3446VT'),
            'xgao_adhoc':("iPhone Distribution: chang xiao (44XC3446VT)", "5d38833c-81b8-46ba-808e-b0934e6d64d5", "shenyuqiyue_adhoc",'com.changxiao.syqy','44XC3446VT'),
            'xgao2_dis':("iPhone Distribution: xueqian dang (L7JBRLTWAN)", "546ece7d-4123-47f9-8827-cce572e53ad5", "kuangbaozhiren_appsto",'com.qianxuedang.kbzr','L7JBRLTWAN'),
            'xgao2_adhoc':("iPhone Distribution: xueqian dang (L7JBRLTWAN)", "8fc6d97d-c752-4119-9bf6-96e711ff6e0a", "kuangbaozhiren_adhoc",'com.qianxuedang.kbzr','L7JBRLTWAN'),
            'xgao3_dis':("iPhone Distribution: jiao ding (JMKSHV7NJ5)", "cbc1c7f5-9ce5-4ef3-a7ab-1962a42a81b8", "fengbaozhange_appsto",'com.jiaoding.qjlm','JMKSHV7NJ5'),
            'xgao3_adhoc':("iPhone Distribution: jiao ding (JMKSHV7NJ5)", "c9ba4632-aec6-43a2-8963-3c48c528bdaa", "fengbaozhange_adhoc",'com.jiaoding.qjlm','JMKSHV7NJ5'),
            'jsh_dis':("iPhone Distribution: Angelo Colombo (NTDV8V44YM)", "e801e9cc-6043-4e53-83ec-ba8cf8f7b853", "sy iOS Distribution",'com.blademaster.sy','NTDV8V44YM'),
            'jsh_adhoc':("iPhone Distribution: Angelo Colombo (NTDV8V44YM)", "7726957f-d79a-4e41-863a-d95336ecb05f", "sy AD HOC",'com.blademaster.sy','NTDV8V44YM'),
        }

# 设置渠道plist文件相对路径
plists = {  "ledo":("icefire_ios_ledo", "./icefire_ios_ledo-Info.plist"),
            "tuyoo":("icefire_ios_tuyoo", "./icefire_ios_tuyoo-info.plist"),
            "yd":("icefire_ios_yd", "./icefire_ios_yd-info.plist"),
            "tuyoo2":("icefire_ios_tuyoo2", "./icefire_ios_tuyoo-info2.plist"),
            "tuyoo3":("icefire_ios_tuyoo3", "./icefire_ios_tuyoo-info3.plist"),
            "9377":("icefire_ios_9377", "./icefire_ios_9377-info.plist"),
            "s9377":("icefire_ios_s9377", "./icefire_ios_s9377-info.plist"),
            "y9377":("icefire_ios_y9377", "./icefire_ios_y9377-info.plist"),
            "yom":("icefire_ios_yom", "./icefire_ios_yom-info.plist"),
            "yom2":("icefire_ios_yom2", "./icefire_ios_yom2-info.plist"),
            "yom3":("icefire_ios_yom3", "./icefire_ios_yom3-info.plist"),
            "yom4":("icefire_ios_yom4", "./icefire_ios_yom4-Info.plist"),
            "dxhk":("icefire_ios_baplay_dxhk", "./icefire_ios_baplay_dxhk-Info.plist"),
            "dx":("icefire_ios_baplay_dx", "./icefire_ios_baplay_dx-Info.plist"),
            "efun":("icefire_ios_efun", "./icefire_ios_efun.plist"),
            "xjp":("icefire_ios_37", "./icefire_ios_37-Info.plist"),
            "vietnam":("icefire_ios_37", "./icefire_ios_37yn-Info.plist"),
            "xgao":("icefire_ios_xgao", "./icefire_ios_xgao-Info.plist"),
            "xgao2":("icefire_ios_xgao2", "./icefire_ios_xgao2-Info.plist"),
            "xgao3":("icefire_ios_xgao3", "./icefire_ios_xgao3-Info.plist"),
            "jsh":("icefire_ios_jsh", "./icefire_ios_jsh-Info.plist"),
            }

def set_info(target,cur_plist,version,bundleid):
    # set version CFBundleIdentifier
    print("--------------------------------version------------------------------")
    print('/usr/libexec/PlistBuddy -c "set :CFBundleIdentifier {0}" {1}'.format(bundleid,cur_plist))
    print('/usr/libexec/PlistBuddy -c "set :CFBundleShortVersionString {0}" {1}'.format(version,cur_plist))
    print('/usr/libexec/PlistBuddy -c "set :CFBundleVersion {0}" {1}'.format(version,cur_plist))
    
    os.system('/usr/libexec/PlistBuddy -c "set :CFBundleIdentifier {0}" {1}'.format(bundleid,cur_plist))
    os.system('/usr/libexec/PlistBuddy -c "set :CFBundleShortVersionString {0}" {1}'.format(version,cur_plist))
    os.system('/usr/libexec/PlistBuddy -c "set :CFBundleVersion {0}" {1}'.format(version,cur_plist))
    

def build_target(nickname, target, sign_info, cur_plist, version, bundleid):
    cur_xcarchive = "./" + nickname + ".xcarchive"
    cur_ipa = "./" + nickname + ".ipa"

    # clean project
    print("准备清理工程...")
    if os.path.isfile(cur_ipa):
        os.remove(cur_ipa)
    if os.path.isfile(cur_xcarchive):
        os.remove(cur_xcarchive)
    os_ret = os.system("xcodebuild clean -configuration Release -target " + target)
    if os_ret == 2:
        print("\n [Ctrl + C] 您终止了打包过程!")
        sys.exit(2)
    print("清理工程完毕!")

    # create .xcarchive
    print("------------------------------xcarchive--------------------------------")
    print('xcodebuild -scheme {0} -archivePath {1} archive PROVISIONING_PROFILE_SPECIFIER=\'{2}\' PRODUCT_BUNDLE_IDENTIFIER=\'{3}\' DEVELOPMENT_TEAM=\'{4}\' CODE_SIGN_IDENTITY=\'{5}\' '.format(target,cur_xcarchive,sign_info[1],bundleid,sign_info[4],sign_info[0]))
        
    str_create_xcarchive = 'xcodebuild -scheme {0} -archivePath {1} archive PROVISIONING_PROFILE_SPECIFIER=\'{2}\' PRODUCT_BUNDLE_IDENTIFIER=\'{3}\' DEVELOPMENT_TEAM=\'{4}\' CODE_SIGN_IDENTITY=\'{5}\' '.format(target,cur_xcarchive,sign_info[1],bundleid,sign_info[4],sign_info[0])
    os_ret = os.system(str_create_xcarchive)
    if os_ret == 2:
        print("\n [Ctrl + C] 您终止了打包过程!")
        sys.exit(2)

    # build ipa
    print("------------------------ipa--------------------------")
    print('xcodebuild -exportArchive -exportOptionsPlist ./export.plist -archivePath {0} -exportPath {1} PROVISIONING_PROFILE=\'{2}\' CODE_SIGN_IDENTITY=\'{3}\' '.format(cur_xcarchive,cur_ipa,sign_info[2],sign_info[0]))
    os_ret = os.system('xcodebuild -exportArchive -exportOptionsPlist ./export.plist -archivePath {0} -exportPath {1} PROVISIONING_PROFILE=\'{2}\' CODE_SIGN_IDENTITY=\'{3}\' '.format(cur_xcarchive,cur_ipa,sign_info[2],sign_info[0]))
    if os_ret == 2:
        print("\n [Ctrl + C] 您终止了打包过程!")
        sys.exit(2)


def build_plist():
    # 构建exportarchive时使用的plist文件
    # 目测只需要method、provisioningProfile这两个参数，使用workspace的工程可能还需要teamID
    # readPlist获得的格式为：{'method': 'enterprise', 'provisioningProfiles': {'com.ledo.ahlm2.tw': 'anhei2 tw inhouse201708'}}
    method = ''
    if 'dis' in sys.argv[2]:
        method = 'app-store'
    elif 'adhoc' in sys.argv[2]:
        method = 'ad-hoc'
    elif 'inhouse' in sys.argv[2]:
        method = 'enterprise'

    bundle_id = signs[sys.argv[2]][3]
    provisioning = signs[sys.argv[2]][2]
    pl = plistlib.readPlist('export.plist')
    pl['method'] = method
    pl['provisioningProfiles'] = {bundle_id: provisioning}
    try:
        plistlib.writePlist(pl, 'export.plist')
    except Exception as e:
        print(e)


def build():
    if len(sys.argv) != 4:
        print("［参数错误］用法：python build-ios.py uc inhouse 3.3.0")
        return
    
    target = sys.argv[1]
    sign_name = sys.argv[2]
    version = sys.argv[3]
    bundleid = signs[sign_name][3]

    print "-------------"
    print target
    print sign_name
    print version
    print bundleid
    print "-------------"
    if sign_name not in signs:
        print "[签名配置错误] 请修改配置！"
        return
    if target not in plists:
        print "[target 错误] 请修改配置！"
        return
    if not os.path.isfile(plists[target][1]):
        print "[plist 配置错误]：" + plists[target][1]
        return
    build_plist()
    set_info(plists[target][0], plists[target][1],version,bundleid)
    build_target(target, plists[target][0], signs[sign_name], plists[target][1], version, bundleid)

if __name__ == '__main__':
    build()
   
