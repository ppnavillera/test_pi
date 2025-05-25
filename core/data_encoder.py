"""
데이터 인코딩 모듈
음악 수익 데이터를 동형암호에 적합한 형태로 변환
"""

import numpy as np
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime


class MusicDataEncoder:
    """음악 데이터 인코딩/디코딩 클래스"""

    def __init__(self):
        """인코더 초기화"""
        # 장르 매핑 (원-핫 인코딩용)
        self.genre_mapping = {
            'Pop': 0,
            'Hip-Hop': 1,
            'Rock': 2,
            'Electronic': 3,
            'R&B': 4,
            'Country': 5,
            'Jazz': 6,
            'Classical': 7
        }

        # 기간 매핑
        self.period_mapping = {
            '2024-Q1': 0,
            '2024-Q2': 1,
            '2024-Q3': 2,
            '2024-Q4': 3,
            '2023-Q1': 4,
            '2023-Q2': 5,
            '2023-Q3': 6,
            '2023-Q4': 7
        }

        # 정규화 범위 설정
        self.normalization_ranges = {
            'revenue': (0, 100000000),      # 최대 1억원
            'song_count': (1, 50),          # 1~50곡
            'danceability': (0.0, 1.0),    # 이미 0~1 범위
            'energy': (0.0, 1.0),          # 이미 0~1 범위
            'valence': (0.0, 1.0),         # 이미 0~1 범위
            'tempo': (60, 200),            # 60~200 BPM
            'acousticness': (0.0, 1.0),
            'instrumentalness': (0.0, 1.0),
            'liveness': (0.0, 1.0),
            'speechiness': (0.0, 1.0),
            'loudness': (-60, 0),          # 데시벨
            'duration_ms': (30000, 600000)  # 30초~10분
        }

        print("📝 데이터 인코더 초기화 완료")

    def normalize_value(self, value: float, field_name: str) -> float:
        """
        값을 0~1 범위로 정규화

        Args:
            value: 정규화할 값
            field_name: 필드명

        Returns:
            0~1 범위로 정규화된 값
        """
        if field_name not in self.normalization_ranges:
            return value

        min_val, max_val = self.normalization_ranges[field_name]

        # 범위를 벗어난 값 클리핑
        value = max(min_val, min(max_val, value))

        # 0~1 범위로 정규화
        normalized = (value - min_val) / (max_val - min_val)

        return normalized

    def denormalize_value(self, normalized_value: float, field_name: str) -> float:
        """
        정규화된 값을 원래 범위로 복원

        Args:
            normalized_value: 0~1 범위의 정규화된 값
            field_name: 필드명

        Returns:
            원래 범위로 복원된 값
        """
        if field_name not in self.normalization_ranges:
            return normalized_value

        min_val, max_val = self.normalization_ranges[field_name]

        # 원래 범위로 복원
        denormalized = normalized_value * (max_val - min_val) + min_val

        return denormalized

    def encode_genre(self, genre: str) -> List[float]:
        """
        장르를 원-핫 인코딩

        Args:
            genre: 장르명

        Returns:
            원-핫 인코딩된 벡터
        """
        vector = [0.0] * len(self.genre_mapping)

        if genre in self.genre_mapping:
            vector[self.genre_mapping[genre]] = 1.0

        return vector

    def decode_genre(self, one_hot_vector: List[float]) -> str:
        """
        원-핫 벡터를 장르명으로 디코딩

        Args:
            one_hot_vector: 원-핫 인코딩된 벡터

        Returns:
            장르명
        """
        max_index = one_hot_vector.index(max(one_hot_vector))

        for genre, index in self.genre_mapping.items():
            if index == max_index:
                return genre

        return "Unknown"

    def encode_period(self, period: str) -> List[float]:
        """
        기간을 원-핫 인코딩

        Args:
            period: 기간 (예: "2024-Q1")

        Returns:
            원-핫 인코딩된 벡터
        """
        vector = [0.0] * len(self.period_mapping)

        if period in self.period_mapping:
            vector[self.period_mapping[period]] = 1.0

        return vector

    def encode_music_data(self, music_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """
        음악 데이터를 동형암호용으로 인코딩

        Args:
            music_data: 원본 음악 데이터

        Returns:
            인코딩된 데이터 딕셔너리
        """
        encoded_data = {}

        # 1. 수치형 데이터 정규화
        numeric_fields = ['revenue', 'song_count', 'danceability', 'energy',
                          'valence', 'tempo', 'acousticness', 'instrumentalness',
                          'liveness', 'speechiness', 'loudness', 'duration_ms']

        for field in numeric_fields:
            if field in music_data:
                normalized = self.normalize_value(music_data[field], field)
                encoded_data[field] = [normalized]  # 단일 값을 리스트로

        # 2. 범주형 데이터 원-핫 인코딩
        if 'genre' in music_data:
            encoded_data['genre'] = self.encode_genre(music_data['genre'])

        if 'period' in music_data:
            encoded_data['period'] = self.encode_period(music_data['period'])

        # 3. 메타데이터 (암호화하지 않음)
        encoded_data['metadata'] = {
            'artist_id': music_data.get('artist_id', ''),
            'upload_time': datetime.now().isoformat(),
            'original_genre': music_data.get('genre', ''),
            'original_period': music_data.get('period', '')
        }

        return encoded_data

    def decode_music_data(self, encoded_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        인코딩된 데이터를 원래 형태로 디코딩

        Args:
            encoded_data: 인코딩된 데이터

        Returns:
            디코딩된 원본 데이터
        """
        decoded_data = {}

        # 1. 수치형 데이터 역정규화
        numeric_fields = ['revenue', 'song_count', 'danceability', 'energy',
                          'valence', 'tempo', 'acousticness', 'instrumentalness',
                          'liveness', 'speechiness', 'loudness', 'duration_ms']

        for field in numeric_fields:
            if field in encoded_data and len(encoded_data[field]) > 0:
                normalized_value = encoded_data[field][0]
                original_value = self.denormalize_value(
                    normalized_value, field)
                decoded_data[field] = original_value

        # 2. 범주형 데이터 디코딩
        if 'genre' in encoded_data:
            decoded_data['genre'] = self.decode_genre(encoded_data['genre'])

        if 'period' in encoded_data:
            max_index = encoded_data['period'].index(
                max(encoded_data['period']))
            for period, index in self.period_mapping.items():
                if index == max_index:
                    decoded_data['period'] = period
                    break

        # 3. 메타데이터 복원
        if 'metadata' in encoded_data:
            decoded_data.update(encoded_data['metadata'])

        return decoded_data

    def create_feature_vector(self, music_data: Dict[str, Any]) -> List[float]:
        """
        음악 특성을 하나의 벡터로 결합

        Args:
            music_data: 음악 데이터

        Returns:
            특성 벡터
        """
        encoded_data = self.encode_music_data(music_data)

        feature_vector = []

        # 음악 특성 순서 정의
        feature_order = ['danceability', 'energy', 'valence', 'tempo',
                         'acousticness', 'instrumentalness', 'liveness',
                         'speechiness', 'loudness', 'duration_ms']

        for feature in feature_order:
            if feature in encoded_data:
                feature_vector.extend(encoded_data[feature])
            else:
                feature_vector.append(0.0)  # 기본값

        # 장르와 기간 추가
        if 'genre' in encoded_data:
            feature_vector.extend(encoded_data['genre'])
        else:
            feature_vector.extend([0.0] * len(self.genre_mapping))

        if 'period' in encoded_data:
            feature_vector.extend(encoded_data['period'])
        else:
            feature_vector.extend([0.0] * len(self.period_mapping))

        return feature_vector

    def batch_encode(self, music_data_list: List[Dict[str, Any]]) -> Dict[str, List[List[float]]]:
        """
        여러 음악 데이터를 배치로 인코딩

        Args:
            music_data_list: 음악 데이터 리스트

        Returns:
            배치 인코딩된 데이터
        """
        batch_encoded = {}

        for music_data in music_data_list:
            encoded = self.encode_music_data(music_data)

            for key, value in encoded.items():
                if key != 'metadata':  # 메타데이터는 제외
                    if key not in batch_encoded:
                        batch_encoded[key] = []
                    batch_encoded[key].append(value)

        return batch_encoded


# 테스트 코드
if __name__ == "__main__":
    print("🧪 데이터 인코더 테스트 시작")

    # 인코더 초기화
    encoder = MusicDataEncoder()

    # 테스트 데이터
    test_music_data = {
        'artist_id': 'artist_001',
        'genre': 'Pop',
        'period': '2024-Q1',
        'revenue': 5000000,  # 500만원
        'song_count': 3,
        'danceability': 0.8,
        'energy': 0.7,
        'valence': 0.9,
        'tempo': 120,
        'acousticness': 0.1,
        'instrumentalness': 0.0,
        'liveness': 0.2,
        'speechiness': 0.05,
        'loudness': -5.0,
        'duration_ms': 210000  # 3분 30초
    }

    print("원본 데이터:", test_music_data)

    # 인코딩
    encoded = encoder.encode_music_data(test_music_data)
    print("\n📊 인코딩 결과:")
    for key, value in encoded.items():
        if key != 'metadata':
            print(f"  {key}: {value}")

    # 디코딩
    decoded = encoder.decode_music_data(encoded)
    print("\n🔄 디코딩 결과:")
    for key, value in decoded.items():
        if key in test_music_data:
            original = test_music_data[key]
            print(
                f"  {key}: {value:.3f if isinstance(value, float) else value} (원본: {original})")

    # 특성 벡터 생성
    feature_vector = encoder.create_feature_vector(test_music_data)
    print(f"\n🎯 특성 벡터 길이: {len(feature_vector)}")
    print(f"특성 벡터 (일부): {[round(x, 3) for x in feature_vector[:10]]}")

    print("✅ 데이터 인코더 테스트 완료!")
