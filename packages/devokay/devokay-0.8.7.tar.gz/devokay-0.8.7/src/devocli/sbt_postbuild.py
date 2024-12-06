# -*- coding: UTF-8 -*-
# python3

import sys

# PC SDK build tool

from devolib import DynamicObject
from devolib.util_log import LOG_D, LOG_E, LOG_W, LOG_I
from devolib.util_os import get_env_var, current_dir
from devolib.util_str import ends_with, str_to_bytes, bytes_to_str
from devolib.util_argparse import typeparse_list, typeparse_str2bool
from devolib.util_httpc import POST_JSON, GET_JSON
from devolib.util_crypt import sim_cipher_decrypt, aes_encrypt_without_b64, aes_decrypt_without_b64
from devolib.util_fs import path_join_one, write_bytes_to_file, path_exists, read_bytes_of_file, write_file, touch_dir, copy_files, copy_dir, remove_files
from devolib.util_json import json_to_str
from devolib.consts import ENV_DEV, ENV_TEST, ENV_PROD

# MARK: Consts

SDK_BUILD_HOST = "SDK_BUILD_HOST"
SDK_BUILD_TOKEN = "SDK_BUILD_TOKEN"

CIPHER_FOR_CIPHER_BYTES = [0xc7, 0xc4, 0xc5, 0xda, 0xcb, 0xcf, 0xcc, 0xcd, 0xc2, 0xc3, 0xc0, 0xc4, 0xc5, 0xda, 0xdb, 0xd8]
CIPHER_FOR_CIPHER_SALT = 0xAA
CIPHER_FOR_CIPHER_IV = [0x9b, 0x98, 0xcb, 0xcb, 0xec, 0xee, 0xf9, 0xeb, 0xc1, 0xcb, 0xc7, 0xcc, 0xce, 0xd9, 0xcb, 0x9b]

# MARK: Utils

def conf_is_wegame(conf_json): # conf = conf_json["data"]
    conf = conf_json["data"]
    return conf["store_type"] == "wegame"

def conf_is_steam(conf_json):
    conf = conf_json["data"]
    return conf["store_type"] == "steam"

def conf_is_offcial(conf_json):
    conf = conf_json["data"]
    return conf["store_type"] == "offcial"

# MARK: Conf retrieve

def get_conf_data(params_str):
    if params_str != None:
        param_arr = params_str.split("-") # official-pc-10001
        host = get_env_var(SDK_BUILD_HOST)
        res_json = GET_JSON(
            host=f'https://{host}', 
            path='/pconf/pack', 
            query=f"app_id={param_arr[2]}&store_type={param_arr[0]}&platform={param_arr[1]}",
            headers={
                'Authorization': get_env_var(SDK_BUILD_TOKEN)
            })
        
        if res_json is None:
            raise Exception(f'get conf data failed.')

        code = res_json['code']
        if code != 200:
            raise Exception(f'get conf data failed, code: {code}')

        return res_json
    else:
        LOG_E('host empty')

        return None

# MARK: Build Stages

def stage_get_conf(params):
    conf_json = get_conf_data(params)

    LOG_W(f"[STAGE] conf json: {conf_json}")

    return conf_json

def stage_handle_files(conf_json, origin_dir, target_dir, is_strict_mode):
    # copy data dir
    # from dll_origin_dir to dll_target_dir
    LOG_D(f"copying `data`")

    origin_dir_data = f"{origin_dir}/data"
    target_dir_data = f"{target_dir}/data"
    copy_dir(src=origin_dir_data, dst=target_dir_data)
    
    # copy locales
    LOG_D(f"copying `locales`")
    origin_dir_locales = f"{origin_dir}/locales"
    target_dir_locales = f"{target_dir}/locales"
    copy_dir(src=origin_dir_locales, dst=target_dir_locales)

    # copy web
    LOG_D(f"copying `web`")
    copy_dir(src=f"{origin_dir}/web", dst=f"{target_dir}/web")

    # copy files
    LOG_D(f"copying `files`")
    extra_files = [
        f"{origin_dir}/chrome_100_percent.pak",
        f"{origin_dir}/chrome_200_percent.pak",
        f"{origin_dir}/icudtl.dat",
        f"{origin_dir}/limpcbrowser.exe",
        f"{origin_dir}/limpcbrowserex.exe",
        f"{origin_dir}/resources.pak",
        f"{origin_dir}/snapshot_blob.bin",
        f"{origin_dir}/v8_context_snapshot.bin",
        f"{origin_dir}/vk_swiftshader_icd.json"
    ]
    copy_files(file_paths=extra_files, output_dir=target_dir)

    # custom actions for different channels
    LOG_D(f"custom actions")

    if not conf_is_wegame(conf_json) and is_strict_mode:
        LOG_D(f"not wegame: deleting `rail_api64.dll`")
        to_delete_files = [
            f"{target_dir}/rail_api64.dll"
        ]
        remove_files(file_paths=to_delete_files)

    if not conf_is_steam(conf_json) and is_strict_mode:
        LOG_D(f"not steam: deleting `steam_api64.dll`")
        to_delete_files = [
            f"{target_dir}/steam_api64.dll"
        ]
        remove_files(file_paths=to_delete_files)

