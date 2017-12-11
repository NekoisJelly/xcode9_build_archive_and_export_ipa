# coding=utf-8
#!/usr/bin/env python
# useage:
#
#   python build-ios.py apple inhouse 3.3.0  (打包某个渠道)
#   python build-ios.py apple dis 3.3.0 (打包某个渠道)
#
#

import os
import sys
import plistlib
import re


# 设置签名信息,bxzw
signs = {   'apple_inhouse':("iPhone Distribution: XXXXXXX Co., Ltd.", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "provisioningProfiles_name",'com.apple.inhouse','xxxxxxxxxx'),
            'apple_dis':("iPhone Distribution: xxxxxxx (UE2Dxxxxxx)", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "provisioningProfiles_name",'com.apple.dis','UE2Dxxxxxx'),
            'apple_adhoc':("iPhone Distribution: xxxxxxx (UE2Dxxxxxx)", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "provisioningProfiles_name",'com.apple.adhoc','UE2Dxxxxxx'),
        }

# 设置渠道plist文件相对路径
plists = {  "apple":("target_ios_apple", "./target_ios_apple-Info.plist"),
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
        if get_xcode_version() == '7':
        print('xcodebuild -scheme {0} -archivePath {1} archive PROVISIONING_PROFILE=\'{2}\' PRODUCT_BUNDLE_IDENTIFIER=\'{3}\' DEVELOPMENT_TEAM=\'{4}\' CODE_SIGN_IDENTITY=\'{5}\' '.format(target,cur_xcarchive,sign_info[1],bundleid,sign_info[4],sign_info[0]))
        
        str_create_xcarchive = 'xcodebuild -scheme {0} -archivePath {1} archive PROVISIONING_PROFILE=\'{2}\' PRODUCT_BUNDLE_IDENTIFIER=\'{3}\' DEVELOPMENT_TEAM=\'{4}\' CODE_SIGN_IDENTITY=\'{5}\' '.format(target,cur_xcarchive,sign_info[1],bundleid,sign_info[4],sign_info[0])
    elif get_xcode_version() == '9':
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
    # readPlist获得的格式为：{'method': 'enterprise', 'provisioningProfiles': {'com.apple.inhouse': 'provisioningProfiles_name'}}
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


def get_xcode_version():
    r = os.popen('xcode-select -p').read()
    s = re.sub(r'Developer\n','version.plist', r)
    pl = plistlib.readPlist(s)
    return pl['CFBundleShortVersionString'][0]


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
   
