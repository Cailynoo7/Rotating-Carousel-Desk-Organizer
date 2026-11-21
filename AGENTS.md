# 项目版本规则

用户要求：每次更新同步更新版本号。

- 当前产品版本以 product/version.json 的 current_version 为准。
- 初始命名的修改前版本为 v1；隔板顶面齐平修改为 v2。
- 后续每完成并交付一次实质性的产品更新（需求、零件、结构、CAD），版本整数递增一次，例如 v2 → v3。同一次用户请求中的建模尝试、修复和验证使用同一个版本号；只回答问题且没有修改产品时不递增。
- 同步更新 product/version.json、产品与设计说明的版本、product/requirements.json 的 product_version，以及受影响的零件描述和要求摘要。CAD 版本映射填写最终检查过的完整 revision。
- 需求变化时按项目规则重算 BOM requirements_digest，并保持材料清单与实际几何一致。
- CAD 活跃源仅用 cad.edit 更新。版本映射是标签记录，不代表已创建 Git 提交或可恢复备份；只有用户明确要求时才提交 Git。
- 保持用户外观要求：模型外表不印版本号或尺寸文字。
