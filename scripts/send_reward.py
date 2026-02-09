#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

CONFIG = {
    'api_endpoint': 'http://192.168.0.197:3200',
    'default_reward_amount': 0,
    'third_party_name': '限时福利活动奖励',
}

MESSAGES = {
    'provide_username': '请提供用户名',
    'success': '恭喜您获得 ¥{amount} 奖励！',
    'error': '领取奖励失败，请稍后重试',
    'network_error': '网络错误，请检查网络连接后重试',
    'timeout_error': '请求超时，请稍后重试',
    'server_error': '服务器内部错误',
    'unknown_error': '发生未知错误',
}

SOURCE_OPTIONS = [
    ('quiz', '答题奖励'),
    ('other', '奖励（默认）'),
]

STYLE = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
}


def style_text(text, color=None, bold=False):
    result = ''
    if color and color in STYLE:
        result += STYLE[color]
    if bold:
        result += STYLE['bold']
    result += text
    result += STYLE['reset']
    return result


def clear_screen():
    print('\033[2J\033[H', end='')


def print_header():
    print()
    print(style_text('╔══════════════════════════════════════════════════╗', 'cyan', True))
    print(style_text('║           奖励发放系统 - Send Reward             ║', 'cyan', True))
    print(style_text('╚══════════════════════════════════════════════════╝', 'cyan', True))
    print()


def print_menu():
    print(style_text('┌────────────────────────────────────────────────────┐', 'yellow'))
    print(style_text('│  1. 发放奖励                                       │', 'yellow'))
    print(style_text('│  2. 查看API配置                                    │', 'yellow'))
    print(style_text('│  3. 修改API端点                                    │', 'yellow'))
    print(style_text('│  0. 退出                                           │', 'yellow'))
    print(style_text('└────────────────────────────────────────────────────┘', 'yellow'))
    print()


def print_config():
    print(style_text('┌────────────────────────────────────────────────────┐', 'magenta'))
    print(style_text(f'│  当前API端点: {CONFIG["api_endpoint"]:30}  │', 'magenta'))
    print(style_text(f'│  默认奖励金额: ¥{CONFIG["default_reward_amount"]:29}  │', 'magenta'))
    print(style_text(f'│  第三方名称: {CONFIG["third_party_name"]:31}  │', 'magenta'))
    print(style_text('└────────────────────────────────────────────────────┘', 'magenta'))
    print()


def print_source_options():
    print(style_text('可选奖励来源:', 'blue', True))
    for i, (key, desc) in enumerate(SOURCE_OPTIONS, 1):
        print(f"  {style_text(f'[{i}]', 'yellow')} {desc} ({key})")
    print()


def get_input(prompt_text, default=None, allow_empty=False):
    if default:
        prompt = f"{prompt_text} [{default}]: "
    else:
        prompt = f"{prompt_text}: "
    
    user_input = input(style_text(prompt, 'cyan')).strip()
    
    if not user_input and default is not None:
        return default
    
    if not user_input and allow_empty:
        return ''
    
    return user_input


def get_number_input(prompt_text, default=None):
    while True:
        user_input = get_input(prompt_text, default)
        try:
            if user_input == '' and default is not None:
                return default
            return float(user_input)
        except ValueError:
            print(style_text('请输入有效的数字', 'red'))


def get_choice_input(prompt_text, options, default=None):
    while True:
        user_input = get_input(prompt_text, default)
        if user_input == '' and default is not None:
            return default
        
        try:
            choice = int(user_input)
            if 1 <= choice <= len(options):
                return options[choice - 1][0]
            print(style_text(f'请输入 1-{len(options)} 之间的数字', 'red'))
        except ValueError:
            if user_input in [opt[0] for opt in options]:
                return user_input
            print(style_text('请输入有效的选项', 'red'))


def get_current_date_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M')


def build_description(reward_amount, source=None):
    date_time = get_current_date_time()
    description = f"{CONFIG['third_party_name']} - 奖励金额: ¥{reward_amount} - 领取时间: {date_time}"

    if source == 'quiz':
        description = f"{CONFIG['third_party_name']} - 答题奖励: ¥{reward_amount} - 领取时间: {date_time}"
    elif source == 'other':
        description = f"{CONFIG['third_party_name']} - 奖励: ¥{reward_amount} - 领取时间: {date_time}"
    
    return description


def build_request_data(username, reward_amount, source=None):
    return {
        'username': username,
        'amount': reward_amount,
        'thirdPartyId': source or 'promotion',
        'thirdPartyName': CONFIG['third_party_name'],
        'description': build_description(reward_amount, source)
    }


def send_reward_request(request_data, timeout=30):
    url = f"{CONFIG['api_endpoint']}/api/third-party/receipts"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        data = json.dumps(request_data).encode('utf-8')
        req = Request(url, data=data, headers=headers, method='POST')
        
        with urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get('content-type', '')
            
            if 'application/json' in content_type:
                result = json.loads(response.read().decode('utf-8'))
            else:
                result = {
                    'success': response.status == 200,
                    'message': response.read().decode('utf-8') or '未知响应'
                }
            
            return {
                'success': response.status == 200 and result.get('success', False),
                'status_code': response.status,
                'data': result
            }
            
    except HTTPError as e:
        return {
            'success': False,
            'status_code': e.code,
            'error': f'HTTP错误: {e.reason}',
            'message': MESSAGES['error']
        }
    except URLError as e:
        if 'timed out' in str(e.reason).lower():
            return {
                'success': False,
                'status_code': 408,
                'error': f'请求超时: {e.reason}',
                'message': MESSAGES['timeout_error']
            }
        return {
            'success': False,
            'status_code': 503,
            'error': f'网络错误: {e.reason}',
            'message': MESSAGES['network_error']
        }
    except Exception as e:
        return {
            'success': False,
            'status_code': 500,
            'error': f'未知错误: {str(e)}',
            'message': MESSAGES['unknown_error']
        }


