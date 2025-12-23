import os
import requests

# 定义素材目录
ASSET_DIR = "assets/vectors"
if not os.path.exists(ASSET_DIR):
    os.makedirs(ASSET_DIR)

# 伪装成浏览器 (关键步骤：解决 403 Forbidden)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 更加稳定的 SVG 直链 (来自 Wikimedia Commons)
ASSETS_URLS = {
    "dna_structure.svg": "https://upload.wikimedia.org/wikipedia/commons/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBB.svg",
    "antibody_igg.svg": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Antibody_scheme.svg",
    # 替换了之前可能不稳定的链接
    "bacterium.svg": "https://upload.wikimedia.org/wikipedia/commons/3/32/Average_prokaryote_cell-_en.svg",
    "cell_membrane.svg": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cell_membrane_detailed_diagram_4.svg",
    "mitochondria.svg": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Animal_mitochondrion_diagram_en_%28edit%29.svg"
}

print(f"🚀 开始下载素材到 {ASSET_DIR}...")
print("ℹ️  正在伪装 User-Agent 以绕过防火墙...")

success_count = 0

for name, url in ASSETS_URLS.items():
    print(f"⬇️  正在下载: {name}...", end=" ")
    try:
        # 添加 headers 参数
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code == 200:
            file_path = os.path.join(ASSET_DIR, name)
            with open(file_path, "wb") as f:
                f.write(response.content)
            print("✅ 成功")
            success_count += 1
        else:
            print(f"❌ 失败 (Status {response.status_code})")

    except requests.exceptions.ProxyError:
        print("\n❌ 网络代理错误。如果您在医院/内网，可能需要配置代理。")
    except Exception as e:
        print(f"\n❌ 出错: {e}")

print(f"\n✨ 下载完成: 成功 {success_count}/{len(ASSETS_URLS)} 个文件。")
if success_count > 0:
    print("👉 现在可以运行: streamlit run app.py")