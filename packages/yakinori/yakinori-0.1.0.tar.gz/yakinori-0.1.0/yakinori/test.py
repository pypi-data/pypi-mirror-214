from yakinori import Yakinori
import ipdb

yakinori = Yakinori("/usr/local/lib/mecab/dic/mecab-unidic-neologd")
# yakinori = Yakinori()
text_list = [
    "幽☆遊☆白書は最高の漫画です",
    "そういえば今日は新宿スワンがみたいですんね。。。",
    "人工知能学会ってどのくらいすごいんですかね？",
    "ACLに通りたい人生だった",
    "任せればいいや",
    "通りたい",
    "デフォルトでは\1, \2, \3...が、それぞれ1つ目の()、2つ目の()、3つ目の()...にマッチした部分に対応している。raw文字列ではない通常の文字列だと'\\1'のように\をエスケープする必要があるので注意。"
]
for text in text_list:
    print(text)
    parsed_list = yakinori.get_parsed_list(text)
    katakana_sentence = yakinori.get_katakana_sentence(parsed_list)
    hiragana_sentence = yakinori.get_hiragana_sentence(parsed_list)
    roma_sentence = yakinori.get_roma_sentence(parsed_list)
    print("読み")
    print(katakana_sentence)
    print(hiragana_sentence)
    print(roma_sentence)

    katakana_sentence = yakinori.get_katakana_sentence(parsed_list, is_hatsuon=True)
    hiragana_sentence = yakinori.get_hiragana_sentence(parsed_list, is_hatsuon=True)
    roma_sentence = yakinori.get_roma_sentence(parsed_list, is_hatsuon=True)
    print("発音")
    print(katakana_sentence)
    print(hiragana_sentence)
    print(roma_sentence)
    print('\n')