def send_reward(username, reward_amount=None, source=None):
    if not username:
        print(MESSAGES['provide_username'])
        return False
    
    if reward_amount is None:
        reward_amount = CONFIG['default_reward_amount']
    
    if not isinstance(reward_amount, (int, float)) or reward_amount < 0:
        print('错误：奖励金额必须为非负数字')
        return False
    
    request_data = build_request_data(username, reward_amount, source)
    
    print()
    print(style_text('正在发送奖励请求...', 'blue'))
    print(f"请求URL: {CONFIG['api_endpoint']}/api/third-party/receipts")
    print(f"请求数据: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
    print()
    
    result = send_reward_request(request_data)
    
    if result['success']:
        print()
        print(style_text('=' * 50, 'green', True))
        print(style_text(MESSAGES['success'].format(amount=reward_amount), 'green', True))
        print(style_text('=' * 50, 'green', True))
        return True
    else:
        print()
        print(style_text('=' * 50, 'red', True))
        print(style_text(f"错误: {result.get('message', MESSAGES['error'])}", 'red', True))
        if 'data' in result and isinstance(result['data'], dict):
            error_detail = result['data'].get('message', result['data'].get('error', ''))
            if error_detail:
                print(style_text(f"详情: {error_detail}", 'yellow'))
        print(style_text('=' * 50, 'red', True))
        return False


def interactive_mode():
    while True:
        print_header()
        print_menu()
        
        choice = get_input('请选择操作', '1')
        print()
        
        if choice == '1':
            print(style_text('【发放奖励】', 'green', True))
            print()
            
            username = get_input('请输入用户名')
            if not username:
                print(style_text('用户名不能为空', 'red'))
                input(style_text('按 Enter 键继续...', 'cyan'))
                continue
            
            reward_amount = get_number_input('请输入奖励金额', CONFIG['default_reward_amount'])
            print_source_options()
            source = get_choice_input('请选择奖励来源（直接输入编号或类型）', SOURCE_OPTIONS, 'promotion')
            
            print()
            print(style_text('确认信息:', 'blue', True))
            print(f"  用户名: {style_text(username, 'yellow')}")
            print(f"  奖励金额: {style_text(f'¥{reward_amount}', 'yellow')}")
            print(f"  奖励来源: {style_text([desc for k, desc in SOURCE_OPTIONS if k == source][0], 'yellow')}")
            print()
            
            confirm = get_input('确认发放奖励？(y/n)', 'y')
            if confirm.lower() == 'y' or confirm.lower() == 'yes':
                send_reward(username, reward_amount, source)
            
            input(style_text('按 Enter 键继续...', 'cyan'))
            
        elif choice == '2':
            print(style_text('【查看配置】', 'green', True))
            print()
            print_config()
            input(style_text('按 Enter 键继续...', 'cyan'))
            
        elif choice == '3':
            print(style_text('【修改API端点】', 'green', True))
            print()
            new_endpoint = get_input('请输入新的API端点', CONFIG['api_endpoint'])
            if new_endpoint:
                CONFIG['api_endpoint'] = new_endpoint
                print(style_text('API端点已更新', 'green'))
            input(style_text('按 Enter 键继续...', 'cyan'))
            
        elif choice == '0':
            print(style_text('感谢使用，再见！', 'green', True))
            break
        
        else:
            print(style_text('无效选项，请重新选择', 'red'))
            input(style_text('按 Enter 键继续...', 'cyan'))


def command_line_mode(args):
    if args.endpoint:
        CONFIG['api_endpoint'] = args.endpoint
    
    success = send_reward(args.user, args.amount, args.source)
    sys.exit(0 if success else 1)


def main():
    parser = argparse.ArgumentParser(
        description='向指定用户发送自定义奖励',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog="""
交互模式（无参数运行）:
  直接运行脚本将进入交互式菜单界面

命令行模式:
  python send_reward.py -u 用户名
  python send_reward.py --user 用户名 --amount 100
  python send_reward.py -u 用户名 -a 50 -s daily_sign_in

参数说明:
  -u, --user     目标用户名（必填）
  -a, --amount   奖励金额（默认使用默认值）
  -s, --source   奖励来源
  -e, --endpoint API端点地址
  -t, --timeout  请求超时时间
        """
    )
    
    parser.add_argument(
        '-u', '--user',
        dest='user',
        help='目标用户名'
    )
    
    parser.add_argument(
        '-a', '--amount',
        type=float,
        default=None,
        dest='amount',
        help='奖励金额'
    )
    
    parser.add_argument(
        '-s', '--source',
        choices=['quiz', 'other'],
        default=None,
        dest='source',
        help='奖励来源'
    )
    
    parser.add_argument(
        '-e', '--endpoint',
        default=None,
        dest='endpoint',
        help='API端点地址'
    )
    
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        dest='timeout',
        help='请求超时时间（默认: 30秒）'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        dest='interactive',
        help='强制进入交互模式'
    )
    
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='显示帮助信息'
    )
    
    args = parser.parse_args()
    
    if args.interactive or args.user is None:
        interactive_mode()
    else:
        command_line_mode(args)


if __name__ == '__main__':
    main()
