import BCSFE_Python_Discord as BCSFE_Python
from BCSFE_Python_Discord import *
import traceback
import random

def main():
    
    country_code = input("국가 코드를 입력하세요 (kr, jp, tw, en): ")
    transfer_code = input("기종변경 코드를 입력하세요: ")
    confirmation_code = input("인증번호를 입력하세요: ")
    game_version = input("게임 버전을 입력하세요 (12.3): ")
    try:
        path = helper.save_file(
            "세이브 저장하기",
            helper.get_save_file_filetype(),
            helper.get_save_path_home(),
        )
        BCSFE_Python.helper.set_save_path(path)
        game_version = helper.str_to_gv(game_version)
        save_data = BCSFE_Python.server_handler.download_save(country_code, transfer_code, confirmation_code, game_version)
        save_data = patcher.patch_save_data(save_data, country_code)
        global save_stats
        save_stats = parse_save.start_parse(save_data, country_code)
        number = int(input("복제할 갯수를 입력하세요 (숫자): "))
        print("복제중... 프로그램을 닫지 마세요")
        list = []
        i = 0
        for i in range(number):
            try:
                print("복제중...{}/{}".format(i, number))
                i += 1
                random_inquiry_code = random.randint(100000, 9999999)
                save_stats["inquiry_code"] = random_inquiry_code
                edits.other.create_new_account.create_new_account(save_stats)
                edits.save_management.save.save_save(save_stats)
                save_data = BCSFE_Python.serialise_save.start_serialize(save_stats)
                
                save_data = BCSFE_Python.helper.write_save_data(
                    save_data, save_stats["version"], helper.get_save_path(), False
                )
                
                upload_data = BCSFE_Python.server_handler.upload_handler(save_stats, helper.get_save_path())
                transfer_code = upload_data['transferCode']
                confirmation_code = upload_data['pin']
                list.append("{}:{}".format(transfer_code, confirmation_code))
                with open("duplicated_account.txt", "a+", encoding="utf-8") as list_file:
                    list_file.write("{}:{}\n".format(transfer_code, confirmation_code))
                
            except:
                pass
        print("복제를 모두 완료하였습니다.\nduplicated_account.txt에 저장하였습니다.\n프로그램을 종료합니다.")
        print(list)
        input()
    except Exception as e:
        print("{}".format(traceback.format_exc()))
        exit(1)





if __name__ == "__main__":
    main()