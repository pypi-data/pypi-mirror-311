<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>


<div align="center">


# nonebot-plugin-hyp

_✨ NoneBot X Hypixel小游戏服务器数据查询插件✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/Reversedeer/nonebot_plugin_hyp/main/LICENSE">
  	<img src="https://img.shields.io/github/license/Reversedeer/nonebot_plugin_hyp" alt="license">
  </a>
  <a href="https://pypi.org/project/nonebot-plugin-eventmonitor">
	<img src="https://img.shields.io/pypi/v/nonebot-plugin-hyp?logo=python&logoColor=edb641" alt="pypi">
  </a>
  	<img src="https://img.shields.io/badge/python-3.9+-blue?logo=python&logoColor=edb641" alt="python">
  <a href="https://nonebot.dev/">
    <img src="https://img.shields.io/badge/NoneBot2-blue?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="Nonebot2">
  </a>
</p>




## 介绍:

> 一款旨在查询全球最大的小游戏服务器"Hypixel"玩家游戏数据信息及Minecraft-Mojang数据的插件
>
> 服务器内各种游戏数据，包括但不限于(Bedwars, Skywars, Skyblock...)
>
> 可查询自己及朋友或任何人已公开的数据
>
> 借助Antisniper 提供的api我们可以查询更多的数据

> [!WARNING]
>
> /hypapi 指令请谨慎使用，此指令会发送当前使用的API, 鉴于现在API有一定的获取难度，我们不推荐随意使用
>
> 指令使用帮助仅展示受支持的指令，已实现的指令请看相关文件

## 安装方式

### nb-cli

```python
nb plugin install nonebot-plugin-hyp
```

### pip


```python
pip install nonebot-plugin-hyp
```

### update：

```python
pip install --upgrade nonebot-plugin-hyp
```

## 配置

|      config       | type |    default    |               example               | usage | 是否必须 |
| :---------------: | :--: | :-----------: | :---------------------------------: | :---: | :------: |
|  hypixel_apikey   | int  | 1145141919810 |  hypixel_apikey = '1145141919810'   |  API  |    是    |
| antisniper_apikey | int  | 1145141919810 | antisniper_apikey = '1145141919810' |  API  |    否    |

## 指令结构帮助：

```
usage = """
    help 显示指令列表
    mc|minecraft|profile|skin|mcskin <玩家> 查询玩家 Minecraft 信息
    mcuuid|uuid <UUID> 查询 UUID 玩家信息
    hyp|hypixel <玩家> [游戏] 查询 Hypixel 信息
    hypapi 查询当前使用的 API Key 信息
    ban|bans|punishment|punishments 查询封禁信息
    bw|bedwar|bedwars <玩家> [模式] 查询起床战争数据
    sw|skywar|skywars <玩家> 查询空岛战争数据
    mw|megawall|megawalls <玩家> 查询超级战墙数据
    duel|duels <玩家> [模式] 查询决斗游戏数据
    bsg|blitz <玩家> 查询闪电饥饿游戏数据
    uhc <玩家> 查询 UHC 数据
    mm|murder <玩家> 查询密室杀手数据
    tnt|tntgame|tntgames <玩家> 查询掘战游戏数据
    pit <玩家> 查询天坑之战数据
    gname|guildname <公会名称> 查询公会
    g|guild <玩家> 查询玩家所在公会
    bwshop|bwfav <玩家> 查询玩家起床战争商店
    denick <Nick> 查询 Nick (Antisniper)
    findnick <玩家> 查找 Nick (Antisniper)
    ws|winstreak <玩家> 查询起床战争普通模式连胜 (Antisniper)
    wsall|winstreakall <玩家> 查询起床战争其他模式连胜 (Antisniper)
    wshyp <玩家> 查询起床战争普通模式连胜 (Hypixel)
    wsallhyp <玩家> 查询起床战争其他模式连胜 (Hypixel)
    ofcape|optifine <玩家> 查询 OptiFine 披风
    """
```

## TODO

- [ ] 创建指令列表帮助
- [ ] 增加玩家数据缓存
- [x] 查询api 当前使用的API Key信息
- [x] 查询玩家 Minecraft 信息及UUID
- [x] 查询hypixel 个人信息
- [x] 查询bedwars 起床战争数据
- [x] 查询skywars 空岛战争数据
- [ ] 查询megawalls 超级战墙数据
- [ ] 查询duels 决斗游戏数据
- [ ] 查询blitz 闪电饥饿游戏数据
- [ ] 查询UHC 游戏数据
- [ ] 查询murder 密室杀手游戏数据
- [ ] 查询tntgames 掘战游戏数据
- [ ] 查询pit 天坑之战游戏数据
- [ ] 查询guildname 公会
- [ ] 查询guild 玩家所在公会
- [ ] 查询bwfav 玩家起床战争商店
- [ ] 查询 denick 查询玩家Nick（Antisniper）
- [ ] 查询findnick 查找Nick（Antisniper）
- [ ] 查询winstreak 起床战争普通模式连胜（Antisniper）
- [ ] 查询winstreakall 起床战争其他模式连胜（Antisniper）
- [ ] 查询wsall 查询玩家起床战争普通模式连胜（Hypixel）
- [ ] 查询wshyp 起床战争其他模式连胜（Hypixel）
- [ ] 查询optfine OptFine披风
- [ ] 查询bans Hypixel今日封禁信息

<details>
    <summary><h2>更新日志</h2></summary>


- v0.0.4
  - ✨使用Pydantic管理插件配置项

- v0.0.1
  - ✨增加minecraft个人信息查询
  - ✨增加hypixel个人数据查询
  - ✨增加bedwars查询
  - ✨增加skywars查询
  - ✨增加apikey查询


  </details>


## 关于 ISSUE

以下 ISSUE 会被直接关闭

- 提交 BUG 不使用 Template
- 询问已知问题
- 提问找不到重点
- 重复提问

> 请注意, 开发者并没有义务回复您的问题. 您应该具备基本的提问技巧。  
> 有关如何提问，请阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)

## 其他插件

[nonebot-plugin-dog(获取舔狗文案，汪！)](https://github.com/Reversedeer/nonebot_plugin_dog)

[nonebot_plugin_eventmonitor(群荣誉事件检测)](https://github.com/Reversedeer/nonebot_plugin_eventmonitor)