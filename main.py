from typing import List

def path_to_file_list(path: str) -> List[str]:
    """Reads a file and returns a list of lines in the file"""
    # 'w'는 쓰기 모드이므로 읽기 전용인 'r'로 변경함
    lines = open(path, 'r').read().split('\n')
    return lines

def train_file_list_to_json(english_file_list: List[str], german_file_list: List[str]) -> List[str]:
    """Converts two lists of file paths into a list of json strings"""
    # Preprocess unwanted characters
    def process_file(file):
        if '\\' in file:
            file = file.replace('\\', '\\')
        if '/' or '"' in file:
            file = file.replace('/', '\\/')
            file = file.replace('"', '\\"')
        return file

    # Template for json file
    # key 값을 정확히 반영 ("English", "German")
    template_start = '{\"English\":\"'
    template_mid = '\",\"German\":\"'
    template_end = '\"}'

    # Can this be working?
    processed_file_list = []
    for english_file, german_file in zip(english_file_list, german_file_list):
        english_file = process_file(english_file)
        # 독립적으로 각각의 파일명을 이스케이프 처리함 
        german_file = process_file(german_file)
        # 포맷을 template_start + english + template_mid + german + template_end 순으로 구성
        processed_file_list.append(template_start + english_file + template_mid + german_file + template_end)
    return processed_file_list


def write_file_list(file_list: List[str], path: str) -> None:
    """Writes a list of strings to a file, each string on a new line"""
    # 파일에 쓰기 위해 'r'이 아닌 'w' 모드 사용, 줄바꿈 포함하여 각 항목 쓰기
    with open(path, 'w') as f:
        for file in file_list:
            f.write(file + '\n')
            
if __name__ == "__main__":
    path = './'
    german_path = './german.txt'
    english_path = './english.txt'

    english_file_list = path_to_file_list(english_path)
    # path_to_file_list는 파일 경로를 받는 함수이므로, 리스트가 아닌 텍스트 파일로부터 리스트 생성
    german_file_list = path_to_file_list(german_path)
    # train_file_list_to_json 함수로 리스트들을 JSON 문자열 리스트로 변환
    processed_file_list = train_file_list_to_json(english_file_list, german_file_list)

    write_file_list(processed_file_list, path+'concated.json')
