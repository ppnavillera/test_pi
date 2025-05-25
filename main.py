#!/usr/bin/env python3
"""
음악가 수익 분석 플랫폼 - 메인 실행 파일
동형암호를 사용한 프라이버시 보존 음악 수익 분석 도구

작성자: 음악가 수익 분석 팀
목적: 개인정보 보호와 시장 인사이트의 균형 제공
"""

import sys
import os
import traceback
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """필요한 의존성 확인"""
    missing_packages = []
    
    try:
        import piheaan
    except ImportError:
        missing_packages.append("pi-heaan")
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append("tkinter")
    
    try:
        import numpy
    except ImportError:
        missing_packages.append("numpy")
    
    if missing_packages:
        print("❌ 다음 패키지들이 설치되지 않았습니다:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n설치 방법:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def setup_directories():
    """필요한 디렉토리 생성"""
    directories = [
        "data",
        "keys",
        "logs"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
    
    print("📁 필요한 디렉토리가 준비되었습니다.")

def create_init_files():
    """__init__.py 파일들 생성"""
    init_dirs = ["core", "gui"]
    
    for init_dir in init_dirs:
        init_file = project_root / init_dir / "__init__.py"
        init_file.parent.mkdir(exist_ok=True)
        
        if not init_file.exists():
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f'"""{init_dir} 모듈"""\n')
    
    print("📝 모듈 초기화 파일이 생성되었습니다.")

def create_sample_data_file():
    """샘플 데이터 파일 생성"""
    sample_data_file = project_root / "data" / "sample_data.json"
    
    if not sample_data_file.exists():
        import json
        
        sample_data = {
            "description": "음악가 수익 분석을 위한 샘플 데이터",
            "version": "1.0",
            "sample_artists": [
                {
                    "artist_id": "sample_001",
                    "genre": "Pop",
                    "period": "2024-Q1",
                    "revenue": 8500000,
                    "song_count": 4,
                    "danceability": 0.85,
                    "energy": 0.78,
                    "valence": 0.92,
                    "tempo": 128,
                    "acousticness": 0.05,
                    "instrumentalness": 0.0,
                    "liveness": 0.15,
                    "speechiness": 0.08,
                    "loudness": -4.2,
                    "duration_ms": 195000
                },
                {
                    "artist_id": "sample_002",
                    "genre": "Hip-Hop",
                    "period": "2024-Q1",
                    "revenue": 12300000,
                    "song_count": 6,
                    "danceability": 0.92,
                    "energy": 0.88,
                    "valence": 0.65,
                    "tempo": 145,
                    "acousticness": 0.02,
                    "instrumentalness": 0.1,
                    "liveness": 0.25,
                    "speechiness": 0.35,
                    "loudness": -3.8,
                    "duration_ms": 238000
                }
            ]
        }
        
        with open(sample_data_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        print("📊 샘플 데이터 파일이 생성되었습니다.")

def show_welcome_message():
    """환영 메시지 출력"""
    print("\n" + "="*60)
    print("🎵 음악가 수익 분석 플랫폼")
    print("="*60)
    print("📖 과제: 동형암호를 활용한 프라이버시 보존 애플리케이션")
    print("🔐 특징: 개인 수익 정보는 보호하되 시장 트렌드는 공유")
    print("⚙️  기술: pi-heaan (CKKS 동형암호)")
    print("="*60)
    print("\n🚀 시스템을 시작합니다...\n")

def main():
    """메인 함수"""
    try:
        # 환영 메시지
        show_welcome_message()
        
        # 의존성 확인
        print("🔍 의존성 확인 중...")
        if not check_dependencies():
            return 1
        print("✅ 모든 의존성이 확인되었습니다.")
        
        # 디렉토리 설정
        print("📁 디렉토리 설정 중...")
        setup_directories()
        
        # 초기화 파일 생성
        print("📝 모듈 초기화 중...")
        create_init_files()
        
        # 샘플 데이터 파일 생성
        print("📊 샘플 데이터 준비 중...")
        create_sample_data_file()
        
        print("✅ 모든 준비가 완료되었습니다!")
        print("\n🎵 GUI 애플리케이션을 시작합니다...")
        
        # GUI 애플리케이션 시작
        from gui.main_window import MusicRevenueAnalyzerGUI
        
        app = MusicRevenueAnalyzerGUI()
        app.run()
        
        return 0
        
    except ImportError as e:
        print(f"❌ 모듈 import 실패: {e}")
        print("다음을 확인해주세요:")
        print("1. 모든 파일이 올바른 위치에 있는지")
        print("2. requirements.txt의 패키지들이 설치되었는지")
        return 1
        
    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}")
        print("\n상세 오류 정보:")
        traceback.print_exc()
        return 1

def run_tests():
    """간단한 테스트 실행"""
    print("🧪 기본 테스트 실행 중...")
    
    try:
        # HE 엔진 테스트
        print("  - HE 엔진 테스트...")
        from core.he_engine import HEEngine
        he_engine = HEEngine(log_slots=3)  # 작은 크기로 테스트
        
        test_data = [0.1, 0.2, 0.3]
        encrypted = he_engine.encrypt_data(test_data)
        decrypted = he_engine.decrypt_data(encrypted, len(test_data))
        
        if abs(decrypted[0] - 0.1) < 0.01:
            print("    ✅ HE 엔진 정상 작동")
        else:
            print("    ❌ HE 엔진 오류")
            return False
        
        # 데이터 인코더 테스트
        print("  - 데이터 인코더 테스트...")
        from core.data_encoder import MusicDataEncoder
        encoder = MusicDataEncoder()
        
        test_music_data = {
            'artist_id': 'test',
            'genre': 'Pop',
            'revenue': 1000000,
            'danceability': 0.8
        }
        
        encoded = encoder.encode_music_data(test_music_data)
        if 'revenue' in encoded and 'genre' in encoded:
            print("    ✅ 데이터 인코더 정상 작동")
        else:
            print("    ❌ 데이터 인코더 오류")
            return False
        
        print("✅ 모든 테스트 통과!")
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    # 명령행 인수 처리
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # 테스트 모드
            if run_tests():
                print("🎉 시스템이 정상적으로 작동합니다!")
                sys.exit(0)
            else:
                print("💥 시스템에 문제가 있습니다.")
                sys.exit(1)
        elif sys.argv[1] == "--help":
            # 도움말
            print("🎵 음악가 수익 분석 플랫폼")
            print("\n사용법:")
            print("  python main.py           - GUI 애플리케이션 실행")
            print("  python main.py --test    - 시스템 테스트 실행")
            print("  python main.py --help    - 이 도움말 표시")
            print("\n설명:")
            print("  동형암호를 사용하여 음악가들의 수익 데이터를")
            print("  안전하게 분석하는 프라이버시 보존 플랫폼입니다.")
            sys.exit(0)
    
    # 기본 실행 (GUI 모드)
    sys.exit(main())

# =============================================================================
# 추가 유틸리티 함수들
# =============================================================================

def create_readme():
    """README 파일 생성"""
    readme_content = """# 🎵 음악가 수익 분석 플랫폼

## 📋 프로젝트 개요

동형암호(Homomorphic Encryption)를 활용하여 음악가들의 수익 데이터를 프라이버시를 보존하면서 분석하는 플랫폼입니다.

## 🔐 핵심 특징

- **완벽한 프라이버시**: 개인 수익 데이터는 절대 노출되지 않음
- **암호화된 연산**: pi-heaan을 사용한 CKKS 동형암호 적용
- **실용적 인사이트**: 시장 트렌드와 비교 분석 제공
- **사용자 친화적**: 직관적인 GUI 인터페이스

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 프로그램 실행
```bash
python main.py
```

### 3. 테스트 실행
```bash
python main.py --test
```

## 📊 주요 기능

### 1. 데이터 입력
- 아티스트 정보 입력
- 수익 데이터 암호화
- 음악 특성 분석

### 2. 프라이버시 보존 분석
- 장르별 평균 수익 계산
- 시장 위치 비교 분석
- 트렌드 분석

### 3. 보안 보장
- 모든 연산이 암호화된 상태에서 수행
- 개인 데이터 완전 보호
- 통계 결과만 공개

## 🏗️ 시스템 구조

```
music_privacy_analyzer/
├── main.py                    # 메인 실행 파일
├── requirements.txt           # 의존성 목록
├── core/                      # 핵심 모듈
│   ├── he_engine.py          # 동형암호 엔진
│   ├── data_encoder.py       # 데이터 인코딩
│   └── privacy_calculator.py # 프라이버시 보존 계산
├── gui/                       # GUI 인터페이스
│   └── main_window.py        # 메인 윈도우
└── data/                      # 데이터 저장소
    ├── sample_data.json      # 샘플 데이터
    └── encrypted_storage.pkl # 암호화된 저장소
```

## 🔧 기술 스택

- **동형암호**: pi-heaan (CKKS 알고리즘)
- **GUI**: tkinter
- **데이터 처리**: numpy, pandas
- **언어**: Python 3.8+

## 📈 사용 시나리오

1. **신인 음악가**: 시장 평균과 비교하여 자신의 위치 파악
2. **음악 산업 분석**: 장르별 트렌드 분석
3. **프라이버시 보호**: 개인 정보 노출 없는 집단 인사이트

## 🎯 과제 목표

- **창의성**: 음악 산업에 특화된 프라이버시 보존 플랫폼
- **유용성**: 실제 음악가들이 활용할 수 있는 가치 제공
- **기술적 도전**: 동형암호의 실용적 적용
- **이해용이성**: 명확한 코드 구조와 문서화

## 👥 팀 구성

- **팀원 A**: 동형암호 엔진 개발
- **팀원 B**: 데이터 처리 및 GUI 개발  
- **팀원 C**: 통계 분석 및 문서화

## 📝 라이선스

교육용 프로젝트 - 상업적 사용 금지
"""
    
    with open(project_root / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--create-readme":
    create_readme()
    print("📝 README.md 파일이 생성되었습니다.")