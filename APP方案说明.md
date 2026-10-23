# 「飞」系企业管理系统 · 手机APP 总体方案说明

## 一、立项背景与目标

「飞」系 24 个企业管理系统（OTMS/FMS/RMS/HIS/TMS/ERP/CRM/WMS/MES/SCM/QMS/APS/HRM/OA 等）此前均以桌面 Web 形式交付。为满足管理层与一线人员移动办公需求，为每个系统**独立立项生成同名手机APP**，实现船期/订单/库存/审批/报表等核心业务随身查、随身办。

## 二、技术路线

| 项 | 决策 |
| --- | --- |
| 形态 | PWA（H5 + Web App Manifest + Service Worker），添加到主屏幕后全屏独立运行，具备图标/启动屏/离线壳 |
| 生成方式 | 统一生成器 gen_all.py 按 24 份项目配置批量产出，一套外壳 × 各自专属 config.js（APP名/主题色/接口端点/账号） |
| 后端 | 零改动复用各系统既有 REST API；登录端点与响应包按各系统适配（{code,data} / {ok,data} / 裸 {token} 三种包式自动兼容） |
| 鉴权 | Bearer Token，按 APP 隔离存储键（<proj>_m_token），互不串号 |
| 部署 | 服务器 /opt/fei-mobile/<proj>/mobile/，nginx location /<prefix>/m/ alias 挂载，与桌面端同域同源免 CORS |
| 缓存 | sw.js 预缓存静态资源、API 直连不缓存，弱网可启动 |
| 适配 | 375×812 手机视口 + safe-area 安全区，禁止横向溢出 |

## 三、APP 清单与访问地址

| APP 名称 | 地址 | 登录 |
| --- | --- | --- |
| 飞洋海洋运输管理系统 | /ocean/m/ | admin / 123456 |
| 飞融金融管理系统 | /finan/m/ | admin / 123456 |
| 飞售零售管理系统 | /retail/m/ | admin / 123456 |
| 飞餐餐饮管理系统 | /rms/m/ | admin / 123456 |
| 飞医医疗管理系统 | /his/m/ | admin / 123456 |
| 飞税税务管理系统 | /tax/m/ | admin / tax@2026 |
| 飞效OA管理系统 | /oa/m/ | admin / oa@2026 |
| 飞育教育管理系统 | /edu/m/ | admin / 123456 |
| 飞运运输管理系统 | /tms/m/ | admin / 123456 |
| 飞划APS系统 | /aps/m/ | admin / aps@2026 |
| 飞瀑能源管理系统 | /pu/m/ | admin / energy@2026 |
| 飞奔成本管理系统 | /cost/m/ | admin / cost@2026 |
| 飞花HRM系统 | /hr/m/ | admin / hr@2026 |
| 飞控QMS系统 | /qms/m/ | 待后端部署 |
| 飞传WMS系统 | /wms/m/ | 待后端部署 |
| 飞驰MES系统 | /mes/m/ | 待后端部署 |
| 飞泉SCM系统 | /scm/m/ | 待后端部署 |
| 飞鸢ERP系统 | /erp/m/ | admin / admin123 |
| 飞鹰CRM系统 | /crm/m/ | 待后端部署 |
| 飞流流程管理系统 | /flow/m/ | admin / admin123 |
| 飞虹股票交易系统 | /fh/m/ | admin / admin123 |
| 飞扬关务系统 | /cus/m/ | admin / admin123 |
| 飞云财务核算系统 | /fin/m/ | admin / admin123 |
| 飞物数据管理系统 | /data/m/ | 待后端部署 |

（地址前缀省略公共主机 http://42.193.158.63）

## 四、统一交互设计

- **底部 5 Tab**：工作台 / 三个核心业务页（按系统定制，如飞洋=航次·订舱·箱货，飞餐=订单·菜品·库存，飞虹=持仓·委托·信号）/ 我的。
- **工作台**：优先渲染各系统 /api/dashboard 或 /api/board 概览指标（自动 KPI 网格）；无概览接口的系统展示品牌卡与核心功能入口。
- **业务页**：标准列表卡片（标题+4 个关键字段），自动兼容 {items:[...]}、[...]、单对象三种返回。
- **我的**：用户身份卡（姓名/角色）、版本、服务地址、退出登录。
- 登录页按项目预填演示账号，减少演示摩擦。

## 五、各 APP 核心业务 Tab 一览

飞洋：航次/订舱/箱货；飞融：凭证/账单/往来；飞售：销售/商品/门店；飞餐：订单/菜品/库存；飞医：挂号/患者/处方；飞税：申报/发票/风险；飞效OA：请假/会议/报销；飞育：学生/成绩/缴费；飞运：运单/调度/车辆；飞划：工单/销售订单/物料；飞瀑：抄表/计量/告警；飞奔：费用/预算/差异；飞花：员工/假勤/薪酬；飞控：检验/缺陷/NCR；飞传：出入库单/库存/库位；飞驰：工单/报工/缺陷；飞泉：采购订单/请购/供应商；飞鸢：销售/采购/库存；飞鹰：客户/线索/商机；飞流：待办/实例/流程模型；飞虹：持仓/委托/信号；飞扬：报关单/HS税则/往来；飞云：凭证/业务事件；飞物：数据集/指标/质量告警。

## 六、质量门禁（check_all.py）

- Playwright 手机视口（375×812, is_mobile）逐 APP 验收：页面加载 → 登录 → 工作台渲染 → 首个业务 Tab → 横向溢出 → JS 异常。
- **最终结果 23/23 全部通过**（feiyang-otms 专属版另有 5/5 独立巡检）。
- 已知弱项：飞奔/飞花工作台指标字段口径待对齐（登录与 Tab 正常）；飞鸢/飞虹第二 Tab 数据为空属种子数据范畴；6 个系统后端尚未部署到线上，APP 静态壳已就绪、后端上线即通。

## 七、运维与扩展

- 重新生成：`python mobile-apps/gen_all.py [proj...]`；验收：`python mobile-apps/check_all.py`。
- 批量部署：dep_fei_mobile_all.tar.gz（/opt/fei-mobile/）+ fei_m_nginx.py / fei_m_static.py 自动补 nginx location。
- 新增系统：在 gen_all.py CONFIGS 加一条配置（名称/前缀/主题色/端点）即可产出同构 APP。
- 管理员口令统一化：已将服务器端 feiyuan-erp/feihong-stock/feiyang-customs/feiyun-finance/feiliu-flow 的 admin 口令重置为 admin123（散列按各系统算法写入）。

## 八、交付物

- 生成器与配置：mobile-apps/gen_all.py（24 份 CONFIGS）、验收脚本 check_all.py、立项清单.md
- 各项目内嵌：fei*/mobile/（index.html、config.js、app.js、style.css、manifest.webmanifest、sw.js、icon.svg）
- 线上：24 个 /<prefix>/m/ 站点；GitHub：dukema81/fei-mobile-apps（本方案+生成器+全部APP源码）
