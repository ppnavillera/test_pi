"""
GUI 메인 윈도우
음악가 수익 분석 플랫폼의 메인 인터페이스
"""

from core.privacy_calculator import PrivacyPreservingCalculator
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Dict, Any
import sys
import os

# 상위 디렉토리의 모듈 import를 위해 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MusicRevenueAnalyzerGUI:
    """음악가 수익 분석 GUI 메인 클래스"""

    def __init__(self):
        """GUI 초기화"""
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()

        # 계산기 초기화 (백그라운드에서)
        self.calculator = None
        self.init_calculator()

        print("🎵 음악가 수익 분석 플랫폼 GUI 시작")

    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("🎵 음악가 수익 분석 플랫폼 - 프라이버시 보존")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # 윈도우 중앙 배치
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")

    def setup_styles(self):
        """스타일 설정"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 커스텀 스타일 정의
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Header.TFrame', background='#e6f3ff')
        self.style.configure(
            'Success.TLabel', foreground='green', font=('Arial', 10, 'bold'))
        self.style.configure('Error.TLabel', foreground='red',
                             font=('Arial', 10, 'bold'))

    def create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 헤더
        self.create_header(main_container)

        # 메인 콘텐츠 (좌우 분할)
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 좌측: 데이터 입력
        self.create_input_panel(content_frame)

        # 우측: 결과 표시
        self.create_result_panel(content_frame)

        # 하단: 상태바
        self.create_status_bar(main_container)

    def create_header(self, parent):
        """헤더 생성"""
        header_frame = ttk.Frame(parent, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # 제목
        title_label = ttk.Label(
            header_frame,
            text="🎵 음악가 수익 분석 플랫폼",
            style='Title.TLabel'
        )
        title_label.pack(pady=10)

        # 부제목
        subtitle_label = ttk.Label(
            header_frame,
            text="동형암호로 개인정보를 보호하면서 시장 트렌드 분석",
            font=('Arial', 10)
        )
        subtitle_label.pack()

        # 프라이버시 안내
        privacy_label = ttk.Label(
            header_frame,
            text="🔒 모든 수익 데이터는 암호화되어 처리되며, 개인 정보는 절대 노출되지 않습니다",
            foreground='green',
            font=('Arial', 9)
        )
        privacy_label.pack(pady=5)

    def create_input_panel(self, parent):
        """데이터 입력 패널 생성"""
        # 좌측 프레임
        left_frame = ttk.LabelFrame(parent, text="📊 수익 데이터 입력", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # 스크롤 가능한 프레임
        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(
            left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 입력 필드들
        self.create_input_fields(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 버튼 프레임
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # 데이터 추가 버튼
        self.add_data_btn = ttk.Button(
            button_frame,
            text="🔐 데이터 암호화 및 추가",
            command=self.add_artist_data,
            style='Accent.TButton'
        )
        self.add_data_btn.pack(fill=tk.X, pady=(0, 5))

        # 샘플 데이터 생성 버튼
        self.sample_data_btn = ttk.Button(
            button_frame,
            text="🧪 샘플 데이터 생성",
            command=self.generate_sample_data
        )
        self.sample_data_btn.pack(fill=tk.X)

    def create_input_fields(self, parent):
        """입력 필드 생성"""
        self.input_vars = {}

        # 기본 정보
        basic_frame = ttk.LabelFrame(parent, text="기본 정보", padding=5)
        basic_frame.pack(fill=tk.X, pady=(0, 10))

        # 아티스트 ID
        ttk.Label(basic_frame, text="아티스트 ID:").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        self.input_vars['artist_id'] = tk.StringVar(value="artist_001")
        ttk.Entry(basic_frame, textvariable=self.input_vars['artist_id'], width=20).grid(
            row=0, column=1, pady=2, padx=(5, 0))

        # 장르
        ttk.Label(basic_frame, text="장르:").grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self.input_vars['genre'] = tk.StringVar(value="Pop")
        genre_combo = ttk.Combobox(
            basic_frame,
            textvariable=self.input_vars['genre'],
            values=['Pop', 'Hip-Hop', 'Rock', 'Electronic',
                    'R&B', 'Country', 'Jazz', 'Classical'],
            state="readonly",
            width=18
        )
        genre_combo.grid(row=1, column=1, pady=2, padx=(5, 0))

        # 기간
        ttk.Label(basic_frame, text="기간:").grid(
            row=2, column=0, sticky=tk.W, pady=2)
        self.input_vars['period'] = tk.StringVar(value="2024-Q1")
        period_combo = ttk.Combobox(
            basic_frame,
            textvariable=self.input_vars['period'],
            values=['2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4',
                    '2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4'],
            state="readonly",
            width=18
        )
        period_combo.grid(row=2, column=1, pady=2, padx=(5, 0))

        # 수익 정보
        revenue_frame = ttk.LabelFrame(parent, text="수익 정보", padding=5)
        revenue_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(revenue_frame, text="수익 (원):").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        self.input_vars['revenue'] = tk.StringVar(value="5000000")
        ttk.Entry(revenue_frame, textvariable=self.input_vars['revenue'], width=20).grid(
            row=0, column=1, pady=2, padx=(5, 0))

        ttk.Label(revenue_frame, text="곡 수:").grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self.input_vars['song_count'] = tk.StringVar(value="3")
        ttk.Entry(revenue_frame, textvariable=self.input_vars['song_count'], width=20).grid(
            row=1, column=1, pady=2, padx=(5, 0))

        # 음악 특성
        music_frame = ttk.LabelFrame(
            parent, text="음악 특성 (0.0 ~ 1.0)", padding=5)
        music_frame.pack(fill=tk.X, pady=(0, 10))

        music_features = [
            ('danceability', 'Danceability', '0.8'),
            ('energy', 'Energy', '0.7'),
            ('valence', 'Valence', '0.9'),
            ('acousticness', 'Acousticness', '0.1'),
            ('instrumentalness', 'Instrumentalness', '0.0'),
            ('liveness', 'Liveness', '0.2'),
            ('speechiness', 'Speechiness', '0.05')
        ]

        for i, (key, label, default) in enumerate(music_features):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(music_frame, text=f"{label}:").grid(
                row=row, column=col, sticky=tk.W, pady=2, padx=(0, 5))
            self.input_vars[key] = tk.StringVar(value=default)
            ttk.Entry(music_frame, textvariable=self.input_vars[key], width=10).grid(
                row=row, column=col+1, pady=2, padx=(0, 20))

        # 기타 특성
        other_frame = ttk.LabelFrame(parent, text="기타 특성", padding=5)
        other_frame.pack(fill=tk.X)

        ttk.Label(other_frame, text="Tempo (BPM):").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        self.input_vars['tempo'] = tk.StringVar(value="120")
        ttk.Entry(other_frame, textvariable=self.input_vars['tempo'], width=15).grid(
            row=0, column=1, pady=2, padx=(5, 0))

        ttk.Label(other_frame, text="Loudness (dB):").grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self.input_vars['loudness'] = tk.StringVar(value="-5.0")
        ttk.Entry(other_frame, textvariable=self.input_vars['loudness'], width=15).grid(
            row=1, column=1, pady=2, padx=(5, 0))

        ttk.Label(other_frame, text="Duration (ms):").grid(
            row=2, column=0, sticky=tk.W, pady=2)
        self.input_vars['duration_ms'] = tk.StringVar(value="210000")
        ttk.Entry(other_frame, textvariable=self.input_vars['duration_ms'], width=15).grid(
            row=2, column=1, pady=2, padx=(5, 0))

    def create_result_panel(self, parent):
        """결과 표시 패널 생성"""
        # 우측 프레임
        right_frame = ttk.LabelFrame(parent, text="📈 분석 결과", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 분석 버튼들
        analysis_btn_frame = ttk.Frame(right_frame)
        analysis_btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.genre_analysis_btn = ttk.Button(
            analysis_btn_frame,
            text="🎯 장르별 평균 분석",
            command=self.analyze_genre_trends
        )
        self.genre_analysis_btn.pack(fill=tk.X, pady=(0, 5))

        self.market_compare_btn = ttk.Button(
            analysis_btn_frame,
            text="📊 시장 비교 분석",
            command=self.compare_with_market
        )
        self.market_compare_btn.pack(fill=tk.X, pady=(0, 5))

        self.privacy_report_btn = ttk.Button(
            analysis_btn_frame,
            text="🔒 프라이버시 현황",
            command=self.show_privacy_report
        )
        self.privacy_report_btn.pack(fill=tk.X)

        # 결과 표시 영역
        self.result_text = scrolledtext.ScrolledText(
            right_frame,
            height=25,
            width=50,
            font=('Consolas', 10),
            wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 초기 메시지
        self.append_result("🎵 음악가 수익 분석 플랫폼에 오신 것을 환영합니다!\n\n")
        self.append_result("🔒 이 플랫폼의 특징:\n")
        self.append_result("• 모든 수익 데이터는 동형암호로 보호됩니다\n")
        self.append_result("• 개인 정보는 절대 노출되지 않습니다\n")
        self.append_result("• 암호화된 상태에서 통계 분석을 수행합니다\n\n")
        self.append_result("📊 시작하려면 좌측에서 데이터를 입력하거나\n")
        self.append_result("샘플 데이터를 생성해보세요!\n\n")

    def create_status_bar(self, parent):
        """상태바 생성"""
        self.status_frame = ttk.Frame(parent)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_label = ttk.Label(
            self.status_frame,
            text="상태: 준비 완료",
            font=('Arial', 9)
        )
        self.status_label.pack(side=tk.LEFT)

        # 진행바
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))

    def init_calculator(self):
        """계산기 초기화 (백그라운드)"""
        def init_task():
            try:
                self.set_status("🔐 동형암호 엔진 초기화 중...")
                self.progress_bar.start()

                self.calculator = PrivacyPreservingCalculator()

                self.progress_bar.stop()
                self.set_status("✅ 시스템 준비 완료")

                # 버튼 활성화
                self.root.after(0, self.enable_buttons)

            except Exception as e:
                self.progress_bar.stop()
                self.set_status(f"❌ 초기화 실패: {e}")
                messagebox.showerror("초기화 오류", f"시스템 초기화에 실패했습니다:\n{e}")

        thread = threading.Thread(target=init_task, daemon=True)
        thread.start()

    def enable_buttons(self):
        """버튼들 활성화"""
        self.add_data_btn.configure(state='normal')
        self.sample_data_btn.configure(state='normal')
        self.genre_analysis_btn.configure(state='normal')
        self.market_compare_btn.configure(state='normal')
        self.privacy_report_btn.configure(state='normal')

    def set_status(self, message: str):
        """상태 메시지 설정"""
        self.status_label.configure(text=f"상태: {message}")
        self.root.update_idletasks()

    def append_result(self, text: str):
        """결과 텍스트 추가"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
        self.root.update_idletasks()

    def clear_results(self):
        """결과 텍스트 클리어"""
        self.result_text.delete(1.0, tk.END)

    def validate_input_data(self) -> Dict[str, Any]:
        """입력 데이터 검증"""
        try:
            data = {}

            # 문자열 필드
            data['artist_id'] = self.input_vars['artist_id'].get().strip()
            data['genre'] = self.input_vars['genre'].get()
            data['period'] = self.input_vars['period'].get()

            if not data['artist_id']:
                raise ValueError("아티스트 ID를 입력해주세요.")

            # 숫자 필드
            data['revenue'] = float(self.input_vars['revenue'].get())
            data['song_count'] = int(self.input_vars['song_count'].get())
            data['tempo'] = float(self.input_vars['tempo'].get())
            data['loudness'] = float(self.input_vars['loudness'].get())
            data['duration_ms'] = float(self.input_vars['duration_ms'].get())

            # 0~1 범위 필드
            range_fields = ['danceability', 'energy', 'valence', 'acousticness',
                            'instrumentalness', 'liveness', 'speechiness']

            for field in range_fields:
                value = float(self.input_vars[field].get())
                if not 0.0 <= value <= 1.0:
                    raise ValueError(f"{field}는 0.0~1.0 범위여야 합니다.")
                data[field] = value

            # 범위 검증
            if data['revenue'] < 0:
                raise ValueError("수익은 0 이상이어야 합니다.")
            if data['song_count'] < 1:
                raise ValueError("곡 수는 1 이상이어야 합니다.")
            if not 60 <= data['tempo'] <= 200:
                raise ValueError("템포는 60~200 BPM 범위여야 합니다.")

            return data

        except ValueError as e:
            messagebox.showerror("입력 오류", str(e))
            return None

    def add_artist_data(self):
        """아티스트 데이터 추가"""
        if not self.calculator:
            messagebox.showwarning("경고", "시스템이 아직 초기화되지 않았습니다.")
            return

        data = self.validate_input_data()
        if not data:
            return

        def add_task():
            try:
                self.set_status("🔐 데이터 암호화 중...")
                self.progress_bar.start()

                success = self.calculator.add_artist_data(data)

                self.progress_bar.stop()

                if success:
                    self.set_status("✅ 데이터 추가 완료")
                    self.root.after(0, lambda: self.append_result(
                        f"✅ '{data['artist_id']}' 데이터가 암호화되어 추가되었습니다.\n"
                        f"   장르: {data['genre']}, 수익: {data['revenue']:,.0f}원\n\n"
                    ))
                else:
                    self.set_status("❌ 데이터 추가 실패")
                    self.root.after(0, lambda: messagebox.showerror(
                        "오류", "데이터 추가에 실패했습니다."))

            except Exception as e:
                self.progress_bar.stop()
                self.set_status(f"❌ 오류: {e}")
                self.root.after(0, lambda: messagebox.showerror(
                    "오류", f"데이터 추가 중 오류 발생:\n{e}"))

        thread = threading.Thread(target=add_task, daemon=True)
        thread.start()

    def generate_sample_data(self):
        """샘플 데이터 생성"""
        if not self.calculator:
            messagebox.showwarning("경고", "시스템이 아직 초기화되지 않았습니다.")
            return

        def generate_task():
            try:
                self.set_status("🧪 샘플 데이터 생성 중...")
                self.progress_bar.start()

                self.calculator.generate_sample_data(15)

                self.progress_bar.stop()
                self.set_status("✅ 샘플 데이터 생성 완료")

                self.root.after(0, lambda: self.append_result(
                    "🧪 15개의 샘플 데이터가 생성되었습니다!\n"
                    "이제 분석 기능을 사용해보세요.\n\n"
                ))

            except Exception as e:
                self.progress_bar.stop()
                self.set_status(f"❌ 오류: {e}")
                self.root.after(0, lambda: messagebox.showerror(
                    "오류", f"샘플 데이터 생성 실패:\n{e}"))

        thread = threading.Thread(target=generate_task, daemon=True)
        thread.start()

    def analyze_genre_trends(self):
        """장르별 트렌드 분석"""
        if not self.calculator:
            messagebox.showwarning("경고", "시스템이 아직 초기화되지 않았습니다.")
            return

        def analyze_task():
            try:
                self.set_status("📊 장르별 분석 중...")
                self.progress_bar.start()

                results = self.calculator.calculate_all_genre_averages()

                self.progress_bar.stop()
                self.set_status("✅ 분석 완료")

                # 결과 표시
                result_text = "📊 장르별 평균 수익 분석 결과\n"
                result_text += "=" * 40 + "\n\n"

                if results:
                    for genre, avg_revenue in sorted(results.items(), key=lambda x: x[1], reverse=True):
                        result_text += f"🎵 {genre:12s}: {avg_revenue:>10,.0f}원\n"
                else:
                    result_text += "분석할 데이터가 충분하지 않습니다.\n"

                result_text += "\n🔒 개인별 수익은 완전히 보호됩니다.\n\n"

                self.root.after(0, lambda: self.append_result(result_text))

            except Exception as e:
                self.progress_bar.stop()
                self.set_status(f"❌ 분석 실패: {e}")
                self.root.after(0, lambda: messagebox.showerror(
                    "분석 오류", f"장르 분석 실패:\n{e}"))

        thread = threading.Thread(target=analyze_task, daemon=True)
        thread.start()

    def compare_with_market(self):
        """시장 비교 분석"""
        if not self.calculator:
            messagebox.showwarning("경고", "시스템이 아직 초기화되지 않았습니다.")
            return

        data = self.validate_input_data()
        if not data:
            return

        def compare_task():
            try:
                self.set_status("🔍 시장 비교 분석 중...")
                self.progress_bar.start()

                result = self.calculator.compare_with_market(
                    data['revenue'],
                    data['genre'],
                    data['period']
                )

                self.progress_bar.stop()
                self.set_status("✅ 비교 분석 완료")

                # 결과 표시
                if result['status'] == 'success':
                    result_text = "🔍 시장 비교 분석 결과\n"
                    result_text += "=" * 40 + "\n\n"
                    result_text += f"📊 분석 대상: {data['genre']} 장르\n"
                    result_text += f"💰 내 수익: {result['my_revenue']:,.0f}원\n"
                    result_text += f"📈 시장 평균: {result['genre_average']:,.0f}원\n"
                    result_text += f"📋 비교 비율: {result['ratio']:.2f}배\n"
                    result_text += f"🎯 시장 위치: {result['position']}\n"
                    result_text += f"📝 분석 샘플: {result['sample_count']}개\n\n"

                    # 성과 해석
                    if result['performance'] == 'excellent':
                        result_text += "🌟 우수한 성과입니다!\n"
                    elif result['performance'] == 'good':
                        result_text += "👍 양호한 성과입니다.\n"
                    elif result['performance'] == 'average':
                        result_text += "📊 평균적인 성과입니다.\n"
                    else:
                        result_text += "💪 개선의 여지가 있습니다.\n"

                    result_text += "\n🔒 모든 비교는 암호화된 상태에서 수행되었습니다.\n\n"
                else:
                    result_text = f"❌ 비교 분석 실패: {result['message']}\n\n"

                self.root.after(0, lambda: self.append_result(result_text))

            except Exception as e:
                self.progress_bar.stop()
                self.set_status(f"❌ 비교 실패: {e}")
                self.root.after(0, lambda: messagebox.showerror(
                    "비교 오류", f"시장 비교 실패:\n{e}"))

        thread = threading.Thread(target=compare_task, daemon=True)
        thread.start()

    def show_privacy_report(self):
        """프라이버시 현황 보고서"""
        if not self.calculator:
            messagebox.showwarning("경고", "시스템이 아직 초기화되지 않았습니다.")
            return

        try:
            report = self.calculator.get_privacy_report()

            result_text = "🔒 프라이버시 보존 현황 보고서\n"
            result_text += "=" * 40 + "\n\n"
            result_text += f"👥 총 참여 아티스트: {report['total_artists']}명\n\n"

            result_text += "🎵 장르별 분포:\n"
            for genre, count in report['genre_distribution'].items():
                result_text += f"   {genre:12s}: {count:3d}명\n"

            result_text += f"\n🛡️  프라이버시 수준: {report['privacy_level']}\n"
            result_text += f"🔐 암호화 방식: {report['encryption_method']}\n"
            result_text += f"⚙️  처리 방식: {report['data_processing']}\n\n"

            result_text += "✅ 보안 특징:\n"
            result_text += "   • 개인 수익 데이터는 절대 노출되지 않음\n"
            result_text += "   • 모든 연산이 암호화된 상태에서 수행\n"
            result_text += "   • 통계 결과만 복호화하여 제공\n"
            result_text += "   • CKKS 동형암호 알고리즘 사용\n\n"

            self.append_result(result_text)

        except Exception as e:
            messagebox.showerror("보고서 오류", f"프라이버시 보고서 생성 실패:\n{e}")

    def run(self):
        """GUI 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
        except Exception as e:
            messagebox.showerror("치명적 오류", f"프로그램 실행 중 오류 발생:\n{e}")


# 메인 실행
if __name__ == "__main__":
    app = MusicRevenueAnalyzerGUI()
    app.run()
