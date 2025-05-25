"""
동형암호 엔진 - pi-heaan 기반
음악가 수익 데이터를 암호화하고 암호화된 상태에서 연산을 수행
"""

import piheaan as heaan
import os
import numpy as np
from typing import List, Dict, Any, Optional


class HEEngine:
    """동형암호(HE) 연산을 위한 핵심 엔진"""

    def __init__(self, log_slots: int = 10):
        """
        HE 엔진 초기화

        Args:
            log_slots: 슬롯 개수의 로그값 (2^log_slots 개의 데이터를 한 번에 처리)
        """
        print("🔐 동형암호 엔진 초기화 중...")

        # CKKS 파라미터 설정
        self.params = heaan.ParameterPreset.FGb
        self.context = heaan.make_context(self.params)
        heaan.make_bootstrappable(self.context)

        self.log_slots = log_slots
        self.num_slots = 2 ** log_slots

        # 키 생성 및 저장
        self.key_file_path = "./keys"
        self._setup_keys()

        # 암호화/복호화/연산 객체 생성
        self.evaluator = heaan.HomEvaluator(self.context, self.pk)
        self.decryptor = heaan.Decryptor(self.context)
        self.encryptor = heaan.Encryptor(self.context)

        print(f"✅ HE 엔진 초기화 완료 (슬롯 수: {self.num_slots})")

    def _setup_keys(self):
        """암호화 키 설정"""
        # 키 저장 디렉토리 생성
        os.makedirs(self.key_file_path, mode=0o775, exist_ok=True)

        # 비밀키 생성
        self.sk = heaan.SecretKey(self.context)

        # 공개키 생성
        key_generator = heaan.KeyGenerator(self.context, self.sk)
        key_generator.gen_common_keys()
        self.pk = key_generator.get_public_key()

        print("🔑 암호화 키 생성 완료")

    def encrypt_data(self, data: List[float]) -> heaan.Ciphertext:
        """
        데이터를 암호화

        Args:
            data: 암호화할 실수 리스트 (0~1 범위 권장)

        Returns:
            암호화된 ciphertext
        """
        if len(data) > self.num_slots:
            raise ValueError(
                f"데이터 크기({len(data)})가 슬롯 수({self.num_slots})를 초과합니다.")

        # 데이터를 슬롯 크기만큼 패딩
        padded_data = data + [0.0] * (self.num_slots - len(data))

        # Message 객체 생성
        message = heaan.Message(self.log_slots)
        for i, value in enumerate(padded_data):
            message[i] = complex(value)  # CKKS는 복소수를 지원

        # 암호화
        ciphertext = heaan.Ciphertext(self.context)
        self.encryptor.encrypt(message, self.pk, ciphertext)

        return ciphertext

    def decrypt_data(self, ciphertext: heaan.Ciphertext, size: int = None) -> List[float]:
        """
        암호문을 복호화

        Args:
            ciphertext: 복호화할 암호문
            size: 반환할 데이터 크기 (None이면 전체)

        Returns:
            복호화된 실수 리스트
        """
        # 복호화
        message = heaan.Message(self.log_slots)
        self.decryptor.decrypt(ciphertext, self.sk, message)

        # 복소수에서 실수 부분만 추출
        result = []
        actual_size = size if size else self.num_slots

        for i in range(actual_size):
            value = message[i].real  # 실수 부분만 사용
            result.append(value)

        return result

    def add_encrypted(self, ctxt1: heaan.Ciphertext, ctxt2: heaan.Ciphertext) -> heaan.Ciphertext:
        """암호화된 상태에서 덧셈"""
        result = heaan.Ciphertext(self.context)
        self.evaluator.add(ctxt1, ctxt2, result)
        return result

    def multiply_encrypted(self, ctxt1: heaan.Ciphertext, ctxt2: heaan.Ciphertext) -> heaan.Ciphertext:
        """암호화된 상태에서 곱셈"""
        result = heaan.Ciphertext(self.context)
        self.evaluator.mult(ctxt1, ctxt2, result)
        return result

    def multiply_by_constant(self, ctxt: heaan.Ciphertext, constant: float) -> heaan.Ciphertext:
        """암호화된 데이터에 상수 곱셈"""
        result = heaan.Ciphertext(self.context)
        self.evaluator.mult_by_const(ctxt, complex(constant), result)
        return result

    def add_constant(self, ctxt: heaan.Ciphertext, constant: float) -> heaan.Ciphertext:
        """암호화된 데이터에 상수 덧셈"""
        result = heaan.Ciphertext(self.context)
        self.evaluator.add_const(ctxt, complex(constant), result)
        return result

    def calculate_encrypted_sum(self, encrypted_list: List[heaan.Ciphertext]) -> heaan.Ciphertext:
        """
        여러 암호문의 합계 계산

        Args:
            encrypted_list: 암호화된 데이터 리스트

        Returns:
            합계가 계산된 암호문
        """
        if not encrypted_list:
            raise ValueError("빈 리스트입니다.")

        result = encrypted_list[0]

        for i in range(1, len(encrypted_list)):
            result = self.add_encrypted(result, encrypted_list[i])

        return result

    def calculate_encrypted_average(self, encrypted_list: List[heaan.Ciphertext]) -> heaan.Ciphertext:
        """
        여러 암호문의 평균 계산

        Args:
            encrypted_list: 암호화된 데이터 리스트

        Returns:
            평균이 계산된 암호문
        """
        total_sum = self.calculate_encrypted_sum(encrypted_list)
        count = len(encrypted_list)

        # 개수로 나누기 (상수 곱셈으로 구현)
        average = self.multiply_by_constant(total_sum, 1.0 / count)

        return average

    def encrypt_revenue_data(self, revenue_data: Dict[str, Any]) -> Dict[str, heaan.Ciphertext]:
        """
        수익 데이터 전체를 암호화

        Args:
            revenue_data: 수익 관련 데이터 딕셔너리

        Returns:
            암호화된 데이터 딕셔너리
        """
        encrypted_data = {}

        # 수치형 데이터만 암호화
        numeric_fields = ['revenue', 'danceability',
                          'energy', 'valence', 'tempo']

        for field in numeric_fields:
            if field in revenue_data:
                value = float(revenue_data[field])

                # 정규화 (0~1 범위로)
                if field == 'revenue':
                    # 수익은 로그 스케일로 정규화 (최대 1억원 가정)
                    normalized_value = min(value / 100000000, 1.0)
                elif field == 'tempo':
                    # BPM은 60~200 범위를 0~1로 정규화
                    normalized_value = (value - 60) / 140
                else:
                    # 나머지는 이미 0~1 범위
                    normalized_value = value

                # 단일 값을 리스트로 만들어 암호화
                encrypted_data[field] = self.encrypt_data([normalized_value])

        return encrypted_data


