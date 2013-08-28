<?php
 
//対象テキスト
$text = readline("");
 
//テキストのサイズ
//  参考：http://www.cpa-lab.com/tech/0144
$textsize = strlen(bin2hex($text))/2;
 
 
//WMAインスタンス生成
//  引数NULLで標準オプション
$webma = WMA_CreateWebMA(NULL);
 
//WMAにテキストを設定
$left = WMA_PutText($webma, $text, $textsize);
 
//結果表示用
$result = "";
 
while(true){
  $resultStatus = WMA_GetNextToken($webma, $segmentinfo, $termkey);
  if($resultStatus == WMARS_NO_MORE_TEXT){
    break;
  }
  if($resultStatus == WMARS_WANT_MORE_TEXT){
    if($left != 0){
      $left = WMA_PutText($webma, $text, $left);
    }else{
      WMA_NoMoreText($webma);
    }
  }
  else if($resultStatus != WMARS_OK){
    echo "Error...\n";
    break;
  }
  else{
    //解析結果(1形態素ずつ)
    $result .= $segmentinfo["token"]."\t"; //表層(形態素)
    $result .= $segmentinfo["norm"].","; //表記を標準化したもの
    $result .= $segmentinfo["read"].","; //読み
    $result .= WMA_GetPOSName($webma,$segmentinfo["p_o_s"]).","; //品詞(番号を品詞名に直したもの)
    $result .= WMA_GetKatsuyouName($webma,$segmentinfo["p_o_s"],$segmentinfo["katsuyou"]).","; //活用(番号を活用名に直したもの)
    $result .= $segmentinfo["type"].","; //区切り情報の種類
    $result .= $segmentinfo["offset"].","; //形態素の開始位置(文字単位、PutTextごとに変わ る)
    $result .= $segmentinfo["length"].","; //形態素の文字長
    $result .= $segmentinfo["lenstem"].","; //語幹部分の文字長
    $result .= $segmentinfo["bhasdictionaryform"].","; //VMA辞書のID
    $result .= $segmentinfo["wma_flg"]."\n"; //各情報を表すビットフラグ
  }
}
 
//WMAインスタンスの破棄
WMA_DestroyWebMA($webma);
 
//結果の表示
echo $result;
