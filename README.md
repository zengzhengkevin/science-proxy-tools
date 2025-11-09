# 🌐 Science Proxy Tools

一套实用的代理工具配置与生成脚本合集，支持 **Surge / Shadowrocket / Stash / Clash**。

---

## 🧩 文件说明

| 文件 | 说明 |
|------|------|
| `node_builder.py` | 命令行交互式节点生成器（支持 hysteria2 / ss / trojan / tuic） |
| `科学20251109_Shadowrocket_Compat.conf` | 已优化、兼容 Shadowrocket 的 Surge 配置文件 |
| `科学20251109_Stash.yaml` | Stash / Clash 通用 YAML 版配置文件 |
| `examples/` | 节点模板与示例 |

---

## 🚀 一、运行环境

支持所有主流系统：Debian/Ubuntu、CentOS/RHEL、Fedora、Arch、Alpine、macOS、Windows(WSL)。

### 安装依赖
```bash
# 以 Debian/Ubuntu 为例
sudo apt update
sudo apt install -y python3 python3-pip
# 可选：更好看的交互菜单
pip3 install --user questionary
```

---

## ⚙️ 二、运行节点生成器
```bash
python3 node_builder.py
```
或：
```bash
chmod +x node_builder.py
./node_builder.py
```

---

## 💡 三、功能介绍

交互示例：
```
=== 通用代理节点生成器 ===

请选择协议类型：
❯ hysteria2
  ss
  trojan
  tuic

请输入节点名称: HK-HY-1
请输入服务器地址: pqshkt.ngrok.xin
请输入端口号: 45678
请输入密码 / UUID / psk: 2ebb7ac4
是否需要 SNI？(默认 www.bing.com):
```

自动生成两份配置文件：
```
✅ HK-HY-1_hysteria2.conf    # Surge / Shadowrocket 版
✅ HK-HY-1_hysteria2.yaml    # Stash / Clash 版
```

---

## 🔧 四、配置文件示例

### examples/example_hysteria2.conf
```ini
HK-HY-1 = hysteria2, pqshkt.ngrok.xin, 45678, password=2ebb7ac4, sni=www.bing.com, skip-cert-verify=true
```

### examples/example_hysteria2.yaml
```yaml
- name: "HK-HY-1"
  type: hysteria2
  server: pqshkt.ngrok.xin
  port: 45678
  password: "2ebb7ac4"
  sni: "www.bing.com"
  skip-cert-verify: true
```

---

## 🧱 五、兼容性说明

| 客户端 | 支持协议 | 备注 |
|---------|------------|------|
| **Shadowrocket / Surge** | ss / hysteria2 / trojan / tuic | 不支持 Snell |
| **Stash / Clash / Clash Verge** | ss / hysteria2 / trojan / tuic | 完全支持 |
| **Quantumult / Loon** | 部分支持 | 建议使用 Clash/Stash 格式 |

---

## 🛠 六、扩展功能计划
- [ ] 批量生成节点（从 CSV 导入）
- [ ] 一键合并生成完整配置模板
- [ ] 在线版（Web 生成器）

---

## 📜 LICENSE
MIT License — 可自由修改与分发。
