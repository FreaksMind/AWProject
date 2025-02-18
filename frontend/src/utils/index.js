export function isValidJwt (jwt) {
    if (!jwt || jwt.split('.').length < 3) {
      return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp

}

export function isAppointmentDate(date){
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();

  let today_date = yyyy + '-' + mm + '-' + dd;

  let split_date = date.split(' ')[0]
  if(split_date == today_date)
    return true;
  else
    return false;
}

export function Utf8ArrayToStr(array) {
  var out, i, len, c;
  var char2, char3;

  out = "";
  len = array.length;
  i = 0;
  while(i < len) {
  c = array[i++];
  switch(c >> 4)
  { 
    case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
      // 0xxxxxxx
      out += String.fromCharCode(c);
      break;
    case 12: case 13:
      // 110x xxxx   10xx xxxx
      char2 = array[i++];
      out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
      break;
    case 14:
      // 1110 xxxx  10xx xxxx  10xx xxxx
      char2 = array[i++];
      char3 = array[i++];
      out += String.fromCharCode(((c & 0x0F) << 12) |
                     ((char2 & 0x3F) << 6) |
                     ((char3 & 0x3F) << 0));
      break;
  }
  }

  return out;
}

export function convertWordArrayToUint8Array(wordArray) {
      var arrayOfWords = wordArray.hasOwnProperty("words") ? wordArray.words : [];
      var length = wordArray.hasOwnProperty("sigBytes") ? wordArray.sigBytes : arrayOfWords.length * 4;
      var uInt8Array = new Uint8Array(length), index=0, word, i;
      for (i=0; i<length; i++) {
          word = arrayOfWords[i];
          uInt8Array[index++] = word >> 24;
          uInt8Array[index++] = (word >> 16) & 0xff;
          uInt8Array[index++] = (word >> 8) & 0xff;
          uInt8Array[index++] = word & 0xff;
      }
      return uInt8Array;
  }