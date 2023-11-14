import re
import pandas as pd

ma_ttp ={
    'Hà Nội'       : 'HNI', 
    'Vĩnh Phúc'    : 'VPC', 
    'Hoà Bình'     : 'HBH', 
    'Bắc Ninh'     : 'BNH', 
    'Bắc Kạn'      : 'BCN', 
    'Lào Cai'      : 'LCI', 
    'Lạng Sơn'     : 'LSN', 
    'Bắc Giang'    : 'BGG', 
    'Cao Bằng'     : 'CBG', 
    'Thái Nguyên'  : 'TNN', 
    'Phú Thọ'      : 'PTO', 
    'Tuyên Quang'  : 'TQG', 
    'Yên Bái'      : 'YBI', 
    'Sơn La'       : 'SLA', 
    'Điện Biên'    : 'DBN', 
    'Lai Châu'     : 'LCU', 
    'Hà Giang'     : 'HGG', 
    'Hà Nam'       : 'HNM', 
    'Nam Định'     : 'NDH', 
    'Thái Bình'    : 'TBH', 
    'Hải Dương'    : 'HDG', 
    'Hải Phòng'    : 'HPG', 
    'Quảng Ninh'   : 'QNH', 
    'Hưng Yên'     : 'HYN', 
    'Ninh Bình'    : 'NBH', 
    'Thanh Hóa'    : 'THA', 
    'Nghệ An'      : 'NAN', 
    'Hà Tĩnh'      : 'HTH', 
    'Quảng Bình'   : 'QBH', 
    'Quảng Trị'    : 'QTI', 
    'Thừa Thiên - Huế': 'HUE', 
    'Quảng Nam'    : 'QNM', 
    'Quảng Ngãi'   : 'QNI', 
    'Bình Định'    : 'BDH', 
    'Gia Lai'      : 'GLI', 
    'Đắk Lắk'      : 'DLC', 
    'Đắk Nông'     : 'DKN', 
    'Phú Yên'      : 'PYN', 
    'Khánh Hòa'    : 'KHA', 
    'Kon Tum'      : 'KTM', 
    'Đà Nẵng'      : 'DNG', 
    'Lâm Đồng'     : 'LDG', 
    'Bình Thuận'   : 'BTN', 
    'Ninh Thuận'   : 'NTN', 
    'Hồ Chí Minh'  : 'HCM', 
    'Đồng Nai'     : 'DNI', 
    'Bình Dương'   : 'BDG', 
    'Tây Ninh'     : 'TNH', 
    'Bà Rịa - Vũng Tàu': 'VTU', 
    'Bình Phước'   : 'BPC', 
    'Long An'      : 'LAN', 
    'Tiền Giang'   : 'TGG', 
    'Bến Tre'      : 'BTE', 
    'Trà Vinh'     : 'TVH', 
    'Vĩnh Long'    : 'VLG', 
    'Cần Thơ'      : 'CTO', 
    'Hậu Giang'    : 'HAG', 
    'Đồng Tháp'    : 'DTP', 
    'An Giang'     : 'AGG', 
    'Kiên Giang'   : 'KGG', 
    'Cà Mau'       : 'CMU', 
    'Sóc Trăng'    : 'STG', 
    'Bạc Liêu'     : 'BLU',
    'Không xác định'    : '000'
    }

ma_mien = {
    "HNI": "MB",
    "VPC": "MB",
    "HBH": "MB",
    "BNH": "MB",
    "BCN": "MB",
    "LCI": "MB",
    "LSN": "MB",
    "BGG": "MB",
    "CBG": "MB",
    "TNN": "MB",
    "PTO": "MB",
    "TQG": "MT",
    "YBI": "MB",
    "SLA": "MB",
    "DBN": "MB",
    "LCU": "MB",
    "HGG": "MB",
    "HNM": "MB",
    "NDH": "MB",
    "TBH": "MB",
    "HDG": "MB",
    "HPG": "MT",
    "QNH": "MB",
    "HYN": "MB",
    "NBH": "MT",
    "THA": "MB",
    "NAN": "MT",
    "HTH": "MT",
    "QBH": "MT",
    "QTI": "MT",
    "HUE": "MT",
    "QNM": "MT",
    "QNI": "MT",
    "BDH": "MT",
    "GLI": "MT",
    "DLC": "MT",
    "DKN": "MT",
    "PYN": "MT",
    "KHA": "MT",
    "KTM": "MT",
    "DNG": "MT",
    "LDG": "MN",
    "BTN": "MN",
    "NTN": "MN",
    "HCM": "MN",
    "DNI": "MN",
    "BDG": "MN",
    "TNH": "MN",
    "VTU": "MN",
    "BPC": "MN",
    "LAN": "MN",
    "TGG": "MN",
    "BTE": "MN",
    "TVH": "MN",
    "VLG": "MN",
    "CTO": "MN",
    "HAG": "MN",
    "DTP": "MN",
    "AGG": "MN",
    "KGG": "MN",
    "CMU": "MN",
    "STG": "MN",
    "BLU": "MN",
    "000": "00"
}

