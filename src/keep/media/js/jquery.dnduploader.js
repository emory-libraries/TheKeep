(function( $ ){

  var methods = {
    init : function(options) {  

    return this.each(function(){      

       var $this = $(this);
       var data = {
        'file_count': 0,
        'files': new Array(),
        'ingest_on_completion': false,
       };
       $.extend(data, options);

       // create a special-function ingest button
       var ingest_button = $('<input type="button" value="Submit when all uploads complete"/>');
       ingest_button.click(function(){
          var data = $(this).prev().data('dnduploader');
          data['ingest_on_completion'] = true;
          $(this).prev().data('dnduploader', data);
          $(this).after("<p>Items will be submitted for ingest when all uploads complete.</p>");
       });
       $this.after(ingest_button);

       // following recommended practice: store data in one object with name of plugin
       $this.data('dnduploader', data);

       $this.bind('dragenter.dndUploader', methods.dragEnter);
       $this.bind('dragover.dndUploader', methods.dragOver);
       $this.bind('drop.dndUploader', methods.drop);
       $this.bind('dragleave.dndUploader', methods.dragLeave);
     });
    },

    dragEnter : function (event) {
      $(this).addClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      return false;
    },

    dragOver : function (event) {
      $(this).addClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      return false;
    },

    dragLeave : function (event) {
      $(this).removeClass('dragover');

      return false;
    },

    drop : function(event) {
      $(this).removeClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      var obj = $(this);
      var data = obj.data('dnduploader');
      // store current file count - marker for where to start processing in full list of files
      var start_processing = data['file_count'];
      var allowed_types =  data['allowed_types'];
      var not_allowed = new Array();
      // display files if they are allowed type, add to list of all files
      if (event.originalEvent.dataTransfer.files.length > 0) {
        $.each(event.originalEvent.dataTransfer.files, function ( i, file ) {
            // if allowed types are defined, check that file is one of the specified types
            if (allowed_types.length &&
                $.inArray(file.type, allowed_types) != -1) {    // returns index or -1 if not found
                // rudimentary list display
                var p = $('<p><a class="remove">X</a> ' + file.fileName + ' ' +
                    '<span class="file-info">(' + filesize_format(file.size) +
		    ', ' + file.type + ')</span></p>');
                obj.append(p);
                // create status node and attach to file so it is easy to update
                file.status = $('<span class="status">-</span>');
                p.append(file.status);
                data['files'].push(file);
                data['file_count']++;
            } else {
                // push dis-allowed files into a list so they can be reported all at once
                not_allowed.push(file);
            }
        });
        $(".remove").click(function () {$(this).parent().remove(); });

        if (not_allowed.length) {
          var msg = "The following file(s) were not added because the " +
                "type indicates they are not a supported upload formats:\n\n";
          $.each(not_allowed, function ( i, file ) {
            msg += "  " + file.fileName + "\t" + file.type + "\n";
           });
           alert(msg);
        }
        // update stored data
        obj.data('dnduploader', data);
	// if there are new files to process, disable submit button until upload completes
        if (data['file_count'] > start_processing) {
	  methods.disableSubmit.apply(obj);
       }

       // loop through files added on the current drop
       // calculate checksum and then upload 
       for (var x = start_processing; x < data['files'].length; x++) {
            var file = data['files'][x];
            // update status
            file.status.html('calculating checksum');
            // give each file a separate reader so they don't clobber each other
            reader = new FileReader();
            // set handler for when file reading completes
            var obj = $(this);
            reader.onloadend = function (evt){
                  file.status.html('calculating checksum');
                  file.md5 = rstr2hex(rstr_md5(evt.target.result));
                  console.log(file.fileName + ' checksum ' + file.md5);
                  file.status.html('uploading');
                  methods.uploadFile.apply(obj, [file]);
                };
            reader.readAsBinaryString(file);
            }
      };

      return false;
    },

    afterUpload: function() {
        var data = $(this).data('dnduploader');
        // check if all files have finished uploaded
        for (var x = 0; x < data['files'].length; x++) {
            if (! data['files'][x].upload_id) {
                return;
            }
        }
        // all files have completed uploading - if requested, submit the form
        if (data['ingest_on_completion']) {
            $(this).parents('form').submit();
        }
        // otherwise, re-enable normal submit button
        methods.enableSubmit.apply($(this));
    },

    disableSubmit: function() {
       $(this).nextAll('[type="submit"]').attr('disabled', 'disabled');
    },

    enableSubmit: function() {
      $(this).nextAll('[type="submit"]').removeAttr('disabled');
    },

    uploadFile: function(file) {
       var data = $(this).data('dnduploader');
       var obj = $(this);
       var xhr   = new XMLHttpRequest();

        // display an upload progress bar
        var indicator = $('<p/>');
        file.progress = $('<div class="progress-bar"/>');
        file.progress.append(indicator);
        file.status.append(file.progress);
        xhr.upload.addEventListener("progress", function(event) {
              if (event.lengthComputable) {
                var percentage = Math.round((event.loaded * 100) / event.total);
                indicator.width(percentage);
                indicator.html(percentage + "%");
              }
            }, false);

        xhr.open('POST', data['url'], true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        // set required headers for processing the file
        xhr.setRequestHeader('Content-Disposition', "filename=" + file.fileName);
        xhr.setRequestHeader('Content-Type', file.type);
        xhr.setRequestHeader('Content-MD5', file.md5);

        // Content-Length header could be set explicitly from file.size,
        // but should be set automatically by the browser (tested in FF and Chrome)

        xhr.onreadystatechange = function() {
          if (xhr.readyState == 4) {
            if(xhr.status == 200) { // ok
                file.status.html('Ready to ingest');
                file.upload_id = xhr.responseText;
                // add form data for submission
                // - adding to file dom element so we can easily remove individual files
                file.status.parent().append('<input type="hidden" name="fileUploads" value="' + file.upload_id + '"/>');
                file.status.parent().append('<input type="hidden" name="originalFileNames" value="' + file.fileName + '"/>');
                file.status.parent().append('<input type="hidden" name="fileMD5sum" value="' + file.md5 + '"/>');

             } else { // if(xhr.status == 400)  // bad request
                file.status.html('Upload error: ' + xhr.responseText);
                file.upload_id = -1;
                // TODO: include upload errors in the form somehow so that
                // we can report them on the form submission page
             }

             methods.afterUpload.apply(obj);
          }
        };


        xhr.send(file);
    },
   
  };
  

  $.fn.dndUploader = function( method ) {
    if ( methods[method] ) {
      return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } else if ( typeof method === 'object' || ! method ) {
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  method + ' does not exist on jQuery.dndUploader' );
    }
  };
})( jQuery );



// FIXME: where should filesize_format function go?
/* convert integer filesize in bytes to a human-readable format */
function filesize_format(size) {
    if (size === 0) {
        return '';
    } else if (size < 100) {
        return '' + size + ' bytes';
    } else if (size < (1000 * 1000)) {
        size = size / 1000;
        size = '' + size;
        vals = size.split('.');
        return vals[0] + '.' + vals[1].substring(0, 1) + 'kb';
    } else {
        size = size / (1000 * 1000);
        size = '' + size;
        vals = size.split('.');
        return vals[0] + '.' + vals[1].substring(0, 1) + 'mb';
    }
    // TODO: gb ?
}

