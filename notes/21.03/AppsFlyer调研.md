[TOC]

# AppsFlyer调研

## 广告投放步骤

1. 注册一个新的 AppsFlyer 帐户或添加团队成员到现有帐户。
2. 在AppsFlyer控制面板中添加应用，可以使用商店链接或者应用链接。
3. 下载并集成SDK：针对Android、iOS、Windows 手机、Unity以及其他安卓平台的集成指南。
4. 集成测试。
5. 开始归因投放。



### 归因链接（监测链接）

#### 广告参数相关

| 参数          | 原始数据中的显示名称 | 释义                                                         | 字段类型   |
| :------------ | :------------------- | :----------------------------------------------------------- | :--------- |
| pid           | 媒体渠道             | AppsFlyer集成合作伙伴的唯一标识不要更改它[更多详情](https://support.appsflyer.com/hc/zh-cn/articles/207447163#why-is-pid-publisher-id-the-most-important-parameter)。 | String 50  |
| c             | 广告系列活动         | 广告系列名称-由广告主/发行商提供。名称长度超过100个字符的广告系列在控制面板上会被显示为"c_name_exceeded_max_length" | String 100 |
| af_prt        | 代理商               | 代理帐户名称-可以把激活归因给相应代理**注意** ：在启用**授权代理**之前，请勿使用此参数。 | String 50  |
| af_mp         | 不适用               | 启用后每次安装将回传给发行商营销合作伙伴。**注意** ：当前此参数仅与Pinterest Marketing Partners相关。 |            |
| clickid       | 不适用               | 广告平台唯一点击标识符                                       |            |
| af_siteid     | Site ID              | 广告平台的发行商ID                                           | String 24  |
| af_sub_siteid | 次级站点ID           | 次级广告平台／发行商ID                                       | String 50  |
| af_c_id       | 广告系列活动ID       | 由广告商/发行商提供                                          | String 24  |
| af_adset      | 广告集               | 由广告商/发行商提供广告集是广告系列和广告层次结构之间的中间层级。[查看更多](https://support.appsflyer.com/hc/zh-cn/articles/207447163#levels-of-data-granularity) | String 100 |
| af_adset_id   | 广告集ID             | 由广告商/发行商提供                                          | String 24  |
| af_ad         | 广告                 | 广告名称（[查看更多](https://support.appsflyer.com/hc/zh-cn/articles/207447163#levels-of-data-granularity)）-由广告主/发行商提供 | String 100 |
| af_ad_id      | 广告ID               | 由广告商/发行商提供                                          | String 24  |

#### 安卓相关

| advertising_id      | Advertising ID | 谷歌广告 ID-需要广告平台支持                      | 40 字符上限                     |
| ------------------- | -------------- | ------------------------------------------------- | ------------------------------- |
| sha1_advertising_id | 不适用         | 通过SHA1加密的谷歌广告ID-需要广告平台支持         |                                 |
| md5_advertising_id  | 不适用         | 通过SHA1加密的谷歌广告ID-需要广告平台支持         | 仅支持激活和重归因              |
| android_id          | Android ID     | 设备 Android _ id-需要广告平台支持                | 20 字符上限                     |
| sha1_android_id     | 不适用         | 通过SHA1加密的安卓设备ID-需要广告平台支持         |                                 |
| md5_android_id      | 不适用         | 使用MD5 加密的设备Android_id-需要广告平台支持     | 仅支持激活和重归因              |
| imei                | IMEI           | 设备 IMEI ID                                      |                                 |
| sha1_imei           | 不适用         | 使用SHA1加密的设备IMEI ID-需要广告平台支持        |                                 |
| md5_imei            | 不适用         | 使用MD5加密的设备IMEI ID-需要广告平台支持         |                                 |
| OAID                | OAID           | 打开匿名设备标识符                                | 自Android SDK版本4.10.3起可适用 |
| sha1_oaid           | 不适用         | 打开使用SHA1加密的匿名设备标识符-需要广告平台支持 | 自Android SDK版本4.10.3起可适用 |
| md5_oaid            | 不适用         | 打开使用MD5加密的匿名设备标识符-需要广告网络支持  | 自Android SDK版本4.10.3起可适用 |

#### iOS相关

| idfa            | IDFA                                                         | Use upper case. Requires ad network supportField type: 40 char max |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| idfv            | IDFV                                                         | Use upper case.                                              |
| af_ios_url      | Redirect iOS (iPhone or iPad) users to a different URL than the app page on iTunes | 此方法用于落地页引导。                                       |
| af_ios_fallback | 不适用                                                       | 为[iOS10.3用户](https://support.appsflyer.com/hc/zh-cn/articles/115002366466-iOS-10-3-Redirects)提供后备URL |
| sha1_idfa       | 不适用                                                       | IDFA hashed with SHA1. Requires ad network support           |
| sha1_idfv       | 不适用                                                       | IDFV hashed with SHA1                                        |
| mac             | 不适用                                                       | mac 设备地址。需要广告平台支持。                             |
| md5_idfv        | 不适用                                                       | IDFV hashed with MD5                                         |
| sha1_mac        | 不适用                                                       | 通过SHA1加密的mac设备地址。需要广告平台支持                  |

#### publisher ID (PID) ， 类似于ad_id

在所有的归因链接参数里，只有PID是**唯一的每个归因链接都必须有的参数。**

PID-发布平台ID实际上是媒体渠道的名称。这是把安装归因给其来源的主要字段。

#### 数据粒度

1. 广告平台 (pid=)
2. 广告系列名称(c=)
3. 广告集 (af_adset=)
4. 广告名称 (af_ad=)

类似于广告组、广告计划等。

### SDK集成相关

应用程序嵌入SDK后，您可以记录安装，会话和其他应用内事件（例如，应用内购买，游戏级别等）来评估用户参与度，甚至投资回报率！

#### 应用内事件

记录App激活后的后续事件，例如登录，注册，应用内购买，并归因给对应的媒体平台和广告系列等。针对每个事件，都可以发送给AppsFlyer具体的事件参数和事件值。af针对各种行业和各类事件都提供了非常详细的API。

比如完成注册就会调用一次af的SDK

<img src="/Users/dongzhonghua03/Library/Application Support/typora-user-images/image-20210321141317382.png" alt="image-20210321141317382" style="zoom: 50%;" />

#### 服务器到服务器事件S2S

使用服务器到服务器API将app外发生的事件直接发送到AppsFlyer。例如，如果您有一个同时在Web端和移动端上均处于活跃状态的用户，则可以记录来自两个来源的事件，并可以在AppsFlyer将事件分配给的同一用户。它可以是应用内事件，也可以是其他事件

#### OneLink



#### 通过sdk获取归因数据

通过设置监听函数，可以实时的获取归因数据

####  归因

必须收集至少一个唯一标识符以进行归因。可获得以下标识符：GAID、Android ID、IMEI和OAID。

可以归因给第三方应用商店，GooglePlay，预装应用。

可以检测卸载率。

用户邀请归因。

### 广告效果看板





## 归因模型介绍

<img src="/Users/dongzhonghua03/Pictures/AppsFlyer_AttributionFlow_us-en.png" alt="AppsFlyer_AttributionFlow_us-en.png"  />



### 归因方法

| Attribution method                         | Android(Google Play and alternative app stores) | iOS  | Universal Windows Platform (UWP) |
| :----------------------------------------- | :---------------------------------------------- | :--- | :------------------------------- |
| Referrer（？？？？？）                     | Yes*                                            | No   | Yes                              |
| Device ID (advertising ID) matching        | Yes                                             | Yes  | Yes                              |
| 概率模型                                   | Yes                                             | Yes  | No                               |
| 电视归因                                   | Yes                                             | Yes  | Yes                              |
| * Supported by some alternative app stores |                                                 |      |                                  |

#### 安装引用程序

从Google Play和部分第三方应用商店下载的安卓应用通常通过referrer归因。referrer会提供跳转到安卓应用商店之前的原始URL。这是安卓端归因的主要方法。

#### 设备 ID 匹配

可以访问用户设备的广告平台会通过Click URL，或者在通知AppsFlyer他们已展示过广告时，把设备ID发送给AppsFlyer。这使得AppsFlyer可以将发生广告互动的设备 ID 与 AppsFlyer SDK 获取的设备 ID进行匹配。

设备 ID 匹配是 iOS 上的主要归因方法。

可用的 ID有:

- **iOS devices**: IDFA
- **Android设备：具有Google Play服务：** GAID
- **没有Google Play服务的Android设备：** OAID，Android ID，IMEI，Fire ID

归因链接上的设备ID可以使用SHA1或MD5进行加密处理。

#### 自归因平台的设备ID匹配

??这部分还有点疑问，自归因平台先归因然后af去请求？

首次启动应用程序时，AppsFlyer会检查应用程序设置，判断是否有来自自归因平台（SRNs）（例如Facebook，Snapchat和Google Ads）的流量。

AppsFlyer会使用新增激活的唯一设备 ID 去查询该应用配置的所有自归因平台。这是通过SRN授权AppsFlyer使用的MMP (移动监测合作伙伴) API完成的。根据返回的结果, AppsFlyer 可以将新增激活归因给相应的SRN。

#### 概率模型（类似ipua）

1. 包括与设备相关的参数，例如IP地址（IPV4或IPV6）和OS版本。 
2. 是一种不基于唯一ID的统计方法。 
3. 如果Referrer或ID匹配发生在回溯窗口内，则这些点击将会丢失。
4.  AppsFlyer会根据用户网络和唯一性IP地址唯一性动态确定归因窗口。窗口持续时间是自适应的，但比其他方法的窗口短（最多24小时）。

![IP_uniqueness.png](/Users/dongzhonghua03/Pictures/IP_uniqueness.png)

#### 电视归因

#### 预装归因

只通过af sdk上报的数据进行归因。

#### 卸载重装

如果激活该该应用，后来又卸载，然后在初始安装日期的再归因窗口期过去后再次激活该应用不会判定为是新设备。

在再归因窗口期（默认是90天）内再次安装应用的用户会被记为再归因。

### 用户互动归因类型

#### 点击型归因

大多数归因于移动设备的激活来自用户对广告的点击，例如横幅，视频和插屏广告。

在广告点击时, AppsFlyer 会打开一个点击归因回溯窗口期, 默认窗口期是7天，AppsFlyer 建议使用7天的点击归因窗口期。发生在该窗口期内的激活会被认为是非自然激活并归因给相应的媒体渠道。超过该窗口期的激活会被认为是自然激活。

#### 浏览型归因

用户查看移动广告但未点击移动广告，新增激活可归因于展示广告的媒体渠道。浏览型归因的回溯窗口期比点击型归因的回溯窗口期短。窗口期是可配置的。

### 卸载评估（卸载归因）

AppsFlyer 每天使用一次无声推送通知来验证仍在用户设备上安装了应用程序，并统计 特定 app 发生的卸载事件，并将它们归因于特定媒体渠道。好处有两个：

1. 可以对比各个广告，媒体，地域等等的广告效果。
2. 如果用户卸载之后就不会再次推送相似的广告了，可以保护用户的隐私。（或者卸载之后也可以再次精准推送广告？）

### 为什么AppsFlyer可能会显示比应用商店更少的安装？

| 原因                                                 | iTunes / Google Play                                         | AppsFlyer                                                    | AppsFlyer 的提示                                             |
| :--------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| ** 对安装的定义 **                                   | 一旦用户下载并安装应用程序，应用程序商店就会记录安装，无论用户是否稍后启动应用程序。 | AppsFlyer仅在首次启动时记录新安装。**从未启动的用户不会计入AppsFlyer**，即使他们下载并安装（通过应用商店定义）。 | 所有移动应用下载中的90％至少会打开 App 一次。但是，这在不同的地理位置和领域会有很大差异。 |
| **安装记录日期**                                     | 应用商店将下载日期记录为安装日期                             | AppsFlyer 将首次启动的日期记录为安装日期                     | 在 AppsFlyer 的控制面板上使用较长的时间作为您查询的日期范围, 以最大限度地减少这种差异。 |
| **时区**                                             | 数据将根据广告主的本地时区显示。                             | 默认情况下, 数据以 UTC±00:00时区显示。                       | 您可以为自己拥有的每个应用设置首选时区, 并最大限度地减少这种差异 |
| **Android 用户卸载并在定义的重新归因窗口中重新安装** | 有时, Google Play 为同一用户显示**两个唯一安装**, 而不考虑第一次安装所需的时间。另外的时候显示唯一的用户, 因此与 AppsFlyer 差异较小。 | 在重新归因窗口内 (默认情况下, 从原始安装开始 3个月) 中, AppsFlyer 不会重新归因安装。 | 您可以[将重新归因窗口设置为1到24个月。                       |

### 为什么AppsFlyer可能会显示比应用商店更多的安装？

| 原因                                               | description                                                  | AppsFlyer 的提示                                             |
| :------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **升级现有应用安装**                               | 如果应用在没有 AppsFlyer SDK 的情况下发布, 然后在应用程序商店中重新发布, 并集成了 AppsFlyer SDK, 则 AppsFlyer 会显示了较多的新自然安装。 | 当大多数用户完成应用程序升级时, 此峰值通常会在几天后下降。   |
| **用户的多个设备安装相同的应用程序**               | 当一个应用安装在同一 iTunes 用户的 iPhone 和 iPad 上时, iTunes 认为这是一次安装, 而 AppsFlyer 则认为这是两个安装。 | 您可以使用 customer user ID 值跟踪这些 "双重" 安装。如果为每个新用户生成唯一的 customer user ID, 并对同一用户的所有安装使用相同的值, 则可以从原始数据安装报告中筛选出重复的 customer user ID, 这将消除这种差异的原因。 |
| **iOS 用户卸载并在定义的再归因窗口之外的重新安装** | 当重新归因窗口 (默认情况下 3个月) 从原始安装时间经过时, 用户在重新安装时被视为 AppsFlyer 上的新窗口。 但是, 无论卸载和重新安装如何, iTunes 仅显示每个用户的一次安装。 | 您可以将重新归因窗口设置为1到24个月。                        |
| **用户在升级后的设备上重新安装**                   | 对商店来说是相同用户, 但对 AppsFlyer 来说是不同设备。        | AppsFlyer 显示已停止工作的第一个设备的卸载信息。             |
| **设备 ID 重置和限制广告跟踪 (LAT) 欺诈**          | 超过50%的欺诈安装使用这些方法, 导致设备显示为新设备, 而对于商店, 用户保持不变。 | AppsFlyer 的 Protect360 反欺诈解决方案可以很容易地检测到你的应用是否有这些类型的欺诈。 |
| **从 Google Play 中安装**                          | 在店外市场, 预安装和 APK 网站提供安装, 而不是通过 Google Play。 | 如果你在店外的 Android 市场上做广告, 请查阅文档以进行正确的设置。 |



### 再营销广告归因

使用deeplink和onelink跳转来进行**老用户唤醒(Re-engagement)** ，**老用户召回（重新安装）**。

### 针对国内的归因方案

针对国内安卓市场的特殊性，广告主通常面临如下挑战：

- Google Play服务（GPS）在大多数Android设备上无效，也就意味着没有GAID。
- 国内安卓生态中大量第三方应用内市场的存在为商店劫持提供了机会。
- 服务器响应时效可能偏慢
- 如果同时投放海外和国内市场，如何同时管理Google Play和国内第三方应用内商店的数据也是一大挑战。

AppsFlyer为您提供了以下解决方案： 

- 适配主流厂商OAID
- 鉴于国内安卓生态不会使用GAID，我们将根据 OAID 或设备IMEI进行归因，以替代GAID
- 除了提供归因的媒体渠道字段，还会提供商店/渠道包字段，保证每一条激活数据包含用户完整转化路径：从渠道的点击/曝光数据，到最终APK下载来源，可以轻松识别商店劫持
- 配置为中国市场专门制定的归因链接（即点击监测链接）。

## 报告

AppsFlyer提供的自定义汇总数据报告API功能可以根据您的需求生成专属于您的数据报告，无论您需要的是LTV维度分析、留存分析、群组用户分析、活跃用户分析，或是基于Protect360的假量分析，无论您是想分析一个APP、或是多个APP

花费、点击、impression、impression、ROI、次留率和平均eCPI数据会在**Aggregated Performance Report**表格显示，同时也可以通过下载**Partners** 和 **Partners by Date** CSV报告进行查看。

![undefined](/Users/dongzhonghua03/Pictures/pivot_media_source_result.png)

### af和SKAdNetwork

#### SKAdNetwork 数据传输流程

[![PostbackProcess_us-en.png](https://support.appsflyer.com/hc/article_attachments/360012267537/PostbackProcess_us-en.png)](https://support.appsflyer.com/hc/article_attachments/360012267537/PostbackProcess_us-en.png)

 完整的SKAdNetwork回调流程主要有以下几步： 

1. **iOS**设备先将SKAdNetwork回调发给对应被归因的广告平台

2. 广告平台

    可选择下列两种方式的的任意一种：

    - **补充数据维度并转发：**广告平台添加广告系列ID(来解决SKAdNetwork限制至多100个campaign ID的问题），广告系列名称，iOS设备所在IP地址等信息细化回调
    - **重定向：** 广告平台让iOS直接将回调重定向发送给AppsFlyer。在这种情形下，广告系列数据的维度补充会通过AppsFlyer以及广告平台间一个单独的API来进行

3. **AppsFlyer**会对回调进行验证和反编译然后将包含更为详尽信息的回调发回给广告平台（并同时同步给广告主）