list_ttp = [
    'Hà Nội',
    'Hoà Bình', 
    'Bắc Ninh',
    'Bắc Kạn',
    'Lào Cai',
    'Lạng Sơn',
    'Bắc Giang',
    'Cao Bằng',
    'Thái Nguyên', 
    'Phú Thọ',
    'Tuyên Quang',
    'Yên Bái',
    'Sơn La',
    'Điện Biên',
    'Lai Châu',
    'Hà Giang',
    'Hà Nam',
    'Nam Định',
    'Thái Bình',
    'Hải Dương',
    'Hải Phòng', 
    'Quảng Ninh',
    'Vĩnh Phúc',
    'Hưng Yên',
    'Ninh Bình',
    'Thanh Hóa',
    'Nghệ An', 
    'Hà Tĩnh',
    'Quảng Bình',
    'Quảng Trị', 
    'Thừa Thiên - Huế',
    'Quảng Nam', 
    'Quảng Ngãi',
    'Bình Định',
    'Gia Lai',
    'Đắk Lắk',
    'Đắk Nông',
    'Phú Yên',
    'Khánh Hòa',
    'Kon Tum',
    'Đà Nẵng',
    'Lâm Đồng',
    'Bình Thuận',
    'Ninh Thuận',
    'Hồ Chí Minh',
    'Đồng Nai',
    'Bình Dương', 
    'Tây Ninh',
    'Bà Rịa - Vũng Tàu',
    'Bình Phước',
    'Long An',
    'Tiền Giang', 
    'Bến Tre',
    'Trà Vinh',
    'Vĩnh Long',
    'Cần Thơ',
    'Hậu Giang', 
    'Đồng Tháp',
    'An Giang',
    'Kiên Giang', 
    'Cà Mau',
    'Sóc Trăng',
    'Bạc Liêu'
    ]

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def get_city_name(location, list_ttp):
    location = no_accent_vietnamese(location)
    location = location.lower()
    location = location.replace(' ','')
    
    list_ttp_solved = [get_location_name(city.lower()) for city in list_ttp]
    list_ttp_solved = [no_accent_vietnamese(city_lower) for city_lower in list_ttp_solved]
    list_ttp_solved = [city_lower.replace(' ','') for city_lower in list_ttp_solved]
    
    list_index = [location.rfind(city) for city in list_ttp_solved ]
    max_value = max(list_index)
    if max_value == -1:
        return ''
    else:
        index_max_value = list_index.index(max_value)
        return list_ttp[index_max_value]

def get_city_code(city, ma_ttp):
    return ma_ttp[city]

def get_city_area(city_code, ma_mien):
    return ma_mien[city_code]

def get_location_name(s):
    s = re.sub(r'^thành phố|^huyện|^quận|^thị xã|^tx|^tt|^xã|^thị trấn|^tp|^tỉnh|^phường', '', s)
    s = s.strip()
    return s

def get_district_town_name(city,location,info_full):
    town, district = '',''
    
    full_district = info_full.loc[info_full['Tỉnh Thành Phố'] == city]
    full_district = full_district.drop_duplicates(subset=['Quận Huyện'], keep='first', ignore_index=True)
    
    city_solved = get_location_name(city.lower())
    city_solved = no_accent_vietnamese(city_solved).replace(' ','')
    
    list_district = full_district['Quận Huyện'].values.tolist()
    list_district.sort(key=lambda s: len(s))
    list_district_lower = [get_location_name(district.lower()) for district in list_district]
    list_district_lower = [no_accent_vietnamese(district) for district in list_district_lower]
    list_district_lower = [district.replace(' ','') for district in list_district_lower]
        
    location = location.lower()
    location = location.replace(' ','')
    # index_city = location.rfind(city_solved)
    location = no_accent_vietnamese(location)
    index_city = location.rfind(city_solved)
    # location = location.replace(' ','')
    
    if index_city == -1:
        return ['','']
    else: 
        location = location[:index_city]
    
        list_index_district = [location.rfind(value) for value in list_district_lower]
        max_value_district = -1
        if len(list_index_district) <= 1:
            return ['','']
        else:
            for i in reversed(list_index_district):
                if i != -1:
                    max_value_district = i
                    break
            if max_value_district == -1:
                return ['','']
            else:
                index_max_value_district = [index for index, item in enumerate(list_index_district) if item == max_value_district][-1]
                district = list_district[index_max_value_district]

                full_town = info_full.loc[(info_full['Tỉnh Thành Phố'] == city) & (info_full['Quận Huyện'] == district)]
                
                list_town = full_town['Phường Xã'].values.tolist()
                list_town.sort(key=lambda s: len(s))
                list_town_solved = [get_location_name(town.lower()) for town in list_town]
                list_town_solved = [no_accent_vietnamese(town) for town in list_town_solved]
                list_town_solved = [town.replace(' ','') for town in list_town_solved]
                
                district_solve = get_location_name(district.lower())
                district_solve = no_accent_vietnamese(district_solve)
                district_solve = district_solve.replace(' ','')
                
                index_district = location.rfind(district_solve)
                location = location[:index_district]
                
                list_index_town= [location.rfind(value) for value in list_town_solved]
                max_value_town = -1
                if len(list_index_town) <= 1:
                    return [district,'']
                else:
                    for i in reversed(list_index_town):
                        if i != -1:
                            max_value_town = i
                            break
                    if max_value_town == -1:
                        return [district,'']
                    else:
                        index_max_value_town = [index for index, item in enumerate(list_index_town) if item == max_value_town][-1]
                        town = list_town[index_max_value_town]
                        return [district,town]

if __name__ == '__main__':
    info_full = pd.read_csv('/Users/dinhvan/Projects/Code/jupyter/split_location_detail/don_vi_hanh_chinh/don_vi_hanh_chinh.csv',dtype = str)
    location = '33 Phạm Hùng, 9, Vĩnh Long, Vĩnh Long'
    city = get_city_name(location, list_ttp)
    print(city)
    city_code = get_city_code(city, ma_ttp)
    print(city_code)
    city_area = get_city_area(city_code, ma_mien)
    print(city_area)
    print(get_district_town_name(city,location,info_full))