# 테스트 코드
if __name__ == "__main__":
    print("🧪 HE 엔진 테스트 시작")

    # HE 엔진 초기화
    he_engine = HEEngine(log_slots=5)  # 32개 슬롯

    # 테스트 데이터
    test_data1 = [0.1, 0.2, 0.3, 0.4, 0.5]
    test_data2 = [0.2, 0.3, 0.4, 0.5, 0.6]

    # 암호화
    print("🔐 데이터 암호화 중...")
    ctxt1 = he_engine.encrypt_data(test_data1)
    ctxt2 = he_engine.encrypt_data(test_data2)

    # 암호화된 상태에서 덧셈
    print("➕ 암호화된 상태에서 덧셈 수행")
    result_add = he_engine.add_encrypted(ctxt1, ctxt2)
    decrypted_add = he_engine.decrypt_data(result_add, len(test_data1))

    print(f"원본1: {test_data1}")
    print(f"원본2: {test_data2}")
    print(
        f"암호화 덧셈 결과: {[round(x, 3) for x in decrypted_add[:len(test_data1)]]}")
    print(
        f"실제 덧셈 결과: {[round(a+b, 3) for a, b in zip(test_data1, test_data2)]}")

    # 평균 계산 테스트
    print("\n📊 평균 계산 테스트")
    encrypted_list = [ctxt1, ctxt2]
    avg_result = he_engine.calculate_encrypted_average(encrypted_list)
    decrypted_avg = he_engine.decrypt_data(avg_result, len(test_data1))

    print(
        f"암호화 평균 결과: {[round(x, 3) for x in decrypted_avg[:len(test_data1)]]}")
    expected_avg = [(a+b)/2 for a, b in zip(test_data1, test_data2)]
    print(f"실제 평균 결과: {[round(x, 3) for x in expected_avg]}")

    print("✅ HE 엔진 테스트 완료!")
