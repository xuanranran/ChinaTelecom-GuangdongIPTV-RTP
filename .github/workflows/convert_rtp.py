import os
import re
import glob

EXTM3U_HEADER = '#EXTM3U name="guangdong-iptv" x-tvg-url="https://raw.githubusercontent.com/Tzwcard/ChinaTelecom-GuangdongIPTV-RTP-List/refs/heads/master/epg.xml"'

EXTRA_CHANNELS = '''#EXTINF:-1 tvg-id="1" tvg-name="翡翠台" tvg-logo="https://gh-proxy.com/https://raw.githubusercontent.com/fanmingming/live/main/tv/翡翠台.png" group-title="别人-翡翠台",翡翠台
http://cdn9.163189.xyz/smt1.1.php?id=jade_twn

#EXTINF:-1 tvg-id="1" tvg-name="翡翠台" tvg-logo="https://gh-proxy.com/https://raw.githubusercontent.com/fanmingming/live/main/tv/翡翠台.png" group-title="别人-翡翠台",翡翠台
http://mytv.cdn.loc.cc/o12.php?id=fct

#EXTINF:-1 tvg-id="1" tvg-name="翡翠台" tvg-logo="https://gh-proxy.com/https://raw.githubusercontent.com/fanmingming/live/main/tv/翡翠台.png" group-title="别人-翡翠台",翡翠台
https://hls.iill.top/api/TVB-Jade/index.m3u8
'''

def convert_rtp_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(r'rtp://([\d.]+:\d+)', r'http://192.168.11.1:5140/rtp/\1?fcc=183.59.144.166:8027', content)

    lines = new_content.splitlines(keepends=True)
    if lines and lines[0].startswith('#EXTM3U'):
        lines[0] = EXTM3U_HEADER + '\n'
    else:
        lines.insert(0, EXTM3U_HEADER + '\n')
    lines.insert(1, EXTRA_CHANNELS)
    new_content = ''.join(lines)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Converted: {file_path}")
    else:
        print(f"No changes: {file_path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    m3u_files = glob.glob(os.path.join(base_dir, '**', '*.m3u'), recursive=True)
    m3u_files += glob.glob(os.path.join(base_dir, '**', '*.m3u8'), recursive=True)

    if not m3u_files:
        print("No m3u/m3u8 files found.")
        return

    for file_path in m3u_files:
        convert_rtp_links(file_path)

    print(f"Done. Processed {len(m3u_files)} file(s).")

if __name__ == '__main__':
    main()
