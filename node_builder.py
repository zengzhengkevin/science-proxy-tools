#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用代理节点生成器（命令行交互式）
支持：hysteria2 / ss / trojan / tuic
输出：.conf (Surge/Shadowrocket) 与 .yaml (Stash/Clash)
"""
import os
import sys

def have_questionary():
    try:
        import questionary  # type: ignore
        return True
    except Exception:
        return False

def prompt_inputs():
    """
    收集输入参数。优先使用 questionary 提供菜单和输入框；
    如果没有安装，则退化为 input()。
    """
    protocols = ["hysteria2", "ss", "trojan", "tuic"]

    if have_questionary():
        import questionary  # type: ignore
        proto = questionary.select(
            "请选择协议类型：", choices=protocols
        ).ask()
        name = questionary.text("节点名称（例如 HK-HY-1）:").ask()
        host = questionary.text("服务器地址:").ask()
        port = questionary.text("端口号:", validate=lambda t: t.isdigit() or "请输入数字").ask()
        passwd = questionary.text("密码 / psk / uuid（按协议需求填）:").ask()
        sni = questionary.text("SNI（可留空，默认 www.bing.com）:").ask()
        method = ""
        if proto == "ss":
            method = questionary.text("SS 加密方式（默认 2022-blake3-aes-128-gcm）:").ask()
    else:
        print("未检测到 questionary，使用基础交互。若需更好体验：pip install questionary")
        def ask(msg, default=None):
            v = input(msg).strip()
            return v if v else (default or "")
        def ask_int(msg):
            while True:
                v = input(msg).strip()
                if v.isdigit():
                    return v
                print("请输入数字")
        def ask_choice(msg, choices):
            print(msg, " / ".join(choices))
            while True:
                v = input("> ").strip().lower()
                if v in choices:
                    return v
                print("请从：", ", ".join(choices), "中选择")
        proto = ask_choice("协议类型：", protocols)
        name = ask("节点名称（例如 HK-HY-1）:")
        host = ask("服务器地址:")
        port = ask_int("端口号:")
        passwd = ask("密码 / psk / uuid（按协议需求填）:")
        sni = ask("SNI（可留空，默认 www.bing.com）:", "")
        method = ""
        if proto == "ss":
            method = ask("SS 加密方式（默认 2022-blake3-aes-128-gcm）:", "")

    if not sni:
        sni = "www.bing.com"
    if proto == "ss" and not method:
        method = "2022-blake3-aes-128-gcm"

    return {
        "proto": proto,
        "name": name.strip(),
        "host": host.strip(),
        "port": int(port),
        "passwd": passwd.strip(),
        "sni": sni.strip(),
        "method": method.strip(),
    }

def gen_conf(p):
    proto = p["proto"]
    name  = p["name"]
    host  = p["host"]
    port  = p["port"]
    pw    = p["passwd"]
    sni   = p["sni"]
    if proto == "hysteria2":
        return f"{name} = hysteria2, {host}, {port}, password={pw}, sni={sni}, skip-cert-verify=true\n"
    if proto == "ss":
        method = p["method"]
        return f'{name} = ss, {host}, {port}, encrypt-method={method}, password="{pw}", udp-relay=true\n'
    if proto == "trojan":
        return f"{name} = trojan, {host}, {port}, password={pw}, sni={sni}, skip-cert-verify=true\n"
    if proto == "tuic":
        return f"{name} = tuic, {host}, {port}, uuid={pw}, alpn=h3, sni={sni}, skip-cert-verify=true\n"
    raise ValueError("Unknown protocol")

def gen_yaml(p):
    proto = p["proto"]
    name  = p["name"]
    host  = p["host"]
    port  = p["port"]
    pw    = p["passwd"]
    sni   = p["sni"]
    if proto == "hysteria2":
        return (
            f'- name: "{name}"\n'
            f"  type: hysteria2\n"
            f"  server: {host}\n"
            f"  port: {port}\n"
            f'  password: "{pw}"\n'
            f'  sni: "{sni}"\n'
            f"  skip-cert-verify: true\n"
        )
    if proto == "ss":
        method = p["method"]
        return (
            f'- name: "{name}"\n'
            f"  type: ss\n"
            f"  server: {host}\n"
            f"  port: {port}\n"
            f'  cipher: "{method}"\n'
            f'  password: "{pw}"\n'
            f"  udp: true\n"
        )
    if proto == "trojan":
        return (
            f'- name: "{name}"\n'
            f"  type: trojan\n"
            f"  server: {host}\n"
            f"  port: {port}\n"
            f'  password: "{pw}"\n'
            f'  sni: "{sni}"\n'
            f"  skip-cert-verify: true\n"
        )
    if proto == "tuic":
        return (
            f'- name: "{name}"\n'
            f"  type: tuic\n"
            f"  server: {host}\n"
            f"  port: {port}\n"
            f'  uuid: "{pw}"\n'
            f"  alpn: [h3]\n"
            f'  sni: "{sni}"\n'
            f"  skip-cert-verify: true\n"
        )
    raise ValueError("Unknown protocol")

def main():
    p = prompt_inputs()
    base = f'{p["name"]}_{p["proto"]}'
    conf_file = f"{base}.conf"
    yaml_file = f"{base}.yaml"

    conf = gen_conf(p)
    yaml_text = gen_yaml(p)

    with open(conf_file, "w", encoding="utf-8") as f:
        f.write(conf)
    with open(yaml_file, "w", encoding="utf-8") as f:
        f.write(yaml_text)

    print("\n✅ 已生成配置文件：")
    print(f"  - {conf_file}  (Surge / Shadowrocket)")
    print(f"  - {yaml_file}  (Stash / Clash)")
    print("\n提示：如需菜单式界面，请先安装 questionary： pip install questionary")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(1)
