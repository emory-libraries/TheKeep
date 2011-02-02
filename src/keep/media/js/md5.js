/* Asynchronous streamable MD5.
 *
 * The MD5 algorithm here is based on:
 *
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Version 2.2 Copyright (C) Paul Johnston 1999 - 2009
 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
 * Distributed under the BSD License
 * See http://pajhome.org.uk/crypt/md5 for more info.
 *
 * With modifications from Emory University Libraries to enable streaming
 */

/* constructor for a streamable MD5 calculator. Use:
 *   var md5 = new MD5();
 *   md5.process_bytes("abc");
 *   md5.process_bytes("12345");
 *   md5.finish();
 *   var result = md5.toString();
 */
function MD5() {
  // magic numbers from the MD5 algorithm
  this.a =  1732584193;
  this.b = -271733879;
  this.c = -1732584194;
  this.d =  271733878;

  this.offset = 0;  // bytes processed so far
  this.buffer = ""; // bytes buffered for processing once we have a whole block
}

/* represent the MD5 state as an Array */
MD5.prototype.asArray = function() {
  return Array(this.a, this.b, this.c, this.d);
};

(function() {
  /* Append bytes to the MD5 state. Immediately process any complete blocks,
   * and buffer any leftover data for when we have a complete block.
   */
  MD5.prototype.process_bytes = function(bytes) {
    if (this.buffer.length + bytes.length < 64) {
      // not enough data between current buffer and the new bytes for a
      // complete block. just buffer.
      this.buffer = this.buffer + bytes;
    } else {
      // we have at least one block. construct the first block manually by
      // combining the buffered data and the new bytes.
      var i = 64 - this.buffer.length
      var block_str = this.buffer + bytes.substring(0, i)
      var block = make_block(block_str);
      this.process_block(block, 0);
      this.buffer = "";

      // keep pulling all complete blocks from the data
      for (/* i initialized above */;
           i + 64 < bytes.length;
           i += 64) {
        var block = make_block(bytes.substring(i, i + 64));
        this.process_block(block, 0);
      }

      // buffer any bytes we didn't use
      this.buffer = bytes.substring(i);
    }
  };

  /* Mark the end of data. MD5 says we pad the data out to block boundaries,
   * so we do that and then append any final blocks to the calculator.
   */
  MD5.prototype.finish = function() {
    var block = make_block(this.buffer);
    this.bump_bytes(this.buffer.length);
    pad(block, this.offset, this.buffer.length);
    this.buffer = "";

    // This could actually result in 1 or 2 full blocks remaining. Process
    // whatever we've got.
    for (var i = 0; i < block.length; i += 16)
      this.process_block(block, i);
  };

  /* Put input data into a block array for MD5 processing. Derived from
   * rstr2binl() in source implementation.
   */
  function make_block(input)
  {
    var output = Array(input.length >> 2);
    for(var i = 0; i < output.length; i++)
      output[i] = 0;
    for(var i = 0; i < input.length * 8; i += 8)
      output[i>>5] |= (input.charCodeAt(i / 8) & 0xFF) << (i%32);
    return output;
  }

  /* Pad an end-of-file block array per MD5 algorithm. */
  function pad(block, total_bytes, block_bytes) {
    var total_bits = total_bytes * 8;
    var block_bits = block_bytes * 8;

    block[block_bits >> 5] |= 0x80 <<((block_bits) % 32);
    block[(((block_bits + 64) >>> 9) << 4) + 14] = total_bits;
  }

})();

(function() {
  /* Append a single full block of data to our calculator according to the
   * MD5 algorithm.
   */
  MD5.prototype.process_block = function(x, i) {
    var a = this.a;
    var b = this.b;
    var c = this.c;
    var d = this.d;

    a = ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = ff(c, d, a, b, x[i+10], 17, -42063);
    b = ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = ff(d, a, b, c, x[i+13], 12, -40341101);
    c = ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = ff(b, c, d, a, x[i+15], 22,  1236535329);

    a = gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = gg(c, d, a, b, x[i+11], 14,  643717713);
    b = gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = gg(c, d, a, b, x[i+15], 14, -660478335);
    b = gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = gg(b, c, d, a, x[i+12], 20, -1926607734);

    a = hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = hh(b, c, d, a, x[i+14], 23, -35309556);
    a = hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = hh(d, a, b, c, x[i+12], 11, -421815835);
    c = hh(c, d, a, b, x[i+15], 16,  530742520);
    b = hh(b, c, d, a, x[i+ 2], 23, -995338651);

    a = ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = ii(c, d, a, b, x[i+10], 15, -1051523);
    b = ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = ii(d, a, b, c, x[i+15], 10, -30611744);
    c = ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = ii(b, c, d, a, x[i+ 9], 21, -343485551);

    this.a = safe_add(a, this.a);
    this.b = safe_add(b, this.b);
    this.c = safe_add(c, this.c);
    this.d = safe_add(d, this.d);

    this.bump_bytes(64);
  };

  /* Increase the reported number of bytes processed.
   *
   * FIXME: This uses, in effect, 32-bit integers to count the bytes. MD5
   * padding uses a 64-bit integer of bits. This *should* work with files
   * >2GB, but will probably fail for files >4GB. If that happens, we may
   * need to figure out how to record and add numbers that size. js numbers,
   * which are stored as double-precision floating points *should* be
   * lossless up to 2**53, but there are two potential pitfalls with this:
   * 1) the original MD5 code we're pulling from mentions some large integer
   * adding bugs in IE, and 2) MD5 goes up to 2**64, which is > 2**53.
   * Fortunately, all we need to do is add positive integers, which should
   * be pretty simple to implement, even if we have to do it manually.
   *
   * Anyway, that's why adding bytes gets its own function here.
   */
  MD5.prototype.bump_bytes = function(n) {
    this.offset = safe_add(n, this.offset);
  }

  /* These next few functions are imported from the source MD5
   * implementation, where they're described as implementing the basic MD5
   * operations.
   */
  function cmn(q, a, b, x, s, t) {
    return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b);
  }

  function ff(a, b, c, d, x, s, t) {
    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
  }

  function gg(a, b, c, d, x, s, t) {
    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
  }

  function hh(a, b, c, d, x, s, t) {
    return cmn(b ^ c ^ d, a, b, x, s, t);
  }

  function ii(a, b, c, d, x, s, t) {
    return cmn(c ^ (b | (~d)), a, b, x, s, t);
  }

  function safe_add(x, y) {
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
    return (msw << 16) | (lsw & 0xFFFF);
  }

  function bit_rol(num, cnt) {
    return (num << cnt) | (num >>> (32 - cnt));
  }
})();

(function() {
  /* Express a completed MD5 calculation in its conventional hex
   * representation. This is mostly imported from the source implementation.
   */
  MD5.prototype.asString = function() {
    var md5arr = this.asArray();
    return rstr2hex(binl2rstr(md5arr));
  };

  function binl2rstr(input)
  {
    var output = "";
    for(var i = 0; i < input.length * 32; i += 8)
      output += String.fromCharCode((input[i>>5] >>> (i % 32)) & 0xFF);
    return output;
  }

  function rstr2hex(input)
  {
    var hex_tab = "0123456789abcdef";
    var output = "";
    var x;
    for(var i = 0; i < input.length; i++)
    {
      x = input.charCodeAt(i);
      output += hex_tab.charAt((x >>> 4) & 0x0F)
             +  hex_tab.charAt( x        & 0x0F);
    }
    return output;
  }
})();
