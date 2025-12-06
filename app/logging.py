import logging
import logging.config
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

LOGGING_CONFIG = {

}


def init_logging() -> None:
    """
    애플리케이션 시작 시 불러서 logging 전체 설정 적용
    """
    # logs 디렉토리 없으면 생성

    os.makedirs("logs", exist_ok=True)
    # 1) 로깅 기본 설정
    # logging.basicConfig(
    #     format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    #     # format="%(asctime)s [%(levelname)s] %(message)s",
    #     level=logging.INFO,  # INFO 이상 레벨만 출력
    #     filename="logs/upstage-network-info.log"
    # )


def create_logger(
        name: str = "app",
        filename="logs/upstage-network-info.log",
        level=logging.INFO,
        console_level=logging.INFO
):
    # 1) 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # # 2) 파일 핸들러 생성
    # file_handler = logging.FileHandler(filename, encoding="utf-8")
    # file_handler.setLevel(level)

    file_handler = TimedRotatingFileHandler(
        filename,
        encoding="utf-8",
        backupCount=5,
        when = "S",  # 초 단위 테스트용, 일반적으로 일/시간 단위 when="D"/ when="H"
    )

    # 3) 포맷터 설정
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s %(filename)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    # 4) 로거에 핸들러 붙이기
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