def stage_save_conf(conf_json, target_dir, need_encrypt, env_key): # 加密配置数据，保存在指定目录
    global CIPHER_FOR_CIPHER_BYTES, CIPHER_FOR_CIPHER_SALT

    # conf_data_encrypt
    # sim_cipher_encrypt
    LOG_D(f"target_dir: {target_dir}")

    file_name = "pcsdk.json"
    if (env_key is not None) and (len(env_key) > 0):
        file_name = f"pcsdk-{env_key}.json"
    conf_file_path = path_join_one(target_dir, file_name)

    LOG_D(f"conf_file_path: {conf_file_path}")

    cipher_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_BYTES, salt=CIPHER_FOR_CIPHER_SALT)
    iv_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_IV, salt=CIPHER_FOR_CIPHER_SALT)

    conf_json_str = json_to_str(conf_json)

    LOG_D(f"conf_json_str: {conf_json_str}")

    if need_encrypt:
        conf_str_encrypted = aes_encrypt_without_b64(conf_json_str, cipher_decrypted, iv_decrypted)

        write_bytes_to_file(conf_file_path, conf_str_encrypted)
    else:
        write_file(conf_file_path, conf_json_str)

    if path_exists(conf_file_path):
        LOG_I(f"conf path exists: {conf_file_path}")
    else:
        LOG_E(f"conf path not exists")

# MARK: Command Handle

def cmd_handle_build_store(args):
    LOG_D(f'params: {args.params}')
    LOG_D(f'origin: {args.origin}')
    LOG_D(f'target: {args.target}')
    LOG_D(f'encrypt: {args.encrypt}')
    LOG_D(f'encrypt: {args.strict}')

    if args.params is None:
        raise Exception("params is None")
    params_arr = args.params.split(",")
    if len(params_arr) == 0:
        raise Exception("params is empty")
    
    for params in params_arr:
        env_key = params
        conf_json = stage_get_conf(env_key)

        if args.origin != None and len(args.origin) != 0:
            stage_handle_files(conf_json, args.origin, args.target, args.strict)

        if args.target == None or len(args.target) == 0:
            args.target = current_dir()

        touch_dir(args.target) # touch target dir

        if len(params_arr) == 0:
            env_key = None
        stage_save_conf(conf_json, args.target, args.encrypt, env_key)

    sys.exit()

def cmd_handle_tools_decrypt(args):
    if args.path is not None:
        file_path = args.path
        decrypted_file_path = f"{file_path}.decrypted"

        LOG_D(f"file_path: {file_path}")
        LOG_D(f"decrypted_file_path: {decrypted_file_path}")

        cipher_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_BYTES, salt=CIPHER_FOR_CIPHER_SALT)
        iv_decrypted = sim_cipher_decrypt(cipher_bytes=CIPHER_FOR_CIPHER_IV, salt=CIPHER_FOR_CIPHER_SALT)

        encrypted_bytes = read_bytes_of_file(file_path)
        decrypted_bytes = aes_decrypt_without_b64(encrypted_bytes, cipher_decrypted, iv_decrypted)
        write_bytes_to_file(decrypted_file_path, decrypted_bytes)
    else:
        LOG_E(f"none file is processed.")

    sys.exit()

# MARK: Command Regist

def cmd_regist(subparsers):
    parser = subparsers.add_parser('pcs.build.store', help='pc sdk build tool for game build in postprocess.')
    parser.add_argument('-p', '--params', type=str, default=None, help='store params, E.g: offcial-pc-10001,official-pc-12001')
    parser.add_argument('-o', '--origin', type=str, default=None, help='origin full path')
    parser.add_argument('-t', '--target', type=str, default=None, help='target full path')
    parser.add_argument('-s', '--strict', type=typeparse_str2bool, default=True, help='if strict, then file cropping.')
    parser.add_argument('-enc', '--encrypt', type=typeparse_str2bool, default=True, help='need encrypt or not')
    parser.set_defaults(handle=cmd_handle_build_store)

    parser = subparsers.add_parser('sbt.tools.decrypt', help='pc sdk tools for file decryption.')
    parser.add_argument('-p', '--path', type=str, default=None, help='encrypted file path, default search current dir for `pcsdk.json` file.')
    parser.set_defaults(handle=cmd_handle_tools_decrypt)

    # SDK Build Tool
    parser = subparsers.add_parser('sbt.postbuild_pcsdk_unity', help='SDK Build Tool for postbuilding pcsdk in unity.')
    parser.add_argument('-p', '--params', type=str, default=None, help='store params, E.g: offcial-pc-10001,official-pc-12001')
    parser.add_argument('-o', '--origin', type=str, default=None, help='origin full path')
    parser.add_argument('-t', '--target', type=str, default=None, help='target full path')
    parser.add_argument('-e', '--encrypt', type=typeparse_str2bool, default=True, help='need encrypt or not')
    parser.add_argument('-s', '--strict', type=typeparse_str2bool, default=True, help='if strict, then file cropping.')
    parser.set_defaults(handle=cmd_handle_build_store)

# python src/devocli/pcs_postbuild.py
if __name__ == '__main__':
    # args = DynamicObject(params='official-pc-10001', origin='', target='/Users/fallenink/Desktop/Developer/devokay-py/tmp', encrypt=True)
    # cmd_handle_build_store(args)

    args = DynamicObject(path="/Users/fallenink/Desktop/Developer/devokay-py/tmp/pcsdk.json")
    cmd_handle_tools_decrypt(args)