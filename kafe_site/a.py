import json


kampanya_path=r'C:\Users\MONSTER\3D Objects\yazprojeler\KAFE\kafe_site\json\kampanya.json'
def json_dosya_oku(dosya_adi):
      try:
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            return json.load(f)
      except FileNotFoundError:
        return "dosya bulunmadı"
      except json.JSONDecodeError:
        return []
kampanyalar = json_dosya_oku(kampanya_path)
print("JSON dosya yolu:", kampanya_path)

import json

def json_dosya_oku(dosya_yolu):
    try:
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            isim=json.load(f)
            return isim
    except FileNotFoundError:
        print("Dosya bulunamadı.")
        return []
    except json.JSONDecodeError:
        print("JSON dosyası bozuk.")
        return []
print(json_dosya_oku(kampanya_path))