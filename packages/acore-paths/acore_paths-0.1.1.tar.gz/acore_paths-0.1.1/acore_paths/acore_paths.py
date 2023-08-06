# -*- coding: utf-8 -*-

"""
Todo: doc string here
"""

from pathlib import Path

dir_home = Path.home()

# ------------------------------------------------------------------------------
# Azerothcore Server
# 跟游戏服务器相关的路径
# ------------------------------------------------------------------------------
# 用 https://github.com/azerothcore/azerothcore-wotlk 编译好后的游戏服务器的根目录
# ${HOME}/azeroth-server/
dir_azeroth_server = dir_home / "azeroth-server"

# 游戏服务器里的所有可执行文件的目录
# ${HOME}/azeroth-server/bin/
dir_server_bin = dir_azeroth_server / "bin"

# 由 Azerothcore 团队提供的登录服务器的默认配置文件模板, 用于留档, 勿动
# ${HOME}/azeroth-server/etc/authserver.conf.dist
path_azeroth_server_authserver_conf_dist = (
    dir_azeroth_server / "etc" / "authserver.conf.dist"
)

# 由 Azerothcore 团队提供的世界服务器的默认配置文件模板, 用于留档, 勿动
# ${HOME}/azeroth-server/etc/worldserver.conf.dist
path_azeroth_server_worldserver_conf_dist = (
    dir_azeroth_server / "etc" / "worldserver.conf.dist"
)

# 最终的登录服务器的配置文件, 由模板和自定义改动合并而成
# ${HOME}/azeroth-server/etc/authserver.conf
path_azeroth_server_authserver_conf = dir_azeroth_server / "etc" / "authserver.conf"

# 最终的世界服务器的配置文件, 由模板和自定义改动合并而成
# ${HOME}/azeroth-server/etc/worldserver.conf
path_azeroth_server_worldserver_conf = dir_azeroth_server / "etc" / "worldserver.conf"

# 游戏服务器的数据文件, 主要是地图数据, 以下载 data.zip 后要把解压出来的文件放在这里
# 最终如果有 ${HOME}/azeroth-server-data/maps/ 的目录就说明你解压的地方对了
# 注意最终你要更新 worldserver.conf 里的 DataDir 字段, 填入 **绝对路径**
# ${HOME}/azeroth-server-data/
dir_azeroth_server_data = dir_home / "azeroth-server-data"

# 在 https://github.com/wowgaming/client-data/releases/ 下载的最新地图数据文件
# ${HOME}/azeroth-server-data/data.zip
dir_azeroth_server_data_dot_zip = dir_azeroth_server_data / "data.zip"

# 游戏服务器的日志文件目录
# ${HOME}/azeroth-server-logs/
dir_azeroth_server_logs = dir_home / "azeroth-server-logs"

# ------------------------------------------------------------------------------
# Azerothcore Server modules
# 跟模组相关的路径
# ------------------------------------------------------------------------------
# 所有的模组都在这个目录下
# ${HOME}/azeroth-server/etc/modules/
dir_modules = dir_azeroth_server / "etc" / "modules"

# ------ Eluna: https://github.com/azerothcore/mod-eluna
# Eluna 模组的配置文件模板, 用于留档, 勿动
# ${HOME}/azeroth-server/etc/modules/mod_LuaEngine.conf
path_mod_eluna_conf_dist = dir_modules / "mod_LuaEngine.conf.dist"

# Eluna 模组的最终配置文件, 由模板和自定义改动合并而成
# ${HOME}/azeroth-server/etc/modules/mod_LuaEngine.conf.dist
path_mod_eluna_conf = dir_modules / "mod_LuaEngine.conf"

# Eluna 模组所有的 Lua 脚本的目录, 你的自定义 Lua 脚本都要放在这里
# 注意最终你要更新 mod_LuaEngine.conf 里的 Eluna.ScriptPath 字段, 填入 **绝对路径**
# ${HOME}/azeroth-server/bin/lua_scripts/
dir_server_lua_scripts = dir_server_bin / "lua_scripts"
