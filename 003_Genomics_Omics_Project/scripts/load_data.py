# 필요한 라이브러리를 불러온다.
import pandas as pd
import os
import urllib.request
import gzip
import shutil
# 'sys' 모듈을 사용해서 스크립트 파일 위치를 확실히 찾는다.
import sys 

def download_and_extract_data(gse_number):
    
    """
    GSE 번호를 받아서 GEO 데이터 파일을 다운로드하고 압축을 푼다.
    """ 
    # [수정 시작]: 실행 위치와 관계없이 스크립트 파일의 실제 위치를 기준으로 data 폴더 경로를 잡는다.
    
    # 실행 방식(터미널 vs 주피터)에 상관없이 이 파일의 진짜 위치를 찾는다.
    # __file__이 없으면 (대화형 셸) sys.argv[0]을 쓴다.
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # 현재 폴더(scripts)에서 한 단계 위(..)로 올라가서 'data' 폴더를 최종 저장 경로로 잡는다.
    # 이렇게 하면 폴더 구조가 바뀌어도 data 경로 꼬일 일 없다.
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    # [수정 종료]

    # GSE 번호에서 FTP 경로를 구성하는 접두사(e.g., '16nnn' for GSE16515)를 추출.
    gse_id_number = gse_number.replace('GSE', '')
    gse_prefix = gse_id_number[:len(gse_id_number)-3] + 'nnn'
    
    file_name = f"{gse_number}_series_matrix.txt.gz"
    
    # 데이터가 저장된 NCBI FTP의 URL을 만든다.
    download_url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/GSE{gse_prefix}/{gse_number}/matrix/{file_name}"

    # 로컬 임시 파일 경로를 설정한다.
    local_gz_path = os.path.join(data_dir, file_name)
    uncompressed_file_path = local_gz_path.replace(".gz", "") # 압축 해제 후 파일 경로
    
    # try...except를 써서 혹시 모를 오류를 대비.
    try:
        print(f"--- 처리 파일: {file_name} ---")
        print(f"다운로드 URL: {download_url}")
        
        # 파일이 이미 압축 해제까지 완료되었는지 확인하고 건너뛴다.
        if os.path.exists(uncompressed_file_path):
            print(f"이미 파일 있음: {os.path.basename(uncompressed_file_path)}. 다운로드 스킵.")
            
            # 절대 경로를 얻은 후, 출력 직전에 \\를 /로 바꿔준다. (핵심 수정 부분)
            absolute_path = os.path.abspath(uncompressed_file_path).replace('\\', '/')
            print(f"\n[저장 위치]: 파일이 이 경로에 있다. ➡ {absolute_path}")
            
            return # 이미 있으면 함수 종료

        print(f"Downloading {file_name}...")
        # 데이터 다운로드 (urllib.request.urlretrieve 사용)
        urllib.request.urlretrieve(download_url, local_gz_path)
        print(f"다운로드 완료: {file_name}")
        
        # .gz 파일 압축 해제 시작
        if file_name.endswith(".gz"):
            with gzip.open(local_gz_path, 'rb') as f_in:
                with open(uncompressed_file_path, 'wb') as f_out:
                    # shutil.copyfileobj로 압축 해제된 데이터를 새 파일에 쓴다.
                    shutil.copyfileobj(f_in, f_out)
            print(f"압축 해제 끝. 파일명: {os.path.basename(uncompressed_file_path)}")
            
            # 최종 저장된 절대 경로를 다시 한번 출력한다. (핵심 수정 부분)
            absolute_path = os.path.abspath(uncompressed_file_path).replace('\\', '/')
            print(f"\n[저장 위치]: 최종 절대 경로 확인. ➡ {absolute_path}")
            
            # 원본 .gz 파일 삭제
            os.remove(local_gz_path)
            print(f"원본 gz 파일 삭제함: {os.path.basename(local_gz_path)}")
        else:
            print("gz 파일이 아님. 압축 해제 스킵.")
        
    except Exception as e:
        # 에러 발생 시 에러 메시지 출력 후 다음 단계로 넘어간다.
        print(f"에러 발생. 다운로드/압축 해제 오류 ({file_name}): {e}")
        if os.path.exists(local_gz_path):
            # 오류 발생 시 불완전한 파일 삭제해서 정리.
            os.remove(local_gz_path)
    print("-" * (20 + len(file_name)))

# 이 스크립트가 직접 실행될 때, GSE 번호를 인자로 넣어 함수를 호출한다.
if __name__ == "__main__":
    GSE_ID = "GSE16515"
    download_and_extract_data(GSE_ID)
