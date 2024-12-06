import random
import math


def rand_gauss(
        data: list | set | tuple,
        center_index: int = None,
) -> any:
    """
    선택한 인덱스를 중심으로 정규분포에 기반한 랜덤 요소를 리턴하는 함수
    
    :param data: 랜덤값 뽑을 리스트
    :param center_index: 정규분포 평균 인덱스 (중심)

    :raise ValueError: center_index가 data의 index 범위에서 벗어났을 때
    """

    if center_index is None:
        center_index = len(data) // 2
    elif not 0 <= center_index < len(data):
        raise ValueError(f'center_index {center_index} is out of range')

    sigma = len(data) / 6

    # 정규분포 기반 가중치 계산
    weights = [
        math.exp(-0.5 * ((i - center_index) / sigma) ** 2)  # 가우스 공식
        for i in range(len(data))
    ]

    # 가중치를 사용해 선택
    return random.choices(data, weights=weights, k=1)[0]
