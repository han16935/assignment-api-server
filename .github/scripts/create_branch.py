import re
import sys
import os
import json

def get_branch_type(label_names, title):
    # 라벨/제목 타입 매핑
    type_map = {
        # 라벨 매핑
        '✨ feature': 'feat',
        'feature': 'feat',
        'feat': 'feat',

        '🐛 bug': 'fix',
        'bug': 'fix',
        'fix': 'fix',

        '♻️ refactor': 'refactor',
        'refactor': 'refactor',
        'refactoring': 'refactor',

        '⚡ performance' : 'performance',

        '🔥 remove': 'chore',
        'remove': 'chore',

        '🔧 config': 'chore',
        'config': 'chore',

        '✅ test': 'chore',
        'test': 'chore',

        '🚀 deploy': 'chore',
        'deploy': 'chore',

        'chore': 'chore',
        '⚙️ chore' : 'chore'
    }
    
    # 1. 라벨에서 이슈 타입 추출
    for label in label_names:
        t = type_map.get(label)
        if t:
            return t
    
    # 2. 제목에서 이슈 타입 추출
    m = re.match(r'^([^/]+)/', title)
    if m:
        t = m.group(1).strip()
        return t.lower()

    return 'issue'

def clean_title(title):
    # 'Feat/' 또는 '[TYPE]' 패턴 제거
    title = re.sub(r'^[^/]+/\s*', '', title)
    title = re.sub(r'^\[[^\]]*\]\s*', '', title)

    # 공백을 언더바(_)로 변경
    title = re.sub(r'\s+', '_', title)

    # 특수문자 제거 (언더바, 하이픈, 한글, 영문, 숫자 제외)
    title = re.sub(r'[^\w\uac00-\ud7a3]', '', title)

    # 연속된 언더바 방지 및 양끝 제거 (소문자 변환 .lower() 제거)
    title = re.sub(r'_+', '_', title).strip('_')
    return title or 'Untitled'

if __name__ == "__main__":
    title = os.environ.get('ISSUE_TITLE', '')
    labels_json = os.environ.get('ISSUE_LABELS', '[]')
    try:
        labels = json.loads(labels_json)
        label_names = [label.get('name', '').lower() for label in labels]
    except Exception:
        label_names = []

    branch_type = get_branch_type(label_names, title)
    clean = clean_title(title)
    branch_name = f"{branch_type}/{clean}"
    print(branch_name) 
